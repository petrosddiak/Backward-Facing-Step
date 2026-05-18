import re
import numpy as np
import matplotlib.pyplot as plt
import math
from pathlib import Path

# -----------------------------
# PARAMETERS (ADJUST THESE)
# -----------------------------
Urel = 44.2
H = 0.0127

# -----------------------------
# READ EXPERIMENTAL DATA
# -----------------------------
def read_backstep_file(filename):
    data = []
    current_block = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()

            if "X/H=" in line:
                match = re.search(r'X/H=\s*([-+]?\d*\.?\d+)', line)
                if match:
                    if current_block is not None:
                        data.append(current_block)

                    current_block = {
                        "X/H": float(match.group(1)),
                        "Y/H": [],
                        "U/Ur": [],
                        "V/Ur": []
                    }

            elif re.match(r'^\d+', line):
                parts = line.split()

                if len(parts) >= 4 and current_block is not None:
                    try:
                        current_block["Y/H"].append(float(parts[1]))
                        current_block["U/Ur"].append(float(parts[2]))
                        current_block["V/Ur"].append(float(parts[3]))
                    except ValueError:
                        pass

    if current_block is not None:
        data.append(current_block)

    return data


# -----------------------------
# READ CFD FILE
# -----------------------------
def read_cfd_file(filename):
    data = np.loadtxt(filename)

    if data.shape[1] >= 5:
        Y = data[:, 0]
        U = data[:, 2]
        V = data[:, 3]
    else:
        raise ValueError(f"Unexpected format in {filename}")

    return Y, U, V


# -----------------------------
# LOAD DATA
# -----------------------------
data_exp = read_backstep_file("experimental.dat")

linePathFolder = Path("/home/petros/cfd_projects/step_duct/postProcessing/lineExtract/")
cfd_data = []

for file in linePathFolder.rglob("*.xy"):
    filename = file.stem  # e.g. line_-2

    match = re.search(r'[-+]?\d*\.?\d+', filename)
    if not match:
        print(f"Skipping file: {file}")
        continue

    x_val = float(match.group()) / H
    print(f"Loaded CFD file: {file.name} → X/H = {x_val}")

    Y_cfd, U_cfd, V_cfd = read_cfd_file(file)

    # --- normalize
    Y_norm = Y_cfd / H
    U_norm = U_cfd / Urel
    V_norm = V_cfd / Urel

    # --- filter (remove Y < 0)
    mask = Y_norm >= 0
    Y_norm = Y_norm[mask]
    U_norm = U_norm[mask]
    V_norm = V_norm[mask]

    # --- sort
    idx = np.argsort(Y_norm)
    Y_norm = Y_norm[idx]
    U_norm = U_norm[idx]
    V_norm = V_norm[idx]

    cfd_data.append({
        "X/H": x_val,
        "Y/H": Y_norm,
        "U/Ur": U_norm,
        "V/Ur": V_norm
    })

# sort CFD blocks
cfd_data = sorted(cfd_data, key=lambda d: d["X/H"])

# -----------------------------
# PLOTTING
# -----------------------------
n = len(data_exp)

ncols = 4
nrows = math.ceil(n / ncols)

fig, axes = plt.subplots(nrows, ncols, figsize=(15, 10), sharey=True)
axes = axes.flatten()

for i, block in enumerate(data_exp):
    ax = axes[i]

    x_exp = block["X/H"]

    # --- experimental (filter Y >= 0 just in case)
    y_exp = np.array(block["Y/H"])
    u_exp = np.array(block["U/Ur"])

    mask = y_exp >= 0
    y_exp = y_exp[mask]
    u_exp = u_exp[mask]

    ax.scatter(u_exp, y_exp, color='black', label='Exp')

    # --- find closest CFD station
    if len(cfd_data) > 0:
        cfd_match = min(cfd_data, key=lambda d: abs(d["X/H"] - x_exp))

        y_cfd = np.array(cfd_match["Y/H"])
        u_cfd = np.array(cfd_match["U/Ur"])

        ax.scatter(u_cfd, y_cfd, color='red', s=4, label='CFD')

        # -----------------------------
        # PRINT COMPARISON
        # -----------------------------
        print(f"\n=== EXP X/H = {x_exp:.3f} | CFD X/H = {cfd_match['X/H']:.3f} ===")
        print(f"ΔX/H = {abs(x_exp - cfd_match['X/H']):.3e}")

        for y_e, u_e in zip(y_exp, u_exp):
            idx_closest = np.argmin(np.abs(y_cfd - y_e))

            y_c = y_cfd[idx_closest]
            u_c = u_cfd[idx_closest]

            print(f"Y_exp={y_e:.3f}  Y_cfd={y_c:.3f}  ΔY={abs(y_e-y_c):.3e} | "
                  f"U_exp={u_e:.3f}  U_cfd={u_c:.3f}")

    ax.set_title(f"X/H = {x_exp}")
    ax.grid()

    if i == 0:
        ax.legend()

# remove empty subplots
for j in range(i + 1, len(axes)):
    fig.delaxes(axes[j])

fig.supxlabel("U/Ur")
fig.supylabel("Y/H")

plt.tight_layout()
plt.show()