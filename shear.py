import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the CSV file
# Replace 'shear_stress.csv' with your actual file path if it's located elsewhere
file_path = 'shear_stress.csv'
df = pd.read_csv(file_path)

# 2. Clean and Isolate the Data
# Since the data has entries for multiple Z depths (Points:2), we group by the 
# X coordinate (Points:0) and take the mean of Cf to collapse it into a clean 2D line.
df_clean = df.groupby('Points:0', as_index=False)['Cf'].mean()

# 3. Sort by the X location to ensure the line connects sequentially
df_clean = df_clean.sort_values(by='Points:0')

# Extract our clean plotting vectors
x_coords = df_clean['Points:0']
cf_values = df_clean['Cf']

# 4. Generate the Plot
plt.figure(figsize=(10, 5), dpi=100)

# Plot the skin friction distribution curve
plt.plot(x_coords, cf_values, color='blue', linewidth=2, label='Skin Friction ($C_f$)')

# Add crucial reference lines for CFD validation
plt.axhline(0, color='black', linestyle='-', linewidth=0.8)  # Zero threshold line
plt.axvline(0, color='red', linestyle='--', alpha=0.8, label='Step Location ($X=0$)')  # Step indicator

# --- Exact Reattachment Calculation ---
# Find where Cf crosses 0 from positive (recirculation) to negative (reattached flow)
xr = None
# Filter points downsteam of the step (X > 0)
df_downstream = df_clean[df_clean['Points:0'] >= 0].reset_index(drop=True)

for i in range(1, len(df_downstream)):
    # In OpenFOAM's convention, positive is reversed flow, negative is forward flow
    if df_downstream.loc[i-1, 'Cf'] > 0 and df_downstream.loc[i, 'Cf'] <= 0:
        x1, x2 = df_downstream.loc[i-1, 'Points:0'], df_downstream.loc[i, 'Points:0']
        y1, y2 = df_downstream.loc[i-1, 'Cf'], df_downstream.loc[i, 'Cf']
        # Linear interpolation for perfect precision
        xr = x1 - y1 * (x2 - x1) / (y2 - y1)
        
        # Mark it on the plot
        plt.scatter(xr, 0, color='red', s=80, zorder=5)
        plt.annotate(f'Reattachment $X_r = {xr:.4f}$ m', xy=(xr, 0), 
                     xytext=(xr + 0.05, 0.0012),
                     arrowprops=dict(facecolor='black', shrink=0.08, width=1, headwidth=6))
        break

# 5. Styling and Labels
plt.xlabel('Duct Position $X$ [m]', fontsize=11)
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
if xr:
    print(f"Calculated Reattachment Length (Xr): {xr:.5f} meters downstream of the step.")