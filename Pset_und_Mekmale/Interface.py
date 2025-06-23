import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QIcon, QFont, QPixmap
from PyQt6.QtCore import Qt
from IfcToExcel import export_ifc_to_excel
from ExcelToIfc import import_excel_to_ifc


class MainWindow(QMainWindow):       
    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("Interface IFC - Excel")
        self.setGeometry(100, 100, 500, 400)
        self.setWindowIcon(QIcon("IFC.png"))  # icono
        
        fuente = QFont("Arial", 11)
        self.setFont(fuente)

        self.label = QLabel("What would you like to do?:", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.export_button = QPushButton("Step 1:Export IFC Attributes to Excel", self)
        self.export_button.clicked.connect(self.exportar)

        self.import_button = QPushButton("Step 2: Import Pset und Properties from Excel to IFC", self)
        self.import_button.clicked.connect(self.importar)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.export_button)
        layout.addWidget(self.import_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        def load_stylesheet():
         with open("styles_e.css", "r") as file:
             return file.read()
        self.setStyleSheet(load_stylesheet())
                           
    def exportar(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Selecct an IFC", "", "IFC Files (*.ifc)")
        if not file_path:
            return
        
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Excel file", "", "Excel Files (*.xlsx)")
        if not output_path:
            return
        
        try:
            export_ifc_to_excel(file_path, output_path)
            QMessageBox.information(self, "Succesfull", f"Successfully exported to: {output_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def importar(self):
        excel_path, _ = QFileDialog.getOpenFileName(self, "Selecct an Excel file", "", "Excel Files (*.xlsx)")
        if not excel_path:
            return
        
        save_ifc_path, _ = QFileDialog.getSaveFileName(self, "Save IFC file", "", "IFC Files (*.ifc)")
        if not save_ifc_path:
            return
        
        try:
            import_excel_to_ifc(excel_path, save_ifc_path)
            QMessageBox.information(self, "Success", f"IFC updated and saved in: {save_ifc_path}")
        except Exception as e:
            QMessageBox.critical(self, "Error - Review excel list, make sure GlobalID are contained on the model and information is fullfield", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
