import ifcopenshell
import pandas as pd

def import_excel_to_ifc(excel_path, ifc_path):
    ifc = ifcopenshell.open(ifc_path)

    # Excel iteration
    df = pd.read_excel(excel_path, sheet_name="Project")

    for index, row in df.iterrows():
        global_id = row['GlobalID']
        
        elemento = ifc.by_guid(global_id)
        
        if elemento:
            psets = {}

            for column_index, column_name in enumerate(df.columns):
                if column_index < 5:  # Ignore first 5 column
                    continue
                
        
                if '.' not in column_name:
                    print(f"⚠️ Columna'{column_name}' has incorrect format 'Pset.Atribut'. Ignored.")
                    continue
                
                pset_name, attribute_name = column_name.split('.', 1)
                column_value = row[column_name]

                # Verify pset
                if pset_name not in psets:
                    existing_pset = None
                    for atrib in elemento.IsDefinedBy:
                        if atrib.is_a("IfcRelDefinesByProperties"):
                            property_set = atrib.RelatingPropertyDefinition
                            if property_set.is_a("IfcPropertySet") and property_set.Name == pset_name:
                                existing_pset = property_set
                                break
                    
                  
                    if not existing_pset:
                        existing_pset = ifc.create_entity('IfcPropertySet', Name=pset_name)
                        ifc.create_entity('IfcRelDefinesByProperties', RelatingPropertyDefinition=existing_pset, RelatedObjects=[elemento])
                  
                    if not hasattr(existing_pset, 'HasProperties') or existing_pset.HasProperties is None:
                        existing_pset.HasProperties = []
                    
                    psets[pset_name] = existing_pset
                else:
                    existing_pset = psets[pset_name]

                # look for existing property
                found_property = False
                for prop in existing_pset.HasProperties:
                    if prop.Name == attribute_name:
                        prop.NominalValue = ifc.create_entity('IfcLabel', column_value)
                        found_property = True
                        break
                
                if not found_property:
                    new_property = ifc.create_entity('IfcPropertySingleValue', Name=attribute_name, NominalValue=ifc.create_entity('IfcLabel', column_value))
                    existing_pset.HasProperties = list(existing_pset.HasProperties) + [new_property]

    ifc.write(ifc_path)

    print(f"✅ IFC file updated: {ifc_path}")

if __name__ == "__main__":
    import_excel_to_ifc("ruta/al/archivo.xlsx", "ruta/al/archivo.ifc")
