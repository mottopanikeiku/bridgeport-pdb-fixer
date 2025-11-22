import sys
import os

def fix_pdb_minimal(input_path, output_path):
    # Standard Mapping for Amber Lipid17
    replacements = {
        "POP ": "POPC",  
        "CHL ": "CHL1",  
    }

    renamed_count = 0
    
    with open(input_path, 'r') as infile, open(output_path, 'w') as outfile:
        for line in infile:
            # Only look at ATOM lines
            if line.startswith("ATOM") or line.startswith("HETATM"):
                # Extract the 3-letter name from columns 17-20
                current_res = line[17:21]
                
                if current_res in replacements:
                    # Swap the name
                    new_res = replacements[current_res]
                    line = line[:17] + new_res + line[21:]
                    renamed_count += 1
            
            outfile.write(line)

    print(f"Processed {input_path}. Renamed {renamed_count} atoms.")
    print(f"Saved to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python fix.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    # Create output filename: input_fixed.pdb
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_fixed{ext}"

    try:
        fix_pdb_minimal(input_file, output_file)
        print("Success.")
    except FileNotFoundError:
        print("Error: Could not find the input file.")