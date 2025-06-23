import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget, QMessageBox, QLineEdit
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import Qt
from Umklasif import reasign_ifc

class MainWindow(QMainWindow):       
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.setWindowTitle("IFC Umklassifisierung")
        self.setGeometry(100, 100, 500, 400)
        self.setWindowIcon(QIcon("IFC.png"))
        

        fuente = QFont("Arial", 11)
        self.setFont(fuente)
       

        self.attribute_label = QLabel("Enter the name of the property were the information is:", self)
        self.attribute_input = QLineEdit(self)
        self.attribute_input.setPlaceholderText("Propertyname")

        self.reasign_button = QPushButton("Create a new IFC file with the reasigned classes", self)
        self.reasign_button.clicked.connect(self.reasign)

            
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignBottom)  # Align everything to the bottom

        layout.addWidget(self.attribute_label)
        layout.addWidget(self.attribute_input)
        layout.addWidget(self.reasign_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        def load_stylesheet():
         with open("styles_c.css", "r") as file:
             return file.read()
        self.setStyleSheet(load_stylesheet())
                           
    def reasign(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecct an IFC", "", "IFC Files (*.ifc)")
        if not file_path:
            return
        
        save_path, _ = QFileDialog.getSaveFileName(self, "Save new IFC file", "", "IFC Files (*.ifc)")
        if not save_path:
            return
        
        attribute_name = self.attribute_input.text()
        if not attribute_name:
            QMessageBox.warning(self, "Warning", "Please enter the attribute name.")
            return

        try:
            reasign_ifc(file_path, save_path, attribute_name)
            QMessageBox.information(self, "Succesfull", f"Successfully reassign and saved as: {save_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))


if __name__ == '__main__':
    app = QApplication(sys.argv)  
    window = MainWindow()  # Ahora MainWindow es la clase de la interfaz
    window.show()
    sys.exit(app.exec())

