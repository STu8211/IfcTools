import ifcopenshell
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog, QWidget
)

def delete_ifc_attributes(ifc_file_path, output_file_path, pset_to_delete, entity_name=None, predefined_type=None, object_type=None):
    ifc_file = ifcopenshell.open(ifc_file_path)

    # Normalize property set names for case-insensitive comparison
    pset_to_delete = [pset.strip().lower() for pset in pset_to_delete if pset.strip()]

    # Get elements by entity or all IfcRoot if not specified
    if entity_name:
        elements = ifc_file.by_type(entity_name)
        print(f"Elements {entity_name}: {len(elements)}")
    else:
        elements = list(ifc_file.by_type("IfcElement")) # All elements in the model
        print(f"Elements in model: {len(elements)}")

    # Filtering logic
    filtered_elements = []
    for element in elements:
        if predefined_type and hasattr(element, "PredefinedType"):
            if element.PredefinedType != predefined_type:
                continue
        if object_type and hasattr(element, "ObjectType"):
            if element.ObjectType != object_type:
                continue
        filtered_elements.append(element)
    # If no filters are given, filtered_elements will be all elements

    print(f"Elements after filtering: {len(filtered_elements)}")

    # Process each element and delete specified PropertySets
    for element in filtered_elements:
        print(f"Processing entity: {getattr(element, 'GlobalId', 'NoId')}")
        if hasattr(element, "IsDefinedBy") and element.IsDefinedBy:
            relations_to_remove = []
            for rel in element.IsDefinedBy:
                if rel.is_a("IfcRelDefinesByProperties") and rel.RelatingPropertyDefinition.is_a("IfcPropertySet"):
                    pset = rel.RelatingPropertyDefinition
                    if pset.Name.lower() in pset_to_delete:
                        relations_to_remove.append(rel)
                        print(f"PropertySet '{pset.Name}' found and deleted")
                        ifc_file.remove(pset)
            # Remove relationships from the element
            for rel in relations_to_remove:
                ifc_file.remove(rel)

    ifc_file.write(output_file_path)
    print(f"File successfully saved to: {output_file_path}")

