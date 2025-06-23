import ifcopenshell
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QWidget
)

def delete_ifc_attribut(ifc_file_path, output_file_path, attributes_to_delete):
   
    ifc_file = ifcopenshell.open(ifc_file_path)

    # Iterate through all elements in the IFC file
    for element in ifc_file.by_type("IfcElement"):
        # Access the property sets (Psets) of the element
        if hasattr(element, "IsDefinedBy"):
            for rel in element.IsDefinedBy:
                if rel.is_a("IfcRelDefinesByProperties") and rel.RelatingPropertyDefinition.is_a("IfcPropertySet"):
                    pset = rel.RelatingPropertyDefinition
                    # Convert HasProperties to a list, modify it, and reassign
                    properties = list(pset.HasProperties)
                    for prop in properties:
                        if prop.Name in attributes_to_delete:
                            # Remove the property from the list
                            print(f"Property '{prop.Name}'found")
                            properties.remove(prop)
                            # Delete the property from the IFC model
                            ifc_file.remove(prop)
                    # Reassign the modified list back to HasProperties
                    pset.HasProperties = properties

    ifc_file.write(output_file_path)

class IfcCleanerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IFC Cleaner")
        self.setGeometry(100, 100, 400, 200)

        # Main layout
        layout = QVBoxLayout()

        
        self.file_label = QLabel("Selected IFC File:")
        layout.addWidget(self.file_label)
        self.select_file_button = QPushButton("Select IFC File")
        self.select_file_button.clicked.connect(self.select_ifc_file)
        layout.addWidget(self.select_file_button)

       
        self.attributes_input = QLineEdit()
        self.attributes_input.setPlaceholderText("Enter property to delete")
        layout.addWidget(self.attributes_input)

        
        self.execute_button = QPushButton("Clean IFC File")
        self.execute_button.clicked.connect(self.clean_ifc_file)
        layout.addWidget(self.execute_button)

    
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Variables
        self.ifc_file_path = None

    def select_ifc_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select IFC File", "", "IFC Files (*.ifc)")
        if file_path:
            self.ifc_file_path = file_path
            self.file_label.setText(f"Selected IFC File: {file_path}")

    def clean_ifc_file(self):
        if not self.ifc_file_path:
            self.file_label.setText("Error: No IFC file selected!")
            return

        attributes = self.attributes_input.text().split(",")
        attributes = [attr.strip() for attr in attributes if attr.strip()]
        if not attributes:
            self.file_label.setText("Error: No properties specified!")
            return

        output_file_path = self.ifc_file_path.replace(".ifc", "_cleaned.ifc")
        delete_ifc_attribut(self.ifc_file_path, output_file_path, attributes)
        self.file_label.setText(f"File cleaned and saved to: {output_file_path}")

if __name__ == "__main__":
    app = QApplication([])
    window = IfcCleanerApp()
    window.show()
    app.exec()