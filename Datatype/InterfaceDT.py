import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QWidget, QMessageBox
)
from Datatype import change_property_datatype  # Make sure this matches the function name in Datatype.py

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Modificar Propiedades IFC")
        self.setGeometry(100, 100, 400, 300)

        # Layout principal
        layout = QVBoxLayout()

        # Widgets
        self.file_label = QLabel("Archivo IFC:")
        self.file_path_input = QLineEdit()
        self.browse_button = QPushButton("Seleccionar Archivo")
        self.entity_label = QLabel("Nombre de la Entidad:")
        self.entity_input = QLineEdit()
        self.property_label = QLabel("Nombre de la Propiedad:") 
        self.property_input = QLineEdit()
        self.datatype_label = QLabel("Nuevo Tipo de Dato:")
        self.datatype_input = QLineEdit()
        self.run_button = QPushButton("Ejecutar")
        
        layout.addWidget(self.file_label)
        layout.addWidget(self.file_path_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.entity_label)
        layout.addWidget(self.entity_input)
        layout.addWidget(self.property_label) 
        layout.addWidget(self.property_input) 
        layout.addWidget(self.datatype_label)
        layout.addWidget(self.datatype_input)
        layout.addWidget(self.run_button)

        # Conectar señales
        self.browse_button.clicked.connect(self.select_file)
        self.run_button.clicked.connect(self.run_script)

        # Configurar widget central
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Seleccionar Archivo IFC", "", "Archivos IFC (*.ifc)")
        if file_path:
            self.file_path_input.setText(file_path)

    def run_script(self):
        file_path = self.file_path_input.text()
        entity_name = self.entity_input.text()
        property_name = self.property_input.text()  
        datatype_str = self.datatype_input.text()

        # Validate empty fields
        if not file_path or not entity_name or not property_name or not datatype_str:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")
            return

        try:
            # Pass the IFC datatype string directly (case-insensitive handled in backend)
            change_property_datatype(file_path, entity_name, property_name, datatype_str)
            QMessageBox.information(self, "Éxito", "Propiedad modificada correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Se produjo un error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
