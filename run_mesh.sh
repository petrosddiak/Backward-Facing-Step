#!/bin/bash

# Exit immediately if any command returns a non-zero exit status
set -e

echo "=========================================="
echo " Starting Mesh Generation Workflow        "
echo "=========================================="

# 1. Run your Python script to update the blockMeshDict
if [ -f "modify_blockmesh.py" ]; then
    echo "--> Running Python script to modify blockMeshDict..."
    python3 modify_blockmesh.py
else
    echo "Error: modify_blockmesh.py not found in the current directory."
    exit 1
fi

# 2. Run blockMesh to generate the OpenFOAM mesh
echo ""
echo "--> Running blockMesh..."
blockMesh

# 3. Open the mesh in ParaView
echo ""
echo "--> Opening paraFoam for visualization..."
paraFoam