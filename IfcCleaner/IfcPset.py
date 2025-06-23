import ifcopenshell
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QWidget
)

def delete_ifc_pset(ifc_file_path, output_file_path, pset_to_delete):
    
    ifc_file = ifcopenshell.open(ifc_file_path)
  
    # Iterate through all elements in the IFC file
    for element in ifc_file.by_type("IfcElement"):
        # Access the property sets (Psets) of the element
        if hasattr(element, "IsDefinedBy") and element.IsDefinedBy:
            relations_to_remove = []
            for rel in element.IsDefinedBy:
                if rel.is_a("IfcRelDefinesByProperties") and rel.RelatingPropertyDefinition.is_a("IfcPropertySet"):
                    pset = rel.RelatingPropertyDefinition
                    if pset.Name in pset_to_delete:
                        relations_to_remove.append(rel)
                        # Remove the Pset from the IFC model
                        ifc_file.remove(pset)
            
            # Remove relationships from the element
            for rel in relations_to_remove:
                ifc_file.remove(rel)



    ifc_file.write(output_file_path)
    
class IfcCleanerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IFC Cleaner")
        self.setGeometry(100, 100, 400, 200)

        # Main layout
        layout = QVBoxLayout()

        # File selection
        self.file_label = QLabel("Selected IFC File: None")
        layout.addWidget(self.file_label)
        self.select_file_button = QPushButton("Select IFC File")
        self.select_file_button.clicked.connect(self.select_ifc_file)
        layout.addWidget(self.select_file_button)

        # Attributes input
        self.pset_input = QLineEdit()
        self.pset_input.setPlaceholderText("Enter Pset to delete")
        layout.addWidget(self.pset_input)

        # Execute button
        self.execute_button = QPushButton("Clean IFC File")
        self.execute_button.clicked.connect(self.clean_ifc_file)
        layout.addWidget(self.execute_button)

        # Set central widget
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
            print("Error: No se seleccionó ningún archivo IFC.")
            return

        psets = self.pset_input.text().split(",")
        psets = [attr.strip() for attr in psets if attr.strip()]
        if not psets:
            self.file_label.setText("Error: No Pset specified!")
            print("Error: No se especificaron Pset para eliminar.")
            return

        output_file_path = self.ifc_file_path.replace(".ifc", "_cleaned.ifc")
        print(f"Archivo de salida: {output_file_path}")
        delete_ifc_pset(self.ifc_file_path, output_file_path, psets)
        self.file_label.setText(f"File cleaned and saved to: {output_file_path}")

if __name__ == "__main__":
    app = QApplication([])
    window = IfcCleanerApp()
    window.show()
    app.exec()