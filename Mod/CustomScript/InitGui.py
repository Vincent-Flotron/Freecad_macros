import FreeCAD as App
import FreeCADGui as Gui
import logging
import os
from tkinter import messagebox

# Show an information message
messagebox.showinfo("Information", "This is an information message.")

# Set up logging
log_file_path = os.path.expanduser('/home/spot/.local/share/FreeCAD/Mod/log.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Log the initialization of the script
logging.info("InitGui.py script has started.")



class DocumentObserver:
    def slotOpenDocument(self, doc):
        logging.info(f"Document {doc.Label} has been opened.")
        self.run_macro()

    def run_macro(self):
        logging.info("Running the macro...")
        App.Console.PrintMessage("This message is from the macro executed after the document is opened.\n")
        # Example of additional log entry during macro execution
        logging.info("Macro execution is complete.")

# Create an instance of the observer
doc_observer = DocumentObserver()

# Add the observer to FreeCAD
App.addDocumentObserver(doc_observer)
logging.info("DocumentObserver has been added to FreeCAD.")
