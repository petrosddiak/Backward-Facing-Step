import numpy as np
import sys
from pathlib import Path
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

H = 0.0127

data = np.loadtxt("/home/petros/cfd_projects/step_duct/postProcessing/lineExtract/1500/line_X-0.051_p_U.xy")  # space-separated by default
Y = data[:, 0]
P = data[:, 1]
U = data[:, 2]
V = data[:, 3]
W = data[:, 4]

U_ref = 44.2
y_wall = np.min(Y)
Y_shifted = Y - y_wall

U_ratio = U / U_ref
edge_idx = np.where(U_ratio >= 0.99)[0][0]

Y_filtered = Y_shifted[:edge_idx]
U_filtered = U[:edge_idx]

integ_funct = U_filtered/U_ref*(1-U_filtered/U_ref)

print(edge_idx)

theta = np.trapz((U_filtered / U_ref) * (1 - U_filtered / U_ref), Y_filtered)
print(theta)
