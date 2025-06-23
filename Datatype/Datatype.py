import ifcopenshell
import ifcopenshell.util.element

def get_python_type_from_ifc(datatype_str):
    """
    Receives an IFC datatype string and returns the corresponding Python type.
    Raises ValueError if the type is invalid.
    """
    # Map IFC datatypes to Python types
    datatype_map = {
        "IFCBOOLEAN": bool,
        "IFCINTEGER": int,
        "IFCREAL": float,
        "IFCNUMBER": float,
        "IFCLENGTHMEASURE": float,
        "IFCAREAMEASURE": float,
        "IFCVOLUMEMEASURE": float,
        "IFCPOSITIVELENGTHMEASURE": float,
        "IFCLABEL": str,
        "IFCTEXT": str,
        "IFCIDENTIFIER": str,
        "IFCDATE": str,
        "IFCLOGICAL": bool,
        "IFCURIREFERENCE": str,
        "IFCINTEGERCOUNTMEASURE": int,
        "IFCPROPERTYREFERENCEVALUE": dict
    }
    # Convert input to uppercase for case-insensitive matching
    datatype_str = datatype_str.upper()
    if datatype_str not in datatype_map:
        raise ValueError(f"Invalid IFC datatype specified: {datatype_str}")
    return datatype_map[datatype_str]

def change_property_datatype(ifc_file_path, entity_name, property_name, new_ifc_datatype):
    # Step 1: Open the IFC file
    ifc_file = ifcopenshell.open(ifc_file_path)
    # Step 2: Get all entities of the specified type
    entities = ifc_file.by_type(entity_name)
    if not entities:
        raise ValueError(f"No entities found with the name '{entity_name}'.")

    property_found = False

    # Step 3: Iterate through each entity
    for entity in entities:
        # Step 4: Check if the entity has property sets
        if hasattr(entity, "IsDefinedBy"):
            # Step 5: Iterate through each relationship
            for rel in entity.IsDefinedBy:
                # Step 6: Find the property set relationship
                if rel.is_a("IfcRelDefinesByProperties") and rel.RelatingPropertyDefinition.is_a("IfcPropertySet"):
                    property_set = rel.RelatingPropertyDefinition
                    # Step 7: Iterate through properties in the property set
                    for prop in property_set.HasProperties:
                        # Step 8: Check for the specific property by name
                        if prop.Name == property_name:
                            # Step 9: Check and change the datatype
                            if hasattr(prop, "NominalValue") and hasattr(prop.NominalValue, "wrappedValue"):
                                current_value = prop.NominalValue.wrappedValue
                                current_ifc_type = prop.NominalValue.is_a().upper()
                                new_ifc_datatype_upper = new_ifc_datatype.upper()
                                current_python_type = get_python_type_from_ifc(current_ifc_type)
                                new_python_type = get_python_type_from_ifc(new_ifc_datatype_upper)
                                if current_python_type != new_python_type:
                                    raise TypeError(
                                        f"Cannot change from {current_ifc_type} to {new_ifc_datatype_upper}: "
                                    )
                                # Create new value wrapper of the new IFC type
                                new_value = ifc_file.create_entity(new_ifc_datatype_upper, current_value)
                                prop.NominalValue = new_value
                                print(f"Property '{property_name}' of entity '{entity_name}' changed from {current_ifc_type} to {new_ifc_datatype_upper}")
                                property_found = True
    if not property_found:
        raise ValueError(f"Property '{property_name}' not found in any '{entity_name}' entity.")

    # Step 10: Save the changes to the IFC file
    ifc_file.write(ifc_file_path)
    print(f"IFC file '{ifc_file_path}' updated successfully.")

