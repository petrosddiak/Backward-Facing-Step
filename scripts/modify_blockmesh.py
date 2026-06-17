import os
import re

def parse_config_file(config_path):
    """Parses the user text configuration file into a dictionary."""
    config_data = {}
    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' not found.")
        return None

    with open(config_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            try:
                parts = [p.strip() for p in line.split('|')]
                block_id = int(parts[0])
                cells = parts[1]
                grad_type = parts[2].lower()
                grad_val = parts[3]
                
                config_data[block_id] = {
                    "cells": f"({cells})",
                    "grad_type": grad_type,
                    "grad_val": grad_val
                }
            except (IndexError, ValueError):
                print(f"Skipping malformed line in config: '{line}'")
    return config_data


def modify_generic_blockmesh():
    dict_path = "system/blockMeshDict"
    
    if not os.path.exists(dict_path):
        print(f"Error: Could not find {dict_path}.")
        return

    # Read current file
    with open(dict_path, 'r') as f:
        content = f.read()

    # Step 1: Capture the exact contents of the blocks section
    # This specifically isolates only the region inside the blocks(...) keyword
    blocks_match = re.search(r"(blocks\s*\n\s*\(\s*\n)(.*?)(\n\s*\);)", content, re.DOTALL)
    if not blocks_match:
        print("Error: Could not parse the 'blocks' section correctly.")
        return

    header, blocks_text, footer = blocks_match.groups()

    # Step 2: Use regex to extract every valid block individually
    # Matches: hex (...) (N N N) simpleGrading/edgeGrading (...) or $variable
    block_regex = re.compile(
        r"(hex\s*\([^\)]+\)\s*)(\(\s*\d+\s+\d+\s+\d+\s*\))(\s+(?:simpleGrading|edgeGrading)\s*(?:\$[a-zA-Z0-9_]+|\([^;]+;|\([^\)]+\)))",
        re.MULTILINE
    )

    all_blocks = block_regex.findall(blocks_text)
    if not all_blocks:
        print("No valid hex blocks found inside the blocks section.")
        return

    print(f"--- Found {len(all_blocks)} blocks inside your blockMeshDict ---\n")
    print("Select input mode:")
    print("  1) Interactive Terminal mode")
    print("  2) Text file mode (reads 'mesh_config.txt')")
    
    mode = input("Select mode (1 or 2): ").strip()
    config_data = {}
    
    if mode == "2":
        config_path = input("Enter config file path (default: mesh_config.txt): ").strip() or "mesh_config.txt"
        config_data = parse_config_file(config_path)
        if config_data is None:
            return

    # Create a list to store rebuilt individual blocks
    rebuilt_blocks = []

    # Get raw individual block blocks before replacement to map them cleanly
    raw_block_strings = [m.group(0) for m in block_regex.finditer(blocks_text)]

    for i, (hex_part, cells_part, grading_part) in enumerate(all_blocks):
        updated_cells = cells_part
        updated_grading = grading_part

        if mode == "2":
            # Text file mode
            if i in config_data:
                updated_cells = f" {config_data[i]['cells']}"
                g_type = config_data[i]["grad_type"]
                g_val = config_data[i]["grad_val"]
                
                if "simple" in g_type:
                    updated_grading = f"\n    simpleGrading ({g_val})" if not g_val.startswith("$") and not g_val.startswith("(") else f"\n    simpleGrading {g_val}"
                else:
                    updated_grading = f"\n    edgeGrading ({g_val})"
                print(f"Block {i}: Applied file configuration successfully.")
            else:
                print(f"Block {i}: No file configuration found. Keeping original parameters.")
        else:
            # Interactive mode
            print(f"Block {i}:")
            print(f"  Vertices: {hex_part.strip()}")
            print(f"  Current Cells: {cells_part.strip()}")
            print(f"  Current Grading: {grading_part.strip()}")
            
            # Update cells
            change_cells = input(f"Modify cells for Block {i}? (y/N): ").strip().lower()
            if change_cells == 'y':
                nx = input("  Enter new X cells: ")
                ny = input("  Enter new Y cells: ")
                nz = input("  Enter new Z cells: ")
                if nx and ny and nz:
                    updated_cells = f" ({nx} {ny} {nz})"

            # Update grading
            change_grading = input(f"Modify grading for Block {i}? (y/N): ").strip().lower()
            if change_grading == 'y':
                grading_type = input("  Select type (1 = simpleGrading, 2 = edgeGrading): ").strip()
                if grading_type == "1":
                    g_val = input("  Enter simpleGrading parameters: ").strip()
                    if g_val:
                        updated_grading = f"\n    simpleGrading ({g_val})" if not g_val.startswith("$") and not g_val.startswith("(") else f"\n    simpleGrading {g_val}"
                elif grading_type == "2":
                    g_val = input("  Enter 12 edge parameters separated by spaces: ").strip()
                    if g_val:
                        updated_grading = f"\n    edgeGrading ({g_val})"
            print("-" * 40)

        # Assemble new string for this block only
        new_block_str = f"    {hex_part.strip()}\n    {updated_cells.strip()}\n   {updated_grading}"
        rebuilt_blocks.append(new_block_str)

    # Step 3: Reconstruct the new blocks block and cleanly overwrite the old string
    new_blocks_text = "\n\n".join(rebuilt_blocks)
    updated_content = content.replace(blocks_match.group(0), header + new_blocks_text + footer)

    # Backup the original file
    backup_path = dict_path + ".bak"
    with open(backup_path, 'w') as f:
        f.write(content)

    # Write the clean text out
    with open(dict_path, 'w') as f:
        f.write(updated_content)

    print(f"\nSuccessfully updated {dict_path} cleanly!")

if __name__ == "__main__":
    modify_generic_blockmesh()