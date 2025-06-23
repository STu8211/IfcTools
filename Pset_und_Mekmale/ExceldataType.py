import ifcopenshell
import pandas as pd

def import_excel_to_ifc(excel_path, ifc_path):
    ifc = ifcopenshell.open(ifc_path)
    df = pd.read_excel(excel_path, sheet_name="Project")

    #Excel iteration
    for index, row in df.iterrows():
        global_id = row['GlobalID']
        #look for the element by GlobalID
        elemento = ifc.by_guid(global_id)

        #if the element exists
        if elemento:
            psets = {}
            for column_index, column_name in enumerate(df.columns):
                if column_index < 5:  # Ignore the first 5 columns
                    continue
                
                # Check if the column name has the correct structure 'Pset.Attribute'
                if '.' not in column_name:
                    print(f"⚠️ Column '{column_name}' has not the correct strucutre 'Pset.Atribut'. Ignored.")
                    continue
                # Split the column name into property set name and attribute name
                pset_name, attribute_name = column_name.split('.', 1)
                # Get the value of the column
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
                    # If the property set does not exist, create it
                    if not existing_pset:
                        existing_pset = ifc.create_entity('IfcPropertySet', Name=pset_name)
                        ifc.create_entity('IfcRelDefinesByProperties', RelatingPropertyDefinition=existing_pset, RelatedObjects=[elemento])
                    
                    if not hasattr(existing_pset, 'HasProperties') or existing_pset.HasProperties is None:
                        existing_pset.HasProperties = []
                    
                    psets[pset_name] = existing_pset
                else:
                    existing_pset = psets[pset_name]

                # Look for existing property
                found_property = False
                for prop in existing_pset.HasProperties:
                    if prop.Name == attribute_name:
                        # Update the property value
                        if '.' in str(column_value):
                            datatype, value = str(column_value).split('.', 1)
                        
                            if datatype == "IfcLabel":
                                prop.NominalValue = ifc.create_entity("IfcLabel", value)
                            elif datatype == "IfcText":
                                prop.NominalValue = ifc.create_entity("IfcText", value)
                            elif datatype == "IfcInteger":
                                prop.NominalValue = ifc.create_entity("IfcInteger", int(value))
                            elif datatype == "IfcReal":
                                prop.NominalValue = ifc.create_entity("IfcReal", float(value))
                            elif datatype == "IfcPositiveLengthMeasure":
                                prop.NominalValue = ifc.create_entity("IfcPositiveLengthMeasure", float(value))
                            elif datatype == "IfcVolumeMeasure":
                                prop.NominalValue = ifc.create_entity("IfcVolumeMeasure", float(value))
                            elif datatype == "IfcAreaMeasure":
                                prop.NominalValue = ifc.create_entity("IfcAreaMeasure", float(value))
                            elif datatype == "IfcBoolean":
                                prop.NominalValue = ifc.create_entity("IfcBoolean", value.strip().lower() in ["true", "yes", "1"])
                            else:
                                raise ValueError(f"Datatype not supported: {datatype}")
                        else:
                            datatype, value = "IfcLabel", str(column_value)
                            prop.NominalValue = ifc.create_entity(datatype, value)
                        found_property = True
                        break
                
                # if not, create it
                if not found_property:
                    if '.' in str(column_value):
                        datatype, value = str(column_value).split('.', 1)
                        if datatype == "IfcLabel":
                            nominal_value = ifc.create_entity("IfcLabel", value)
                        elif datatype == "IfcText":
                            nominal_value = ifc.create_entity("IfcText", value)
                        elif datatype == "IfcInteger":
                            nominal_value = ifc.create_entity("IfcInteger", int(value))
                        elif datatype == "IfcReal":
                            nominal_value = ifc.create_entity("IfcReal", float(value))
                        elif datatype == "IfcPositiveLengthMeasure":
                                prop.NominalValue = ifc.create_entity("IfcPositiveLengthMeasure", float(value))
                        elif datatype == "IfcVolumeMeasure":
                                prop.NominalValue = ifc.create_entity("IfcVolumeMeasure", float(value))
                        elif datatype == "IfcAreaMeasure":
                                prop.NominalValue = ifc.create_entity("IfcAreaMeasure", float(value))
                        elif datatype == "IfcBoolean":
                            nominal_value = ifc.create_entity("IfcBoolean", value.strip().lower() in ["true", "yes", "1"])
                        else:
                            raise ValueError(f"Datatype not supported: {datatype}")
                    else:
                            datatype, value = "IfcLabel", str(column_value)
                    new_property = ifc.create_entity('IfcPropertySingleValue',Name=attribute_name,NominalValue=nominal_value)
                    existing_pset.HasProperties = list(existing_pset.HasProperties) + [new_property]
    # Write the updated IFC file  
    ifc.write(ifc_path)
    print(f"✅  IFC file updated: {ifc_path}")


if __name__ == "__main__":
    import_excel_to_ifc("ruta/al/archivo.xlsx", "ruta/al/archivo.ifc")
