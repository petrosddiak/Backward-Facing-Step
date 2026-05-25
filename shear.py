import pandas as pd
import matplotlib.pyplot as plt
import re
from pathlib import Path


def load_mesh_dimensions(file_path):
    text = Path(file_path).read_text()
    scale_match = re.search(r'^\s*scale\s+([\d.eE+-]+)\s*;', text, re.MULTILINE)
    scale = float(scale_match.group(1)) if scale_match else 1.0

    vertices_match = re.search(r'vertices\s*\((.*?)\);', text, re.DOTALL)
    if not vertices_match:
        raise ValueError(f'Could not find vertices in {file_path}')

    vertices = []
    for match in re.finditer(
        r'\(\s*([-\d.eE+]+)\s+([-\d.eE+]+)\s+([-\d.eE+]+)\s*\)',
        vertices_match.group(1)
    ):
        vertices.append(tuple(float(value) * scale for value in match.groups()))

    x_values = [point[0] for point in vertices]
    y_values = sorted({point[1] for point in vertices})
    positive_y_values = [y for y in y_values if y > 0]

    return {
        'x_min': min(x_values),
        'x_max': max(x_values),
        'step_height': min(positive_y_values),
    }


MESH = load_mesh_dimensions('system/blockMeshDict')
STEP_HEIGHT = MESH['step_height']


def load_experimental_shear(file_path, alpha=0):
    rows = []
    current_alpha = None

    with open(file_path, 'r') as f:
        for line in f:
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith('#'):
                if 'Alpha =' in stripped:
                    current_alpha = float(stripped.split('Alpha =')[1].split('degrees')[0])
                continue

            if current_alpha == alpha:
                x_over_h, cf, relative_uncertainty = map(float, stripped.split()[:3])
                rows.append((x_over_h, x_over_h * STEP_HEIGHT, cf, relative_uncertainty))

    return pd.DataFrame(rows, columns=['x_over_h', 'x', 'Cf', 'relative_uncertainty'])


# 1. Load the CSV file
# Replace 'shear_stress.csv' with your actual file path if it's located elsewhere
file_path = 'shear_stress.csv'
df = pd.read_csv(file_path)
df_exp = load_experimental_shear('shear_exp.dat', alpha=0)

csv_path = Path(file_path)
mesh_path = Path('constant/polyMesh/points')
if mesh_path.exists() and csv_path.exists() and csv_path.stat().st_mtime < mesh_path.stat().st_mtime:
    print(
        f'Warning: {file_path} is older than constant/polyMesh/points. '
        'Regenerate shear_stress.csv to use the new mesh results.'
    )

domain_mask = df['Points:0'].between(MESH['x_min'], MESH['x_max'])
if not domain_mask.all():
    removed = len(df) - int(domain_mask.sum())
    print(f'Warning: removed {removed} shear points outside the current mesh x-range.')
    df = df[domain_mask]

if df.empty:
    raise ValueError(
        f'{file_path} has no points inside the current mesh x-range '
        f'[{MESH["x_min"]}, {MESH["x_max"]}]. Regenerate the shear data from the current mesh.'
    )

# 2. Clean and Isolate the Data
# Since the data has entries for multiple Z depths (Points:2), we group by the 
# X coordinate (Points:0) and take the mean of Cf to collapse it into a clean 2D line.
df_clean = df.groupby('Points:0', as_index=False)['Cf'].mean()

# 3. Sort by the X location to ensure the line connects sequentially
df_clean = df_clean.sort_values(by='Points:0')

# Extract our clean plotting vectors and normalize streamwise position by step height
x_coords = df_clean['Points:0'] / STEP_HEIGHT
cf_values = df_clean['Cf']

# 4. Generate the Plot
plt.figure(figsize=(10, 5), dpi=100)

# Plot the skin friction distribution curve
plt.plot(x_coords, cf_values, color='blue', linewidth=2, label='CFD ($C_f$)')
plt.errorbar(
    df_exp['x_over_h'],
    df_exp['Cf'],
    yerr=(df_exp['Cf'].abs() * df_exp['relative_uncertainty']),
    fmt='o',
    color='darkorange',
    ecolor='darkorange',
    elinewidth=1,
    capsize=3,
    markersize=4,
    label='Experiment, alpha=0 deg'
)

# Add crucial reference lines for CFD validation
plt.axhline(0, color='black', linestyle='-', linewidth=0.8)  # Zero threshold line
plt.axvline(0, color='red', linestyle='--', alpha=0.8, label='Step Location ($X/H=0$)')  # Step indicator

# --- Exact Reattachment Calculation ---
# Find where Cf crosses 0 from negative (recirculation) to positive (reattached flow)
xr = None
xr_over_h = None
# Filter points downsteam of the step (X > 0)
df_downstream = df_clean[df_clean['Points:0'] >= 0].reset_index(drop=True)

for i in range(1, len(df_downstream)):
    if df_downstream.loc[i-1, 'Cf'] < 0 and df_downstream.loc[i, 'Cf'] >= 0:
        x1, x2 = df_downstream.loc[i-1, 'Points:0'], df_downstream.loc[i, 'Points:0']
        y1, y2 = df_downstream.loc[i-1, 'Cf'], df_downstream.loc[i, 'Cf']
        # Linear interpolation for perfect precision
        xr = x1 - y1 * (x2 - x1) / (y2 - y1)
        xr_over_h = xr / STEP_HEIGHT
        
        # Mark it on the plot
        plt.scatter(xr_over_h, 0, color='red', s=80, zorder=5)
        plt.annotate(f'Reattachment $X_r/H = {xr_over_h:.2f}$', xy=(xr_over_h, 0),
                     xytext=(xr_over_h + 2.0, 0.0012),
                     arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6))
        break

# 5. Styling and Labels
plt.xlabel('Duct Position $X/H$', fontsize=11)
plt.ylabel('Skin Friction Coefficient ($C_f$)', fontsize=11)
plt.title('Wall Skin Friction Distribution along Step Duct Floor', fontsize=12, fontweight='bold')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend(frameon=True, facecolor='white', edgecolor='none')

# Adjust limits slightly based on your coordinate ranges
plt.xlim(x_coords.min(), x_coords.max())

# Display the final output
plt.tight_layout()
plt.show()

# Print text readout
if xr is not None:
    print(f"Calculated Reattachment Length (Xr/H): {xr_over_h:.5f}")
    print(f"Calculated Reattachment Length (Xr): {xr:.5f} meters downstream of the step.")
