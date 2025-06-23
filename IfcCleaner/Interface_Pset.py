from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QWidget
)
from PsetFiltered import delete_ifc_attributes

class IfcCleanerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IFC Cleaner")
        self.setGeometry(100, 100, 400, 300)

        # Main layout
        layout = QVBoxLayout()

        self.file_label = QLabel("Selected IFC File:")
        layout.addWidget(self.file_label)
        self.select_file_button = QPushButton("Select IFC File")
        self.select_file_button.clicked.connect(self.select_ifc_file)
        layout.addWidget(self.select_file_button)

        self.entity_input = QLineEdit()
        self.entity_input.setPlaceholderText("Enter entity type (e.g., IfcWall) or leave empty for all")
        layout.addWidget(self.entity_input)

        self.predefined_type_input = QLineEdit()
        self.predefined_type_input.setPlaceholderText("Enter PredefinedType (optional)")
        layout.addWidget(self.predefined_type_input)

        self.object_type_input = QLineEdit()
        self.object_type_input.setPlaceholderText("Enter ObjectType (optional)")
        layout.addWidget(self.object_type_input)

        self.pset_input = QLineEdit()
        self.pset_input.setPlaceholderText("Enter property set to delete")
        layout.addWidget(self.pset_input)

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

        entity_name = self.entity_input.text().strip() or None
        predefined_type = self.predefined_type_input.text().strip() or None
        object_type = self.object_type_input.text().strip() or None

        pset = self.pset_input.text().split(",")
        pset = [attr.strip() for attr in pset if attr.strip()]
        if not pset:
            self.file_label.setText("Error: No property set specified!")
            return

        output_file_path = self.ifc_file_path.replace(".ifc", "_cleaned.ifc")
        delete_ifc_attributes(self.ifc_file_path, output_file_path, pset, entity_name, predefined_type, object_type)
        self.file_label.setText(f"File cleaned and saved to: {output_file_path}")

if __name__ == "__main__":
    app = QApplication([])
    window = IfcCleanerApp()
    window.show()
    app.exec()