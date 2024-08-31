# import FreeCAD as App
import FreeCAD as App
from fractions import Fraction
from collections import deque

def get_page_of_DrawProjGroupItem(selected_objects):
    """
    Parameter:
        selected_objects = Gui.Selection.getSelection()
    """
    selected_obj = selected_objects[0] if selected_objects else None
    parent_obj   = None

    if selected_obj:
        # Traverse up the hierarchy to find the parent page
        if len(selected_obj.InListRecursive) > 1:
            parent_obj = selected_obj.InListRecursive[1]
            
        if parent_obj and parent_obj.TypeId == 'TechDraw::DrawPage':
            return parent_obj
        else:
            print("Parent page not found.")
    else:
        print("Please select a valid object.")


def get_Page_of_DrawProjGroupItem(selected_objects):
    """
    Parameter:
        selected_objects = Gui.Selection.getSelection()
    """
    selected_obj = selected_objects[0] if selected_objects else None
    parent_obj   = None

    if selected_obj:
        # Traverse up the hierarchy to find the parent Page
        if len(selected_obj.InListRecursive) > 0:
            parent_obj = selected_obj.InListRecursive[0]
            
        if parent_obj and parent_obj.TypeId == 'TechDraw::DrawPage':
            return parent_obj
        else:
            print("Parent Page not found.")
    else:
        print("Please select a valid object.")


def get_DrawProjGroup_of_DrawProjGroupItem(selected_objects):
    """
    Parameter:
        selected_objects = Gui.Selection.getSelection()
    """
    selected_obj = selected_objects[0] if selected_objects else None
    parent_obj   = None

    if selected_obj:
        # Traverse up the hierarchy to find the parent DrawProjGroup
        if len(selected_obj.InListRecursive) > 0:
            parent_obj = selected_obj.InListRecursive[0]
            
        print(f"get_DrawProjGroup_of_DrawProjGroupItem : {selected_obj.InListRecursive}")
        print(f"parent_obj.TypeId                      : {parent_obj.TypeId}")
        if parent_obj and parent_obj.TypeId == 'TechDraw::DrawProjGroup':
            return parent_obj
        else:
            print("Parent TechDraw::DrawProjGroup not found.")
    else:
        print("Please select a valid object.")

def is_DrawProjGroup(selected_object):
    return selected_object == 'TechDraw::DrawProjGroup'

def set_editable_texts_of_a_page(selected_obj, editable_text_name, value):
    """
    Parameter:
        selected_object    = 'TechDraw::DrawPage'
        editable_text_name = "Subtitle"
        value              = "New value here :)"
    """
    # selected_obj = selected_objects[0] if selected_objects else None

    if selected_obj and selected_obj.TypeId == 'TechDraw::DrawPage':
        # Access the template associated with the selected page
        template = selected_obj.Template

        if template:
            # Access the editable text fields of the template
            editable_texts = template.EditableTexts
            
            # Check if editable_text_name exists in the editable fields
            if editable_text_name in editable_texts:
                # Update the editable_text_name field value
                editable_texts[editable_text_name] = str(value)
                template.EditableTexts = editable_texts
                
                # Recompute the document to apply changes
                App.activeDocument().recompute()
            else:
                print(f"{editable_text_name} field not found in the template.")
        else:
            print("No template assigned to the selected page.")
    else:
        print("Please select a valid TechDraw::DrawPage.")


def get_page_number_of_DrawPage(obj):
    """
    Parameter:
        obj = 'TechDraw::DrawPage'
    Returns 0 by default.
    """
    page_num = 0
    if obj.TypeId == 'TechDraw::DrawPage':
        try:
            # Extract the number from the page name
            page_num = int(obj.Name.replace('Page', ''))
        except ValueError:
            pass
    return page_num

def obj_is_a_page(obj):
    return obj.TypeId == 'TechDraw::DrawPage'

def get_partname_of_DrawProjGroupItem(selected_objects, sep = '_'):
    """
    Parameter:
        selected_objects = Gui.Selection.getSelection()
    """
    part_name_until_sep = None
    # Check if at least one object is selected
    if selected_objects:
        for obj in selected_objects:
            # Check if the object is of type 'TechDraw::DrawProjGroupItem'
            if obj.TypeId == 'TechDraw::DrawProjGroupItem':
                # Get part name until underscore by safely access Source and Label
                try:
                    # TechDraw::DrawProjGroupItem was made from selected body
                    if obj.Source[0].TypeId != "PartDesign::Body":
                        print(f'obj.Source[0].InListRecursive[0]: {obj.Source[0].InListRecursive[0].TypeId}')
                        part_name_until_sep = obj.Source[0].InListRecursive[0].Label.split(sep)[0]
                    # TechDraw::DrawProjGroupItem was made from selected body's subf-function (like 'Pocket026')
                    else:
                        part_name_until_sep = obj.Source[0].Label.split(sep)[0]
                    return part_name_until_sep
                except Exception as e:
                    print(f"Could not access Source or Label: {e}")
            else:
                print(f"Object {obj.Name} is not a TechDraw::DrawProjGroupItem.")
    else:
        print("No object selected.")


def decimal_to_fraction(decimal):
    fraction = Fraction(decimal).limit_denominator()
    return fraction

def get_highest_page_number():
    # Find the highest page number
    doc = App.activeDocument()
    max_page_num = 0
    for obj in doc.Objects:
        # Extract the number from the page name
        page_num = get_page_number_of_DrawPage(obj)
        if page_num > max_page_num:
            max_page_num = page_num
    return max_page_num

class myQueue(deque):
    pass

if __name__ == "__main__":
    import FreeCADGui as Gui

    # Get the selected object
    selected_obj = Gui.Selection.getSelection()
    
    page      = get_page_of_DrawProjGroupItem(     selected_obj )
    part_name = get_partname_of_DrawProjGroupItem( selected_obj )
    page_number = get_page_number_of_DrawPage(     page         )

    print( f"Part Name   : { part_name  }" )
    print( f"Parent Page : { page.Name  }" )
    print( f"page_number : { page_number}" )

    set_editable_texts_of_a_page(page, "Subtitle", part_name)