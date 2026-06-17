import math
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# -----------------------------
# PARAMETERS
# -----------------------------
Urel = 44.2
H = 0.0127
LINE_PATH_FOLDER = Path("postProcessing/lineExtract")
GRID_PROFILE_DIR = Path("grid_profiles")


# -----------------------------
# READ EXPERIMENTAL DATA
# -----------------------------
def read_backstep_file(filename):
    data = []
    current_block = None

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()

            if "X/H=" in line:
                match = re.search(r"X/H=\s*([-+]?\d*\.?\d+)", line)
                if match:
                    if current_block is not None:
                        data.append(current_block)

                    current_block = {
                        "X/H": float(match.group(1)),
                        "Y/H": [],
                        "U/Ur": [],
                        "V/Ur": [],
                    }

            elif re.match(r"^\d+", line):
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
# READ CFD DATA
# -----------------------------
def read_cfd_file(filename):
    data = np.loadtxt(filename)

    if data.ndim == 1:
        data = data.reshape(1, -1)

    if data.shape[1] < 5:
        raise ValueError(f"Unexpected format in {filename}")

    y = data[:, 0]
    u = data[:, 2]
    v = data[:, 3]

    return y, u, v


def latest_time_folder(line_path_folder):
    folders = [path for path in line_path_folder.iterdir() if path.is_dir()]
    numeric_folders = []

    for folder in folders:
        try:
            numeric_folders.append((float(folder.name), folder))
        except ValueError:
            pass

    if not numeric_folders:
        raise FileNotFoundError(f"No numeric time folders found in {line_path_folder}")

    return max(numeric_folders, key=lambda item: item[0])[1]


def x_over_h_from_filename(file_path):
    match = re.search(r"line_X([-+]?\d*\.?\d+)", file_path.stem)
    if not match:
        raise ValueError(f"Could not read X location from {file_path.name}")

    return float(match.group(1)) / H


def load_cfd_profiles(line_path_folder=LINE_PATH_FOLDER, time_folder=None):
    if time_folder is None:
        profile_folder = latest_time_folder(line_path_folder)
    else:
        profile_folder = line_path_folder / str(time_folder)

    cfd_data = []

    for file in sorted(profile_folder.glob("*.xy")):
        try:
            x_val = x_over_h_from_filename(file)
        except ValueError:
            print(f"Skipping file: {file}")
            continue

        y_cfd, u_cfd, v_cfd = read_cfd_file(file)

        y_norm = y_cfd / H
        u_norm = u_cfd / Urel
        v_norm = v_cfd / Urel

        mask = y_norm >= 0
        y_norm = y_norm[mask]
        u_norm = u_norm[mask]
        v_norm = v_norm[mask]

        idx = np.argsort(y_norm)

        cfd_data.append(
            {
                "X/H": x_val,
                "Y/H": y_norm[idx],
                "U/Ur": u_norm[idx],
                "V/Ur": v_norm[idx],
                "source": str(file),
            }
        )

    cfd_data = sorted(cfd_data, key=lambda block: block["X/H"])

    if not cfd_data:
        raise FileNotFoundError(f"No .xy profile files found in {profile_folder}")

    print(f"Loaded {len(cfd_data)} CFD profiles from {profile_folder}")
    return cfd_data


# -----------------------------
# GRID-INDEPENDENCE EXPORT/COMPARE
# -----------------------------
def save_grid_profiles(label, cfd_data, output_dir=GRID_PROFILE_DIR):
    output_dir.mkdir(exist_ok=True)

    out = {"n_profiles": len(cfd_data)}

    for i, block in enumerate(cfd_data):
        key = f"profile_{i}"
        out[f"{key}_x"] = block["X/H"]
        out[f"{key}_y"] = np.asarray(block["Y/H"])
        out[f"{key}_u"] = np.asarray(block["U/Ur"])
        out[f"{key}_v"] = np.asarray(block["V/Ur"])

    output_path = output_dir / f"{label}.npz"
    np.savez(output_path, **out)
    print(f"Saved {len(cfd_data)} profiles to {output_path}")


def load_grid_profiles(label, output_dir=GRID_PROFILE_DIR):
    path = output_dir / f"{label}.npz"
    data = np.load(path)

    profiles = []
    for i in range(int(data["n_profiles"])):
        key = f"profile_{i}"
        profiles.append(
            {
                "X/H": float(data[f"{key}_x"]),
                "Y/H": data[f"{key}_y"],
                "U/Ur": data[f"{key}_u"],
                "V/Ur": data[f"{key}_v"],
            }
        )

    return profiles


def profile_l2(profile_a, profile_b, component="U/Ur", n_points=300):
    y_min = max(profile_a["Y/H"].min(), profile_b["Y/H"].min())
    y_max = min(profile_a["Y/H"].max(), profile_b["Y/H"].max())

    if y_max <= y_min:
        raise ValueError("Profiles do not overlap in Y/H.")

    y_common = np.linspace(y_min, y_max, n_points)
    a_values = np.interp(y_common, profile_a["Y/H"], profile_a[component])
    b_values = np.interp(y_common, profile_b["Y/H"], profile_b[component])

    return np.sqrt(np.trapz((a_values - b_values) ** 2, y_common) / (y_max - y_min))


def l2_between_grids(label_a, label_b, component="U/Ur"):
    profiles_a = load_grid_profiles(label_a)
    profiles_b = load_grid_profiles(label_b)
    station_errors = []

    print(f"Comparing {label_a} to {label_b} using {component}")

    for profile_a in profiles_a:
        profile_b = min(profiles_b, key=lambda profile: abs(profile["X/H"] - profile_a["X/H"]))
        error = profile_l2(profile_a, profile_b, component=component)
        station_errors.append(error)

        print(
            f"X/H {profile_a['X/H']:8.3f} vs {profile_b['X/H']:8.3f} | "
            f"L2({component}) = {error:.6e}"
        )

    total = np.sqrt(np.mean(np.asarray(station_errors) ** 2))
    print(f"\nOverall RMS L2({label_a}, {label_b}) = {total:.6e}")


# -----------------------------
# PLOTTING
# -----------------------------
def plot_experiment_vs_cfd(data_exp, cfd_data):
    n = len(data_exp)
    ncols = 4
    nrows = math.ceil(n / ncols)

    fig, axes = plt.subplots(nrows, ncols, figsize=(15, 10), sharey=True)
    axes = np.asarray(axes).flatten()

    for i, block in enumerate(data_exp):
        ax = axes[i]
        x_exp = block["X/H"]

        y_exp = np.asarray(block["Y/H"])
        u_exp = np.asarray(block["U/Ur"])

        mask = y_exp >= 0
        y_exp = y_exp[mask]
        u_exp = u_exp[mask]

        ax.scatter(u_exp, y_exp, color="black", label="Exp")

        cfd_match = min(cfd_data, key=lambda data: abs(data["X/H"] - x_exp))
        y_cfd = np.asarray(cfd_match["Y/H"])
        u_cfd = np.asarray(cfd_match["U/Ur"])

        ax.scatter(u_cfd, y_cfd, color="red", s=4, label="CFD")

        print(f"\n=== EXP X/H = {x_exp:.3f} | CFD X/H = {cfd_match['X/H']:.3f} ===")
        print(f"Delta X/H = {abs(x_exp - cfd_match['X/H']):.3e}")

        for y_e, u_e in zip(y_exp, u_exp):
            idx_closest = np.argmin(np.abs(y_cfd - y_e))
            y_c = y_cfd[idx_closest]
            u_c = u_cfd[idx_closest]

            print(
                f"Y_exp={y_e:.3f}  Y_cfd={y_c:.3f}  "
                f"Delta Y={abs(y_e - y_c):.3e} | "
                f"U_exp={u_e:.3f}  U_cfd={u_c:.3f}"
            )

        ax.set_title(f"X/H = {x_exp}")
        ax.grid()

        if i == 0:
            ax.legend()

    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    fig.supxlabel("U/Ur")
    fig.supylabel("Y/H")

    plt.tight_layout()
    plt.show()


def main():
    if len(sys.argv) >= 2:
        mode = sys.argv[1]

        if mode == "export":
            if len(sys.argv) != 3:
                raise SystemExit("Usage: python3 comparison.py export <label>")
            cfd_data = load_cfd_profiles()
            save_grid_profiles(sys.argv[2], cfd_data)
            return

        if mode == "compare":
            if len(sys.argv) not in (4, 5):
                raise SystemExit("Usage: python3 comparison.py compare <label_a> <label_b> [U/Ur|V/Ur]")
            component = sys.argv[4] if len(sys.argv) == 5 else "U/Ur"
            l2_between_grids(sys.argv[2], sys.argv[3], component=component)
            return

        raise SystemExit(f"Unknown mode: {mode}")

    data_exp = read_backstep_file("experimental.dat")
    cfd_data = load_cfd_profiles()
    plot_experiment_vs_cfd(data_exp, cfd_data)


if __name__ == "__main__":
    main()
