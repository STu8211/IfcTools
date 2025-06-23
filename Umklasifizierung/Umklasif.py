import ifcopenshell
import ifcopenshell.util.schema
from typing import Union  

# Main function to reassign IFC classes based on a property value
def reasign_ifc(ifc_path, save_path, attribute_name):
    # Open the IFC file
    ifc = ifcopenshell.open(ifc_path)
    
    # Helper function to get the classification value from a property set
    def get_ifc_classification(element):
        # Loop through all property definitions attached to the element
        for rel in getattr(element, "IsDefinedBy", []):
            if rel.is_a("IfcRelDefinesByProperties"):
                prop_set = rel.RelatingPropertyDefinition
                if prop_set.is_a("IfcPropertySet"):
                    for prop in prop_set.HasProperties:
                        # Check if the property name matches the user-provided attribute
                        if prop.Name == attribute_name:  # Use the user-provided attribute name
                            value = prop.NominalValue.wrappedValue
                            print(f"Element {element.GlobalId}: {attribute_name} = {value}")
                            return str(value)
        return None  # Classification not found

    # Helper function to reassign the IFC class of an element
    def reassign_class(ifc, element: ifcopenshell.entity_instance, ifc_class: str, predefined_type: str, object_type: str) -> ifcopenshell.entity_instance:
        """Reassigns the IFC class of an element in the model."""
        try:
            # Use ifcopenshell utility to change the class
            element = ifcopenshell.util.schema.reassign_class(ifc, element, ifc_class)

            # Set PredefinedType and ObjectType if available
            if hasattr(element, "PredefinedType"):
                try:
                    element.PredefinedType = predefined_type
                    element.ObjectType = object_type
                except Exception as e:
                    print(f"Error assigning PredefinedType to {element.GlobalId}: {e}")

            print(f"Element {element.GlobalId} reasign to {ifc_class} with PredefinedType {predefined_type} and ObjectType {object_type}")
            return element

        except Exception as e:
            print(f"Error reassigning class to{element.GlobalId}: {e}")
            return None

    # Get all elements of type IfcBuildingElementProxy
    elements = ifc.by_type('IfcBuildingElementProxy')

    # Loop through each element to check and reassign class
    for element in elements:
        classification = get_ifc_classification(element)
        if classification:
            try:
                # Split the classification string into class, predefined type, and object type
                ifc_class, predefined_type, object_type = classification.split('.') 
                print(f"element {element.GlobalId} reassign as {ifc_class} with PredefinedType {predefined_type} and ObjectType {object_type}")
                reassign_class(ifc, element, ifc_class, predefined_type, object_type)
            except ValueError:
                print(f"Error {element.GlobalId}: {classification}")
        else:
            print(f"Class not found for {element.GlobalId}")

    # Save the modified IFC file
    ifc.write(save_path)

# Entry point for running the script directly
if __name__ == "__main__":
    # Call the main function with example paths
    reasign_ifc("ruta/al/archivo.ifc")
