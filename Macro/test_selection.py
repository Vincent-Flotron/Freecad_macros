# import FreeCAD
# import FreeCADGui

# Get the current selection
selection = Gui.Selection.getSelection()

# Check if anything is selected
if selection:
    # Loop through selected items (there might be more than one)
    for sel in selection:
        # Check if any face is selected
        try:
            # Get the selected faces
            selected_faces = sel.SubObjects
            for face in selected_faces:
                print(f"Selected face: {face}")

            # Optional: Print the names of the selected sub-shapes (faces)
            for subname in sel.SubElementNames:
                print(f"Selected sub-element name: {subname}")

        except Exception as ex:
            print(f'{ex}')
else:
    print("Nothing selected.")
