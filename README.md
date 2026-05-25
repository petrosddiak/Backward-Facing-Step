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

To change domain length, step height etc. modify vertices in the *blockMeshDict* file.
To calculate desired edge grading based on length, number of cells and first cell height, run the *calc_grading.py* script.
To alter number of cells on edges and input the calculated edge gradings, use the *mesh_config.txt* file.
Use the *run_mesh.sh* to update the mesh.

### Solver runs

3 different mesh sizings were tested, with a refinement factor of ~2 (12k, 28k and 56k elements). Measured quantity wasNo significant changes were noticed after
To run the case, use the *execution.sh* script. To change mesh seetings

For further information please visit:

    https://www.openfoam.com/documentation/guides/latest/doc/verification-validation-turbulent-backward-facing-step.html
