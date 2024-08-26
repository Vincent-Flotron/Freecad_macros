import FreeCAD as App
import FreeCADGui as Gui
import logging
import os
from tkinter import messagebox
from collections import deque

# Show an information message
messagebox.showinfo("Information", "This is an information message.")

# Set up logging
log_file_path = os.path.expanduser('/home/spot/.local/share/FreeCAD/Mod/log.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Log the initialization of the script
logging.info("InitGui.py script has started.")


class DocumentObserver:
    def __init__(self, loggin, max_length=2):
        self.logging = logging
        self.queue = deque(maxlen=max_length)

    def example(self):
        self.run_macro()
        self.queue.append(signal)

    def slotCreatedDocument(self, doc):
        """This is triggered when a new document is created."""
        self.logging.info(f"slotCreatedDocument {doc.Label}")

    def slotDeletedDocument(self, doc):
        self.logging.info(f"slotDeletedDocument {doc.Label}")


    def slotRelabelDocument(self, doc):
        self.logging.info(f"slotRelabelDocument {doc.Label}")

    def slotActivateDocument(self, doc):
        self.logging.info(f"slotActivateDocument {doc.Label}")

    def slotRecomputedDocument(self, doc):
        self.logging.info(f"slotRecomputedDocument {doc.Label}")

    def slotUndoDocument(self, doc):
        self.logging.info(f"slotUndoDocument {doc.Label}")

    def slotRedoDocument(self, doc):
        self.logging.info(f"slotRedoDocument {doc.Label}")

    def slotOpenTransaction(self, doc, name):
        self.logging.info(f"slotOpenTransaction {doc.Label}")

    def slotCommitTransaction(self, doc):
        self.logging.info(f"slotCommitTransaction {doc.Label}")

    def slotAbortTransaction(self, doc):
        self.logging.info(f"slotAbortTransaction {doc.Label}")

    def slotBeforeChangeDocument(self, doc, prop):
        self.logging.info(f"slotBeforeChangeDocument {doc.Label}")

    def slotChangedDocument(self, doc, prop):
        self.logging.info(f"slotChangedDocument {doc.Label}")

    def slotCreatedObject(self, obj):
        self.logging.info(f"slotCreatedObject {obj.Label}")

    def slotDeletedObject(self, obj):
        self.logging.info(f"slotDeletedObject {obj.Label}")

    def slotChangedObject(self, obj, prop):
        self.logging.info(f"slotChangedObject {obj.Label}")

    def slotBeforeChangeObject(self, obj, prop):
        self.logging.info(f"slotBeforeChangeObject {obj.Label}")

    def slotRecomputedObject(self, obj):
        self.logging.info(f"slotRecomputedObject {obj.Label}")
        self.signal.append("slotRecomputedObject")
        if obj.TypeId == 'TechDraw::DrawProjGroup':
            self.logging.info(f"scale {obj.Scale}")
            self.signal.append("slotRecomputedObject:scale")

    def slotAppendDynamicProperty(self, obj, prop):
        self.logging.info(f"slotAppendDynamicProperty {obj.Label}")

    def slotRemoveDynamicProperty(self, obj, prop):
        self.logging.info(f"slotRemoveDynamicProperty {obj.Label}")

    def slotChangePropertyEditor(self, obj, prop):
        self.logging.info(f"slotChangePropertyEditor {obj.Label}")

    def slotStartSaveDocument(self, obj, name):
        self.logging.info(f"slotStartSaveDocument {obj.Label}")

    def slotFinishSaveDocument(self, obj, name):
        self.logging.info(f"slotFinishSaveDocument {obj.Label}")

    def slotBeforeAddingDynamicExtension(self, obj, extension):
        self.logging.info(f"slotBeforeAddingDynamicExtension {obj.Label}")

    def slotAddedDynamicExtension(self, obj, extension):
        self.logging.info(f"slotAddedDynamicExtension {obj.Label}")


    def run_macro(self):
        self.logging.info("Running the macro...")
        App.Console.PrintMessage("This message is from the macro executed after the document is opened.\n")
        # Example of additional log entry during macro execution
        self.logging.info("Macro execution is complete.")

# Create an instance of the observer
doc_observer = DocumentObserver(logging)

# Add the observer to FreeCAD
App.addDocumentObserver(doc_observer)
logging.info("DocumentObserver has been added to FreeCAD.")
