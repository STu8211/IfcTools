import ifcopenshell
import csv
from ifcopenshell.util.file import IfcHeaderExtractor

def export_ifc_to_csvs(ifc_path, output_dir):
    # Cargar el archivo IFC
    ifc = ifcopenshell.open(ifc_path)
    with open(f"{output_dir}/ifc_metadata.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Schema", "Timestamp", "Author", "Filename"])
        extractor = IfcHeaderExtractor(ifc_path)
# Get dictionary of the extracted metadata.
        header_info = extractor.extract() 

        file_schema = header_info["schema_name"]  # Por ejemplo: IFC4X3_ADD2
        timestamp = header_info["time_stamp"]
        author = header_info["autor"]
        file_name = header_info["file_name"]

        # Escribir los datos en el archivo CSV
        writer.writerow([
            file_schema,
            timestamp,
            author,
            file_name
        ])

if __name__ == "__main__":
    ifc_path = r"c:/Users/FlorenciaGomez/Desktop/SIDE_APP/IFC_filetest.ifc"  # Ruta al archivo IFC
    output_dir = r"c:/Users/FlorenciaGomez/Desktop/SIDE_APP/Data_to_PBI"  # Directorio de salida
    export_ifc_to_csvs(ifc_path, output_dir)