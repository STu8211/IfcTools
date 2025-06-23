import ifcopenshell


def delete_ifc_attributes(ifc_file_path, output_file_path, attributes_to_delete, entity_name=None, predefined_type=None, object_type=None):
    ifc_file = ifcopenshell.open(ifc_file_path)

    # Normalize property names for case-insensitive comparison
    attributes_to_delete = [attr.strip().lower() for attr in attributes_to_delete if attr.strip()]

    # If no entity_name is given, process all elements in the model
    if entity_name:
        elements = ifc_file.by_type(entity_name)
        print(f"Elements{entity_name}: {len(elements)}")
    else:
        elements = list(ifc_file.by_type("IfcRoot"))  # All root elements (covers all entities)
        print(f"Elements in model:{len(elements)}")

    # If no filters, process all elements
    if not predefined_type and not object_type:
        filtered_elements = elements
    else:
        filtered_elements = []
        for element in elements:
            if predefined_type and hasattr(element, "PredefinedType"):
                if element.PredefinedType != predefined_type:
                    continue
            if object_type and hasattr(element, "ObjectType"):
                if element.ObjectType != object_type:
                    continue
            filtered_elements.append(element)

    print(f"Elements after filtering: {len(filtered_elements)}")

    # Process each element and delete specified Properties
    for element in filtered_elements:
        print(f"Processing entity: {getattr(element, 'GlobalId', 'NoId')}")
        if hasattr(element, "IsDefinedBy"):
            for rel in element.IsDefinedBy:
                if rel.is_a("IfcRelDefinesByProperties") and rel.RelatingPropertyDefinition.is_a("IfcPropertySet"):
                    pset = rel.RelatingPropertyDefinition
                    properties = list(pset.HasProperties)
                    updated_properties = []
                    for prop in properties:
                        if prop.Name.lower() in attributes_to_delete:
                            print(f"Property '{prop.Name}' found and deleted")
                            ifc_file.remove(prop)
                        else:
                            updated_properties.append(prop)
                    pset.HasProperties = updated_properties

    ifc_file.write(output_file_path)
    print(f"File successfully saved to: {output_file_path}")
