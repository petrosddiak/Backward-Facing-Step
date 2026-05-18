# Save this as generate_lines.py in your case directory
import numpy as np

# Number of lines to extract
num_lines = 22
x_positions_norm = [-4, -2, -1, 0, 1, 1.5, 2, 2.5, 3, 4, 5, 5.5, 6, 6.5, 7, 8, 10, 12, 14, 16, 20, 32]  # Normalized positions (X/H) as in the experimental data
x_positions = [x*0.0127 for x in x_positions_norm] #np.interp(x_positions_norm, [-4, 32], [-0.05, 0.4064])  # Map normalized positions to actual X coordinates

# Fixed Y and Z limits
y_start, y_end = 0.0, 0.1137
z_fixed = 0.0
n_points = 200  # Number of points along each line

# Write out the OpenFOAM formatted file
with open("system/lineExtraction", "w") as f:
    f.write("lineExtract\n{\n")
    f.write("    type            sets;\n")
    f.write("    libs            (sampling);\n")
    f.write("    writeControl    writeTime;\n")
    f.write("    interpolationScheme cellPoint;\n")
    f.write("    setFormat       raw;\n")
    f.write("    fields          (U p);\n\n")
    f.write("    sets\n    (\n")

    for i, x in enumerate(x_positions):
        f.write(f"        line_X{x:.3f}\n")
        f.write("        {\n")
        f.write("            type        uniform;\n")
        f.write("            axis        y;\n")
        f.write(f"            start       ({x:.4f} {y_start} {z_fixed});\n")
        f.write(f"            end         ({x:.4f} {y_end} {z_fixed});\n")
        f.write(f"            nPoints     {n_points};\n")
        f.write("        }\n")

    f.write("    );\n")
    f.write("}\n")

print(f"Successfully generated {num_lines} lines in 'system/lineExtraction'!")