import ifcopenshell
from openpyxl import load_workbook
from shutil import copyfile

def export_ifc_to_excel(ifc_path, output_path):
    template_path = "C:/Users/FlorenciaGomez/Desktop/SIDE_APP/Pset_und_Mekmale/templateDataType.xlsx"
    # Copy template
    copyfile(template_path, output_path)

    ifc = ifcopenshell.open(ifc_path)

    # load excel for the worksheet project
    workbook = load_workbook(output_path)
    worksheet = workbook["Project"] 

    worksheet['A1'] = "GlobalID"
    worksheet['B1'] = "Name"
    worksheet['C1'] = "IfcEntity"
    worksheet['D1'] = "PredefinedType"
    worksheet['E1'] = "TypeName"

    # Filtering, look for all elements that are of type IfcElement
    elementos = ifc.by_type('IfcElement')

    row = 2  # start at row 2

    # Iteration and info extraction
    for elemento in elementos:
        global_id = elemento.GlobalId
        name = elemento.Name   
        entity = elemento.is_a()  
        predefined_type = getattr(elemento, "PredefinedType", "Not defined")
        type_name = getattr(elemento, "IsTypedBy", None)
        type_name = type_name[0].RelatingType.Name if type_name else "Not defined"

        worksheet[f'A{row}'] = global_id
        worksheet[f'B{row}'] = name if name else "No Name"
        worksheet[f'C{row}'] = entity if entity else "Not defined"
        worksheet[f'D{row}'] = predefined_type if predefined_type else "Not defined"
        worksheet[f'E{row}'] = type_name
        row += 1

#save excel file
    workbook.save(output_path)
    print(f"✅ Excel file saved: {output_path}")


if __name__ == "__main__":
    export_ifc_to_excel("ruta/al/archivo.ifc", "ruta/al/output.xlsx")
