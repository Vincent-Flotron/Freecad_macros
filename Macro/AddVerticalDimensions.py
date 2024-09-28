import FreeCADGui as Gui


def add_vertical_dimension_to_selected_vertices():
    # Retrieve the current selection, including sub-objects
    selectionEx = Gui.Selection.getSelectionEx()[0]

    # Display the object name
    # print("Object Name:", selectionEx.ObjectName)
    doc      = App.ActiveDocument
    sel_item = selectionEx.ObjectName

    vertex_lst = []

    # Loop through sub-elements (like vertices)
    for subName in selectionEx.SubElementNames:
        if subName.startswith('Vertex'):
            vertex_lst.append(subName)
            # print(f'sub: {subName}')
        
    print(f'vertex_lst: {vertex_lst}')
    Gui.Selection.clearSelection()

    for i in range(1, len(vertex_lst)):
        # Focus on the vertex and execute the command for vertical dimension
        Gui.Selection.addSelection(doc.Name, sel_item, vertex_lst[0])
        Gui.Selection.addSelection(doc.Name, sel_item, vertex_lst[i])
        Gui.runCommand('TechDraw_VerticalDimension',0)
        Gui.Selection.clearSelection()


if __name__ == '__main__':
    # Run the function
    add_vertical_dimension_to_selected_vertices()
