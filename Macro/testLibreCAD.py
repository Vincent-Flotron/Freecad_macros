import subprocess

# Path to the LibreCAD executable
librecad_path = "/usr/bin/librecad"  # Adjust this path if necessary

# Path to the DXF file
dxf_file_path = "/home/wace/Documents/git/Stairs/dxf/LimonRez1ereVoleeBasGauche.dxf"

# Construct the command to open the file with LibreCAD
command = [librecad_path, dxf_file_path]

# Execute the command
try:
    subprocess.run(command, check=True)
    print(f"Successfully opened {dxf_file_path} with LibreCAD")
except subprocess.CalledProcessError as e:
    print(f"Error opening file: {e}")
except FileNotFoundError:
    print("LibreCAD executable not found. Please check the path.")
