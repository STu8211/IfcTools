from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QWidget, QMessageBox
)
from IfcToCsv import export_ifc_to_csvs
import sys

class IfcToCsvUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Export IFC to CSV")

        # Widgets
        self.ifc_label = QLabel("IFC path:")
        self.ifc_input = QLineEdit()
        self.ifc_button = QPushButton("Select")
        self.ifc_button.clicked.connect(self.select_ifc_file)

        self.output_label = QLabel("Output folder:")
        self.output_input = QLineEdit()
        self.output_button = QPushButton("Select")
        self.output_button.clicked.connect(self.select_output_folder)

        self.export_button = QPushButton("Export to CSV")
        self.export_button.clicked.connect(self.run_export)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.ifc_label)
        layout.addWidget(self.ifc_input)
        layout.addWidget(self.ifc_button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.output_input)
        layout.addWidget(self.output_button)
        layout.addWidget(self.export_button)

        # Central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_ifc_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select IFC file", "", "IFC Files (*.ifc);;All files (*)"
        )
        if file_path:
            self.ifc_input.setText(file_path)

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select output folder")
        if folder_path:
            self.output_input.setText(folder_path)

    def run_export(self):
        ifc_path = self.ifc_input.text()
        output_dir = self.output_input.text()
        if not ifc_path or not output_dir:
            QMessageBox.critical(self, "Error", "You must select an IFC file and an output folder.")
            return
        try:
            export_ifc_to_csvs(ifc_path, output_dir)
            QMessageBox.information(self, "Success", "CSV files generated successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IfcToCsvUI()
    window.show()
    sys.exit(app.exec())
