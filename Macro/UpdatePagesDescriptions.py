# import FreeCAD
import sys
mod_to_import = 'MyTools'
if mod_to_import in sys.modules:
    del sys.modules[mod_to_import]
import MyTools

MyTools.set_editable_texts_of_a_page
MyTools.obj_is_a_page
def set_label2_from_draw_subtitle():
    doc = App.ActiveDocument
    
    for obj in doc.Objects:
        if MyTools.obj_is_a_page(obj):
            subtitle = MyTools.get_editable_text_of_a_page(obj, "Subtitle")
            obj.Label2 = subtitle
    
    doc.recompute()

if __name__ == "__main__":
    set_label2_from_draw_subtitle()
