import ifcopenshell

# Load IFC file
input_file_path = "C:/Users/FlorenciaGomez/Desktop/SIDE_APP/IFC_filetest.ifc"
output_file_path = "C:/Users/FlorenciaGomez/Desktop/SIDE_APP/IFC_test2.ifc"

# Open IFC
ifc_file = ifcopenshell.open(input_file_path)

# Initialize a counter for the sequential numbers
counter = 1

# Iterate over all elements in the model
for element in ifc_file.by_type("IfcRoot"):
    # Get the current GUID
    current_guid = element.GlobalId
    if current_guid is not None:
        # Modify the GUID by adding a sequential number at the end, separated by "_"
        modified_guid = current_guid + "_" + str(counter)
        # Assign the modified GUID to the element
        element.GlobalId = modified_guid
        # Increment the counter
        counter += 1

ifc_file.write(output_file_path)

print(f"The modified file has been saved at: {output_file_path}")
