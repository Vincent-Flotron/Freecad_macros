import FreeCAD as App
import FreeCADGui as Gui
import logging
import sys
import os


# from tkinter import messagebox

# Show an information message
# messagebox.showinfo("Information", "This is an information message.")

# Set up logging
log_file_path = os.path.expanduser('/home/spot/.local/share/FreeCAD/Mod/log.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Log the initialization of the script
logging.info("InitGui.py script has started.")


class DocumentObserver:
    # from collections import deque

    def __init__(self, logging, max_length=2):
        import MyTools
        self.mytools       = MyTools
        self.logging       = logging
        self.deque_max_len = max_length
        self.signal        = self.mytools.deque(maxlen=max_length)
        self.last_object   = None


    def example(self):
        self.run_macro()
        self.signal.append("test")

    def slotCreatedDocument(self, doc):
        """This is triggered when a new document is created."""
        self.logging.info(f"slotCreatedDocument {doc.Label}")
        self.signal.append("slotCreatedDocument")

    def slotDeletedDocument(self, doc):
        self.logging.info(f"slotDeletedDocument {doc.Label}")
        self.signal.append("slotDeletedDocument")

    def slotRelabelDocument(self, doc):
        self.logging.info(f"slotRelabelDocument {doc.Label}")
        self.signal.append("slotRelabelDocument")

    def slotActivateDocument(self, doc):
        self.logging.info(f"slotActivateDocument {doc.Label}")
        self.signal.append("slotActivateDocument")

    def slotRecomputedDocument(self, doc):
        self.logging.info(f"slotRecomputedDocument {doc.Label}")
        self.signal.append("slotRecomputedDocument")

    def slotUndoDocument(self, doc):
        self.logging.info(f"slotUndoDocument {doc.Label}")
        self.signal.append("slotUndoDocument")

    def slotRedoDocument(self, doc):
        self.logging.info(f"slotRedoDocument {doc.Label}")
        self.signal.append("slotRedoDocument")

    def slotOpenTransaction(self, doc, name):
        self.logging.info(f"slotOpenTransaction {doc.Label}")
        self.signal.append("slotOpenTransaction")

    def slotCommitTransaction(self, doc):
        self.logging.info(f"slotCommitTransaction {doc.Label}")
        self.signal.append("slotCommitTransaction")

    def slotAbortTransaction(self, doc):
        self.logging.info(f"slotAbortTransaction {doc.Label}")
        self.signal.append("slotAbortTransaction")

    def slotBeforeChangeDocument(self, doc, prop):
        self.logging.info(f"slotBeforeChangeDocument {doc.Label}")
        self.signal.append("slotBeforeChangeDocument")

    def slotChangedDocument(self, doc, prop):
        self.logging.info(f"slotChangedDocument {doc.Label}")
        self.signal.append("slotChangedDocument")

    def slotCreatedObject(self, obj):
        self.logging.info(f"slotCreatedObject {obj.Label}")
        self.signal.append("slotCreatedObject")

    def slotDeletedObject(self, obj):
        self.logging.info(f"slotDeletedObject {obj.Label}")
        self.signal.append("slotDeletedObject")

    def slotChangedObject(self, obj, prop):
        self.logging.info(f"slotChangedObject {obj.Label}")
        self.signal.append("slotChangedObject")

    def slotBeforeChangeObject(self, obj, prop):
        self.logging.info(f"slotBeforeChangeObject {obj.Label}")
        self.signal.append("slotBeforeChangeObject")

    def slotRecomputedObject(self, obj):
        self.logging.info(f"slotRecomputedObject {obj.Label}")
        self.signal.append("slotRecomputedObject")
        if obj.TypeId == 'TechDraw::DrawProjGroup':
            self.logging.info(f"scale {obj.Scale}")
            self.signal.append(f"slotRecomputedObject:{obj.Label}")
            self.last_object = obj
        elif self.check_deque_content(self.signal):
            self.trigger_scale_as_changed(self.last_object)
        self.logging.info(f"signal {self.signal}")

    def slotAppendDynamicProperty(self, obj, prop):
        self.logging.info(f"slotAppendDynamicProperty {obj.Label}")
        self.signal.append("slotAppendDynamicProperty")

    def slotRemoveDynamicProperty(self, obj, prop):
        self.logging.info(f"slotRemoveDynamicProperty {obj.Label}")
        self.signal.append("slotRemoveDynamicProperty")

    def slotChangePropertyEditor(self, obj, prop):
        self.logging.info(f"slotChangePropertyEditor {obj.Label}")
        self.signal.append("slotChangePropertyEditor")

    def slotStartSaveDocument(self, obj, name):
        self.logging.info(f"slotStartSaveDocument {obj.Label}")
        self.signal.append("slotStartSaveDocument")

    def slotFinishSaveDocument(self, obj, name):
        self.logging.info(f"slotFinishSaveDocument {obj.Label}")
        self.signal.append("slotFinishSaveDocument")

    def slotBeforeAddingDynamicExtension(self, obj, extension):
        self.logging.info(f"slotBeforeAddingDynamicExtension {obj.Label}")
        self.signal.append("slotBeforeAddingDynamicExtension")

    def slotAddedDynamicExtension(self, obj, extension):
        self.logging.info(f"slotAddedDynamicExtension {obj.Label}")
        self.signal.append("slotAddedDynamicExtension")


    def trigger_scale_as_changed(self, itemGroupObject):
        self.logging.info(f"trigger_scale_as_changed {itemGroupObject.Label}")


    def check_deque_content(self, d):
        expected = self.mytools.deque(['slotRecomputedObject:scale', 'slotRecomputedObject'], self.deque_max_len)
        self.logging.info(f"check_deque_content. d '{d}'\n" + " "*33 + f"check_deque_content. e '{expected}'")
        return d == expected

    def run_macro(self):
        self.logging.info("Running the macro...")
        App.Console.PrintMessage("This message is from the macro executed after the document is opened.\n")
        # Example of additional log entry during macro execution
        self.logging.info("Macro execution is complete.")


# user_dir = FreeCAD.getUserAppDataDir()

# Create an instance of the observer
doc_observer = DocumentObserver(logging)

# Add the observer to FreeCAD
App.addDocumentObserver(doc_observer)
logging.info("DocumentObserver has been added to FreeCAD.")
