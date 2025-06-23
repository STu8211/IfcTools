import sys
import os
import json
from time import perf_counter
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QComboBox, QCheckBox, QMessageBox
)
from PyQt6.QtGui import QIcon 
import ifcjson


class IFC2JSONConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IFC to JSON Converter")
        self.setGeometry(100, 100, 400, 300)
        self.setWindowIcon(QIcon("IFC.png")) 

        # Initialize variables
        self.ifc_file_path = ""
        self.json_file_path = ""
        self.version = "4"
        self.compact = False
        self.no_inverse = False
        self.empty_properties = False
        self.no_ownerhistory = False
        self.geometry = "unchanged"

        # Set up UI
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Input file selection
        self.input_label = QLabel("Input IFC File: Not selected")
        layout.addWidget(self.input_label)
        input_button = QPushButton("Select Input File")
        input_button.clicked.connect(self.select_input_file)
        layout.addWidget(input_button)

        # Output file selection
        self.output_label = QLabel("Output JSON File: Not selected")
        layout.addWidget(self.output_label)
        output_button = QPushButton("Select Output File")
        output_button.clicked.connect(self.select_output_file)
        layout.addWidget(output_button)

        # Version selection
        self.version_combo = QComboBox()
        self.version_combo.addItems(["4", "5a"])
        self.version_combo.currentTextChanged.connect(self.set_version)
        layout.addWidget(QLabel("Select IFCJSON Version:"))
        layout.addWidget(self.version_combo)

        # Options
        self.compact_checkbox = QCheckBox("Compact Mode")
        self.compact_checkbox.stateChanged.connect(self.set_compact)
        layout.addWidget(self.compact_checkbox)

        self.no_inverse_checkbox = QCheckBox("No Inverse Relationships")
        self.no_inverse_checkbox.stateChanged.connect(self.set_no_inverse)
        layout.addWidget(self.no_inverse_checkbox)

        self.empty_properties_checkbox = QCheckBox("Include Empty Properties")
        self.empty_properties_checkbox.stateChanged.connect(self.set_empty_properties)
        layout.addWidget(self.empty_properties_checkbox)

        self.no_ownerhistory_checkbox = QCheckBox("Remove IfcOwnerHistory")
        self.no_ownerhistory_checkbox.stateChanged.connect(self.set_no_ownerhistory)
        layout.addWidget(self.no_ownerhistory_checkbox)

        self.geometry_combo = QComboBox()
        self.geometry_combo.addItems(["unchanged", "none", "tessellate"])
        self.geometry_combo.currentTextChanged.connect(self.set_geometry)
        layout.addWidget(QLabel("Geometry Output Type:"))
        layout.addWidget(self.geometry_combo)

        # Convert button
        convert_button = QPushButton("Convert")
        convert_button.clicked.connect(self.convert_ifc_to_json)
        layout.addWidget(convert_button)

        # Set layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Input IFC File", "", "IFC Files (*.ifc)")
        if file_path:
            self.ifc_file_path = file_path
            self.input_label.setText(f"Input IFC File: {file_path}")

    def select_output_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Select Output JSON File", "", "JSON Files (*.json)")
        if file_path:
            self.json_file_path = file_path
            self.output_label.setText(f"Output JSON File: {file_path}")

    def set_version(self, version):
        self.version = version

    def set_compact(self, state):
        self.compact = state == 2

    def set_no_inverse(self, state):
        self.no_inverse = state == 2

    def set_empty_properties(self, state):
        self.empty_properties = state == 2

    def set_no_ownerhistory(self, state):
        self.no_ownerhistory = state == 2

    def set_geometry(self, geometry):
        self.geometry = geometry

    def convert_ifc_to_json(self):
        if not self.ifc_file_path or not os.path.isfile(self.ifc_file_path):
            QMessageBox.critical(self, "Error", "Invalid input IFC file.")
            return

        if not self.json_file_path:
            QMessageBox.critical(self, "Error", "Output JSON file not selected.")
            return

        t1_start = perf_counter()

        try:
            if self.version == "4":
                json_data = ifcjson.IFC2JSON4(
                    self.ifc_file_path,
                    self.compact,
                    NO_INVERSE=self.no_inverse,
                    EMPTY_PROPERTIES=self.empty_properties,
                    NO_OWNERHISTORY=self.no_ownerhistory,
                    GEOMETRY=self.geometry
                ).spf2Json()
            elif self.version == "5a":
                json_data = ifcjson.IFC2JSON5a(
                    self.ifc_file_path,
                    self.compact,
                    EMPTY_PROPERTIES=self.empty_properties
                ).spf2Json()
            else:
                QMessageBox.critical(self, "Error", f"Version {self.version} is not supported.")
                return

            with open(self.json_file_path, 'w') as outfile:
                json.dump(json_data, outfile, indent=None if self.compact else 2)

            t1_stop = perf_counter()
            QMessageBox.information(self, "Success", f"Conversion completed in {t1_stop - t1_start:.2f} seconds.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IFC2JSONConverter()
    window.show()
    sys.exit(app.exec())