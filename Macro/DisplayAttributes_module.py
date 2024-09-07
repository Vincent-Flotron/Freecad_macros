from PySide import QtGui
import xml.etree.ElementTree as ET
import FreeCAD               as App
import FreeCADGui            as Gui
import sys



def display_attributes():
    # Get the main window of FreeCAD
    parent_window = Gui.getMainWindow()
    window = PropertyTreeView(parent_window)
    window.run()


# Function to parse the Content XML and add it to the tree view
def parse_content_and_add_to_tree(parent_item, xml_content):
    try:
        # Parse the XML string
        root = ET.ElementTree(ET.fromstring(f"<root>{xml_content}</root>")).getroot()

        # Recursively add the children to the tree view
        for child in root:
            add_xml_to_tree(parent_item, child)
    except ET.ParseError as e:
        error_item = QtGui.QTreeWidgetItem(parent_item, [f"Invalid XML content: {e}"])

# Function to add XML elements to the tree view recursively
def add_xml_to_tree(parent_item, element):
    # Create a new tree item with the tag and attributes
    attrs = ", ".join([f'{k}="{v}"' for k, v in element.attrib.items()])
    text = f"{element.tag} ({attrs})" if attrs else element.tag
    item = QtGui.QTreeWidgetItem(parent_item, [text])

    # If the element has text content, add it as a child node
    if element.text and element.text.strip():
        QtGui.QTreeWidgetItem(item, [element.text.strip()])

    # Recursively add the element's children
    for child in element:
        add_xml_to_tree(item, child)

# Function to add collections (tuples, lists, dicts) to the tree view
def add_collection_to_tree(parent_item, collection):
    if isinstance(collection, (tuple, list)):
        for i, value in enumerate(collection):
            item = QtGui.QTreeWidgetItem(parent_item, [f"Index {i}"])
            if isinstance(value, (tuple, list, dict)):
                add_collection_to_tree(item, value)
            else:
                QtGui.QTreeWidgetItem(item, [str(value)])
    elif isinstance(collection, dict):
        for key, value in collection.items():
            item = QtGui.QTreeWidgetItem(parent_item, [str(key)])
            if isinstance(value, (tuple, list, dict)):
                add_collection_to_tree(item, value)
            else:
                QtGui.QTreeWidgetItem(item, [str(value)])

# Function to classify the attributes of the object
def classify_attributes(obj):
    properties = []
    dunder_attributes = []
    methods = []
    content_xml = None

    for attr in dir(obj):
        try:
            value = getattr(obj, attr)
            if attr.startswith('__') and attr.endswith('__'):
                dunder_attributes.append(attr)
            elif callable(value):
                methods.append(attr)
            elif attr == "Content":
                content_xml = value  # Save the XML content for later
            else:
                properties.append((attr, value))
        except Exception:
            pass

    return content_xml, properties, dunder_attributes, methods

# Function to populate the TreeView
def populate_tree(tree, content_xml, properties, dunder_attributes, methods, obj):
    root = tree.invisibleRootItem()

    # Content node
    if content_xml:
        # print('xml')
        content_node = QtGui.QTreeWidgetItem(root, ["Content"])
        parse_content_and_add_to_tree(content_node, content_xml)

    # Properties node
    properties_node = QtGui.QTreeWidgetItem(root, ["Properties"])
    for prop, value in properties:
        # print(f'prp: {prop}.{value}')
        prop_item = QtGui.QTreeWidgetItem(properties_node, [prop])
        if isinstance(value, (tuple, list, dict)):
            add_collection_to_tree(prop_item, value)
        else:
            QtGui.QTreeWidgetItem(prop_item, [str(value)])

    # Dunder Attributes node
    dunder_node = QtGui.QTreeWidgetItem(root, ["Dunder Attributes"])
    for dunder in dunder_attributes:
        # print(f'dunder: {dunder}')
        value = getattr(obj, dunder, "(Could not retrieve value)")
        QtGui.QTreeWidgetItem(dunder_node, [f"{dunder}: {value}"])

    # Methods node
    methods_node = QtGui.QTreeWidgetItem(root, ["Methods"])
    for method in methods:
        # print(f'method: {method}')
        QtGui.QTreeWidgetItem(methods_node, [method])


# Main application code
class PropertyTreeView(QtGui.QMainWindow):
    def __init__(self, parent=None):
        # self.app = QtGui.QApplication.instance()
        # if not self.app:
        #     self.app = QtGui.QApplication(sys.argv)
        super(PropertyTreeView, self).__init__(parent)
        self.setWindowTitle('Object Properties')

        # Create TreeView widget
        self.tree = QtGui.QTreeWidget()
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(['Property'])

        self.setCentralWidget(self.tree)
        self.resize(800, 600)

        # Get the list of selected objects
        selected_objects = Gui.Selection.getSelection()
        # print(f'selected_objects[0].Name: {selected_objects[0].Name}')

        if selected_objects:
            for obj in selected_objects:
                content, properties, dunder_attributes, methods = classify_attributes(obj)
                populate_tree(self.tree, content, properties, dunder_attributes, methods, obj)
        else:
            QtGui.QMessageBox.information(self, "No Selection", "No object selected.")

    def run(self):
        self.show()