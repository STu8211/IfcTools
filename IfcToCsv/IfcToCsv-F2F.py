import ifcopenshell
import csv
import os
from ifcopenshell.util.file import IfcHeaderExtractor

def export_ifc_to_csvs(ifc_path, output_dir, prefix):
    ifc = ifcopenshell.open(ifc_path)

    
    # --- STEP 1: Export Property Sets (Psets) ---
    # For each element, extract property sets and their values
    with open(f"{output_dir}/{prefix}_psets.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["GlobalID", "Entity", "PsetName", "Attribute", "Value"])
        for elemento in ifc.by_type('IfcElement'):
            entity = elemento.is_a()
            for definition in elemento.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    pset = definition.RelatingPropertyDefinition
                    if pset.is_a('IfcPropertySet'):
                        for prop in pset.HasProperties:
                            if hasattr(prop, "NominalValue") and prop.NominalValue:
                                value = prop.NominalValue.wrappedValue
                    # IfcPropertyEnumeratedValue
                            elif hasattr(prop, "EnumerationValues") and prop.EnumerationValues:
                                value = "; ".join(str(ev.wrappedValue) for ev in prop.EnumerationValues if hasattr(ev, "wrappedValue"))
                            writer.writerow([
                                elemento.GlobalId,
                                entity,
                                pset.Name,
                                prop.Name,
                                value
                            ])

    # --- STEP 2: Export Materials by Element ---
    # For each element, extract associated materials (handles different material assignment types)
    with open(f"{output_dir}/{prefix}_materials.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ElementGlobalID", "ElementType", "ElementName", "MaterialName"])
        for elemento in ifc.by_type('IfcElement'):
            material_names = []
            if hasattr(elemento, "HasAssociations"):
                for assoc in elemento.HasAssociations:
                    if assoc.is_a("IfcRelAssociatesMaterial"):
                        material = assoc.RelatingMaterial
                        # IfcMaterial (simple)
                        if material.is_a("IfcMaterial"):
                            material_names.append(material.Name)
                        # IfcMaterialList
                        elif material.is_a("IfcMaterialList") and hasattr(material, "Materials"):
                            for mat in material.Materials:
                                material_names.append(mat.Name)
                        # IfcMaterialLayerSet
                        elif material.is_a("IfcMaterialLayerSetUsage") and hasattr(material, "ForLayerSet"):
                            for layer in material.ForLayerSet.MaterialLayers:
                                if hasattr(layer, "Material") and layer.Material:
                                    material_names.append(layer.Material.Name)
                                
                        # IfcMaterialConstituentSet
                        elif material.is_a("IfcMaterialConstituentSet") and hasattr(material, "MaterialConstituents"):
                            for constituent in material.MaterialConstituents:
                                if hasattr(constituent, "Material") and constituent.Material:
                                    material_names.append(constituent.Material.Name)
            if not material_names:
                material_names = ["Not defined"]
            for mat_name in material_names:
                # Write info back to the csv file
                writer.writerow([
                    elemento.GlobalId if hasattr(elemento, 'GlobalId') else "Not defined",
                    elemento.is_a() if hasattr(elemento, 'is_a') else "Not defined",
                    elemento.Name if hasattr(elemento, 'Name') else "Not defined",
                    mat_name
                ])

    # --- STEP 3: Export Quantity Take-Off (QTO) ---
    # For each element, extract quantity sets and their values
    with open(f"{output_dir}/{prefix}_quantities.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["GlobalID", "QuantitySetName", "QuantityName", "Value"])
        for elemento in ifc.by_type('IfcElement'):
            for definition in elemento.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    qto = definition.RelatingPropertyDefinition
                     # Check if the property definition is a quantity set
                    if qto.is_a('IfcElementQuantity'):
                        # Iterate through quantities in the quantity set and extract values considering different types
                        for quantity in qto.Quantities:
                            value = None
                            if quantity.is_a("IfcQuantityLength"):
                                value = quantity.LengthValue
                            elif quantity.is_a("IfcQuantityArea"):
                                value = quantity.AreaValue
                            elif quantity.is_a("IfcQuantityVolume"):
                                value = quantity.VolumeValue
                            elif quantity.is_a("IfcQuantityCount"):
                                value = quantity.CountValue
                            elif quantity.is_a("IfcQuantityWeight"):
                                value = quantity.WeightValue
                            elif quantity.is_a("IfcQuantityTime"):
                                value = quantity.TimeValue
                            # Write info back to the csv file
                            writer.writerow([
                                elemento.GlobalId,
                                qto.Name if hasattr(qto, 'Name') else "Not defined",
                                quantity.Name,
                                value
                            ])

    # --- STEP 4: Export Entities ---
    # For each element, export basic entity information (type, name, predefined type, etc.)
    with open(f"{output_dir}/{prefix}_entities.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["GlobalID", "Name", "IfcEntity", "PredefinedType", "TypeName"])
        for elemento in ifc.by_type('IfcElement'):
            global_id = elemento.GlobalId
            name = elemento.Name
            entity = elemento.is_a()
            predefined_type = getattr(elemento, "PredefinedType", "Not defined")
            type_name = getattr(elemento, "IsTypedBy", None)
            type_name = type_name[0].RelatingType.Name if type_name else "Not defined"
            object_type = getattr(elemento, "ObjectType", "Not defined")
            
            writer.writerow([
                global_id,
                name if name else "No Name",
                entity if entity else "Not defined",
                predefined_type if predefined_type else "Not defined",
                type_name,
                object_type if object_type else "Not defined"
            ])

    # --- STEP 5: Export IFC File Metadata ---
    # Extract general metadata from the IFC file header (schema, timestamp, description, filename)
    with open(f"{output_dir}/{prefix}_ifc_metadata.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Schema", "Timestamp","Description", "Filename"])
        extractor = IfcHeaderExtractor(ifc_path)
    # Get dictionary of the extracted metadata.
        header_info = extractor.extract() 
    #use information from the header
        file_schema = header_info["schema_name"] 
        timestamp = header_info["time_stamp"]
        description = header_info["description"]
        file_name = header_info["name"]

        writer.writerow([
            file_schema,
            timestamp,
            description,
            file_name
        ])

    
    # --- STEP 6: Export Floors and Elements ---
    # For each floor (building storey), export its elements and their basic info
    with open(f"{output_dir}/{prefix}_floors_and_elements.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["FloorName", "FloorElevation", "ElementGlobalID", "ElementName", "ElementType"])
        # Get all building storeys (floors)
        for piso in ifc.by_type('IfcBuildingStorey'):
            floor_name = piso.Name if piso.Name else "No Name"
            floor_elevation = piso.Elevation if hasattr(piso, "Elevation") else "Not defined"
            # Get the associated elements for each floor
            for rel in piso.ContainsElements:
                for elemento in rel.RelatedElements:
                    element_global_id = elemento.GlobalId
                    element_name = elemento.Name if elemento.Name else "No Name"
                    element_type = elemento.is_a()
                    # Write info back to the csv file
                    writer.writerow([
                        floor_name,
                        floor_elevation,
                        element_global_id,
                        element_name,
                        element_type
                    ])
# define the main function to process all IFC files in a folder
def process_folder(folder_path, output_dir):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.ifc'):
            ifc_path = os.path.join(folder_path, filename)
            prefix = os.path.splitext(filename)[0]
            print(f"Procesing {filename} ...")
            export_ifc_to_csvs(ifc_path, output_dir, prefix)
    print("✅ all files have been processed.")

if __name__ == "__main__":
    input_folder = r'C:\Users\FlorenciaGomez\SIDE\SIDE - Team\17_Severin\05_KI\IFC Models for Training\_IFC-Modelle nach Autorensoftware'   # Input folder- IFC
    output_dir = r'C:\Users\FlorenciaGomez\Desktop\SIDE_APP\Data_to_PBI\CSV'    # Output folder
    process_folder(input_folder, output_dir)
