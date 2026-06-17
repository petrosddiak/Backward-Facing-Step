# Steady flow over a 2D backward facing step

## This canonical case is based on the description by Driver and Seegmiller

    D.M. Driver and H.L. Seegmiller. Features of a reattaching turbulent shear
    layer in divergent channel flow. AIAA Journal, 23(2):163–171, 1985.

## Introduction

This study serves as a comparison between OpenFOAM's simpleFoam solver and experimental data as obtained from a study done on the backward facing step with 0deg inclination. The workflow is fully automated, from mesh generation, to solver setup and post-processing. Further tests can be performed by changing mesh size, inlet velocity, duct length, wall inclination and other parameters, in order to study various setups.  


## Setup Details

Reynolds number based on the momentum thickness height is 5000 at 4 step heights upstream of the step.
Freestream velocity is 44.2 m/s at atmospheric pressure and temperature which corresponds to a Ma=0.128.
![Flow Geometry (not to scale)](images/domain.png)
Stated reattachment length is at 6.26 +/- 0.1 x/h

## Case Runs

### Mesh manipulations

To change domain length, step height etc. modify vertices in the ***blockMeshDict*** file.
To calculate desired edge grading based on length, number of cells and first cell height, run the ***calc_grading.py*** script.
To alter number of cells on edges and input the calculated edge gradings, use the ***mesh_config.txt*** file.
Use the ***run_mesh.sh*** to update the mesh.

### Solver setup

3 different mesh sizings were tested, with a refinement factor of ~2 (12k, 28k and 56k elements). Measured quantity was the RMS L2 norm of velocity profile differences at different x/H locations. No significant changes were noticed after the medium mesh refinement, so it was kept as the benchmark of the study. Inlet boundary condition is the velocity profile as obtained from the experimental data. Outlet is atmospheric pressure and walls are set as no-slip.

The case runs using the ***execution.sh*** script.

### Results discussion

As expected the flow separates after the step due to adverse pressure gradients, which causes a recirculation bubble:
<img src="images/streamlines.png" alt="Velocity colored streamlines through the duct" width="70%">

Velocity profiles are captured relatively accurately away from the lower wall and close to the upper wall:
<img src="images/velocity_profiles.png" alt="Velocity profiles (experimental data vs OpenFOAM)" width="70%">

Things immediately evident:
1. Reattachment roughly in the right location
2. Recirculation zone shape reasonably well
3. Near-wall reverse flow reasonably well


However looking closer at the near-wall velocity profiles for the lower part of the duct, there is not a very good agreement between the 2 datasets:

<img src="images/velocity_profiles_close-up.png" alt="Velocity profiles (close-up at lower wall)" width="70%">


This is a proof that RANS models overpredict turbulent mixing, diffuse the shear layer too quickly and recover to equilibrium too fast. This incorrect velocity profile capturing leads in turn in discrepancies at the developed shear, thus the reattachment location:

<img src="images/Cf.png" alt="Skin friction coefficient (experimental data vs OpenFOAM)" width="70%">


Worth keeping in mind that the ERCOFTAC experiment is an inherently 3D case with side wall effects, large scale coherent structures and most importantly turbulence anisotropy. On the other hand, OpenFOAM setup is a 2.5D case which tends to lead towards a developed flow faster.



For further information please visit:

    https://www.openfoam.com/documentation/guides/latest/doc/verification-validation-turbulent-backward-facing-step.html
