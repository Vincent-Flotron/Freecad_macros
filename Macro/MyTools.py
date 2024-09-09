# import FreeCAD as App
import FreeCAD     as     App
import FreeCADGui  as     Gui
from   fractions   import Fraction
from   collections import deque
from   PySide      import QtGui


# Settings
default_techdraw_template_path = "/home/spot/freecad/A4_LandscapeTD.svg"
param_group_name_techdraw      = "User parameter:BaseApp/Preferences/TechDraw"
setting_key_techdraw           = "techdraw_template_path"


class Settings:

    def save_setting(param_group_name=param_group_name_techdraw, key=setting_key_techdraw, value=None):
        """Save the given setting using FreeCAD's internal parameter system."""
        if value is not None:
            # Save the value under the given key in FreeCAD's settings
            App.ParamGet(param_group_name).SetString(key, value)
            QtGui.QMessageBox.information(None, "Save Setting", f"Setting '{key}' saved with value: {value}")
        else:
            QtGui.QMessageBox.warning(None, "Save Setting", f"No value provided for setting '{key}'.")

    def load_setting(param_group_name=param_group_name_techdraw, key=setting_key_techdraw, default_val=None):
        """Load the setting from FreeCAD's internal parameter system, or return the default if not found."""
        # Retrieve the value from FreeCAD's settings, or use the default if not present
        value = App.ParamGet(param_group_name).GetString(key, default_val)
        return value

    def edit_setting(param_group_name=param_group_name_techdraw, key=setting_key_techdraw):
        val         = Settings.load_setting(param_group_name=param_group_name, key=key)
        new_val, ok = QtGui.QInputDialog.getText(None, "Edit Setting", f"Actual value:\nSetting: '{key}' = '{val}'\nEnter a new Value:")
        if ok:
            Settings.save_setting(param_group_name=param_group_name, key=key, value=new_val)


def new_techdraw_page(techdraw_template_path=None):
    # Create a new page number based on the last existing page
    doc = App.activeDocument()

    # Find the highest page number
    max_page_num = get_highest_page_number(doc)

    # Increment the page number for the new page
    new_page_num = max_page_num + 1
    page_nb      = f"{new_page_num:03}"

    # Create new page and template names
    page_name     = f'Page{page_nb}'
    template_name = f'Template{page_nb}'

    # Create a new page and template in the document
    new_page = doc.addObject( 'TechDraw::DrawPage',        page_name     )
    template = doc.addObject( 'TechDraw::DrawSVGTemplate', template_name )

    # Assign the template to the page
    setting_techdraw_template_path = "techdraw_template_path"
    new_techdraw_template_path     = ""
    if not techdraw_template_path:
        techdraw_template_path = Settings.load_setting(default_val=setting_techdraw_template_path)
    try:
        template.Template = techdraw_template_path
    except:
        new_techdraw_template_path, ok = QtGui.QInputDialog.getText(None, "Set new path for the template", f"The actual path for the TechDraw template:\n'{techdraw_template_path}'\nis not valid.\n\nPlease, select a new path.")
        template.Template = new_techdraw_template_path
    
    new_page.Template = template

    # Save the new TechDraw template setting
    if new_techdraw_template_path:
        Settings.save_setting(key=setting_techdraw_template_path, value=new_techdraw_template_path)

    # Recompute the document to apply changes
    doc.recompute()
    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(App.ActiveDocument.Label, page_name)

    # Update all page numbers
    field_sheet_name     = 'FC-SH'
    last_page_number     = new_page_num
    field_drawing_numb   = "Drawing_number"
    initial_drawing_numb = "V1"
    # doc                  = App.activeDocument()
    for obj in doc.Objects:
        page = obj
        if obj_is_a_page(page):
            page_num = get_page_number_of_DrawPage(page)
            value    = f"{page_num}/{last_page_number}"
            set_editable_texts_of_a_page(page, field_sheet_name, value)
            set_editable_texts_of_a_page(page, field_drawing_numb, initial_drawing_numb)

    doc.recompute()
    Gui.SendMsgToActiveView("ViewFit")

    return doc, new_page


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
            QtGui.QMessageBox.warning(None, "Error getting Page of DrawProjGroupItem", "Parent page not found.")
    else:
        QtGui.QMessageBox.warning(None, "Error getting Page of DrawProjGroupItem", "Please select a valid object.")


# def find_body_parent(obj, depth=0, max_depth=3):
#     """
#     Recursively search for the PartDesign::Body parent of an object with a depth limit.
#     """
#     if obj is None or depth > max_depth:
#         return None
#     if obj.TypeId == 'PartDesign::Body':
#         return obj
#     return find_body_parent(obj.getParentGeoFeature(), depth + 1, max_depth)

def find_body_parent(obj, depth=0, max_depth=3):
    """
    Recursively search for the PartDesign::Body parent of an object with a depth limit.
    """
    if obj is None or depth > max_depth:
        return None
    
    # Check if the current object is of type 'PartDesign::Body'
    if obj.TypeId == 'PartDesign::Body':
        return obj

    # Check if the object has parents using the InListRecursive attribute
    if len(obj.InListRecursive) > 0:
        parent_obj = obj.InListRecursive[0]  # Get the first parent in the list
        return find_body_parent(parent_obj, depth + 1, max_depth)
    
    return None



def get_Page_of_DrawProjGroup(selected_objects):
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
            QtGui.QMessageBox.warning(None, "Error getting Page of DrawProjGroup", "Parent Page not found.")
    else:
        QtGui.QMessageBox.warning(None, "Error getting Page of DrawProjGroup", "Please select a valid object.")


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
        if parent_obj and parent_obj.TypeId == 'TechDraw::DrawProjGroup':
            return parent_obj
        else:
            QtGui.QMessageBox.warning(None, "Error getting DrawProjGroup of a DrawProjGroupItem", "Parent TechDraw::DrawProjGroup not found.")

    else:
        QtGui.QMessageBox.warning(None, "Error getting DrawProjGroup of a DrawProjGroupItem", "Please select a valid TechDraw::DrawProjGroupItem object.")

def is_DrawProjGroup(selected_object):
    return selected_object.TypeId == 'TechDraw::DrawProjGroup'

# The rotate function that applies the selected view
def rotate_projgroup(selection=None, view='FrontBottomLeft'):
    # Define standard view directions and their corresponding XDirections
    views = {
        'FrontBottomLeft': {
            'Direction': (-1, -1, 1),
            'XDirection': (1, 0, 0)
        },
        'FrontBottomRight': {
            'Direction': (1, -1, 1),
            'XDirection': (0, 1, 0)
        },
        'FrontTopRight': {
            'Direction': (1, 1, 1),
            'XDirection': (-1, 0, 0)
        },
        'FrontTopLeft': {
            'Direction': (-1, 1, 1),
            'XDirection': (0, -1, 0)
        }
    }

    rotation_angle = 30  #deg

    # If no selection provided, get the current selection from the GUI
    if selection is None:
        selection = Gui.Selection.getSelection()

    # Check if the selection is not empty
    if not selection:
        QtGui.QMessageBox.warning(None, "Selection Error", "No object selected. Please select a DrawProjGroup item.")
        return

    # Grab the first selected object
    selected_obj = selection[0]

    # Check if the selected object is of type 'TechDraw::DrawProjGroup'
    if selected_obj.TypeId != 'TechDraw::DrawProjGroup':
        QtGui.QMessageBox.warning(None, "Selection Error", "Selected object is not a TechDraw::DrawProjGroup.")
        return

    # Check if the specified view exists
    if view not in views:
        QtGui.QMessageBox.warning(None, "View Error", f"View '{view}' is not recognized. Valid views are: {list(views.keys())}")
        return

    # Set the view direction and corresponding XDirection based on the selected view
    view_direction  = views[view]['Direction']
    view_xdirection = views[view]['XDirection']

    # Iterate through items in the projection group and set the view direction and XDirection
    for view_item in selected_obj.OutList:
        # Check if the view_item has the 'Direction' and 'XDirection' attributes (i.e., it's a valid projection view)
        if hasattr(view_item, 'Direction') and hasattr(view_item, 'XDirection'):
            view_item.Direction  = App.Vector(view_direction)
            view_item.XDirection = App.Vector(view_xdirection)
            view_item.Rotation   = rotation_angle
        else:
            # If the item does not support 'Direction' or 'XDirection', skip it
            # QtGui.QMessageBox.information(None, "Information", f"Skipping item: {view_item.Name}, does not support 'Direction' or 'XDirection'.")
            pass

    # Update the document to reflect changes
    try:
        App.ActiveDocument.recompute()
        # print(f"Projection group rotated to view: {view}")
    except Exception as e:
        QtGui.QMessageBox.warning(None, "Error rotating ProjGroup", f"Recompute failed: {e}")

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
                QtGui.QMessageBox.warning(None, "Error setting editable text of a page", f"{editable_text_name} field not found in the template.")
        else:
            QtGui.QMessageBox.warning(None, "Error setting editable text of a page", "No template assigned to the selected page.")
    else:
        QtGui.QMessageBox.warning(None, "Error setting editable text of a page", "Please select a valid TechDraw::DrawPage.")



def get_ProjGroup_number(obj):
    """
    Parameter:
        obj = 'TechDraw::ProjGroup'
    Returns 0 by default.
    """
    if obj.TypeId == 'TechDraw::ProjGroup':
        try:
            # Extract the number from the page name
            ProjGroup_num = int(obj.Name.replace('ProjGroup', ''))
        except ValueError:
            pass
    return ProjGroup_num

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
                        part_name_until_sep = obj.Source[0].InListRecursive[0].Label.split(sep)[0]
                    # TechDraw::DrawProjGroupItem was made from selected body's subf-function (like 'Pocket026')
                    else:
                        part_name_until_sep = obj.Source[0].Label.split(sep)[0]
                    return part_name_until_sep
                except Exception as e:
                    QtGui.QMessageBox.warning(None, "Error getting partname of DrawProjGroupItem", f"Could not access Source or Label: {e}")
            else:
                QtGui.QMessageBox.warning(None, "Error getting partname of DrawProjGroupItem", f"Object {obj.Name} is not a TechDraw::DrawProjGroupItem.")
    else:
        QtGui.QMessageBox.warning(None, "Error getting partname of DrawProjGroupItem", "No object selected.")


def decimal_to_fraction(decimal):
    fraction = Fraction(decimal).limit_denominator()
    return fraction

# def name_draw(selected_objs):
def name_draw(page, selected_objs):
    part_name  = get_partname_of_DrawProjGroupItem( selected_objs )

    field_name = "Subtitle"
    set_editable_texts_of_a_page(page, field_name, part_name)


def set_draw_cartridge_scale(page, group):
    field_name       = "FC-SC"
    scale_fractional = decimal_to_fraction(group.Scale)
    set_editable_texts_of_a_page(page, field_name, scale_fractional)

def fraction_to_decimal(fraction_str):
    # Remove spaces from the fraction string
    fraction_str = fraction_str.replace(" ", "")
    
    # Now convert to Fraction and then to float
    decimal = float(Fraction(fraction_str))
    
    return decimal

def get_highest_page_number(doc):
    max_page_num = 0
    for obj in doc.Objects:
        # Extract the number from the page name
        page_num = get_page_number_of_DrawPage(obj)
        if page_num > max_page_num:
            max_page_num = page_num
    return max_page_num
    
def get_highest_ProjGroup_number(doc):
    max_ProjGroup_num = 0
    for obj in doc.Objects:
        # Extract the number from the page name
        page_num = get_page_number_of_DrawPage(obj)
        if page_num > max_ProjGroup_num:
            max_ProjGroup_num = page_num
    return max_ProjGroup_num

def lock_objects(selected_objects):
    # Check if at least one object is selected
    if selected_objects:
        for obj in selected_objects:
            # Check if the object has a 'Source' attribute
            if obj.isDerivedFrom("TechDraw::DrawProjGroupItem"):
                obj.LockPosition = not obj.LockPosition
            else:
                QtGui.QMessageBox.warning(None, "Bad Selection", f"Selected object must be a TechDraw::DrawProjGroupItem.\n Actually is type: '{obj.TypeId}'")
    else:
        QtGui.QMessageBox.warning(None, "No Selection", "Please select one or more object(s) first.")


def get_value_from_spreadsheet_alias(doc, alias = 'Scale', spreadsheet_name = 'Spreadsheet'):
    # spr = App.getDocument('Maison2').getObject('Spreadsheet')
    spr = doc.getObject(spreadsheet_name)
    aliasValue = spr.getCellFromAlias(alias)
    pref_scale = spr.getContents(aliasValue).split('=')
    if len(pref_scale) > 1:
        pref_scale = spr.getContents(aliasValue).split('=')[1]
    else:
        pref_scale = spr.getContents(aliasValue).split('=')[0]
    return pref_scale

def get_prefered_scale_deci_and_type(key="techdraw_prefered_scale"):
    pref_scale = Settings.load_setting(key, default_val='1/10')
    scale_deci = None
    scale_type = 1 # Automatic
    if pref_scale and pref_scale != 'Automatique' and pref_scale != '':
        scale_type = 2 # Custom
        scale_deci = fraction_to_decimal(pref_scale)
    return scale_deci, scale_type

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