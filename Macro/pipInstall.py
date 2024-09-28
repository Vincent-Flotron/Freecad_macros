from PySide2 import QtWidgets
import os
import sys
mod_to_import = 'MyTools'
if mod_to_import in sys.modules:
    del sys.modules[mod_to_import]
import MyTools

def ask_for_packages():
    # Create an input dialog
    dialog = QtWidgets.QInputDialog()
    dialog.setWindowTitle("Enter Packages")
    dialog.setLabelText("Please enter the names of the pip packages to install (separated by spaces):")
    dialog.setTextValue("")

    # Show the dialog and wait for user input
    if dialog.exec_():
        return dialog.textValue().strip()  # Return the entered packages, stripping unnecessary spaces
    else:
        return None


def generate_install_script(packages):
    if packages:
        script_content = f"""#!/bin/bash
# This script will install the specified pip packages using snap
snap run freecad.pip install {packages}
"""
        script_path = os.path.expanduser("~/install_packages.sh")
        with open(script_path, "w") as script_file:
            script_file.write(script_content)

        os.chmod(script_path, 0o755)  # Make the script executable

        # Show a message box with the success message
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle("Script Generated")
        message_box.setText(f"A script has been generated at {script_path}.\nPlease run this script manually with the necessary permissions.")
        message_box.setIcon(QtWidgets.QMessageBox.Information)
        message_box.exec_()

        # Open the folder in the default file browser
        MyTools.open_file_browser(script_path)
    else:
        # Show a message box if no packages were entered
        message_box = QtWidgets.QMessageBox()
        message_box.setWindowTitle("No Packages Specified")
        message_box.setText("No packages were specified for installation.")
        message_box.setIcon(QtWidgets.QMessageBox.Warning)
        message_box.exec_()

# Ask the user for the packages to install
packages = ask_for_packages()

# Generate the installation script
if packages is not None:
    generate_install_script(packages)
else:
    # Show a message box if the user canceled the input
    message_box = QtWidgets.QMessageBox()
    message_box.setWindowTitle("Action Canceled")
    message_box.setText("Package input was canceled. No script was generated.")
    message_box.setIcon(QtWidgets.QMessageBox.Information)
    message_box.exec_()
