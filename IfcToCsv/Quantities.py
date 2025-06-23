import ifcopenshell
import csv

def export_ifc_to_csvs(ifc_path, output_dir):
    ifc = ifcopenshell.open(ifc_path)

    # file 1: Psets
    with open(f"{output_dir}/quantites.csv", mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["GlobalID", "QuantitySetName", "QuantityName", "Value"])
        for elemento in ifc.by_type('IfcElement'):
            for definition in elemento.IsDefinedBy:
                if definition.is_a('IfcRelDefinesByProperties'):
                    qto = definition.RelatingPropertyDefinition
                    if qto.is_a('IfcElementQuantity'):
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
                            writer.writerow([
                                elemento.GlobalId,
                                qto.Name if hasattr(qto, 'Name') else "Not defined",
                                quantity.Name,
                                value
                            ])


if __name__ == "__main__":
    ifc_path = r"c:/Users/FlorenciaGomez/Desktop/KEM_test/KEM_DM_ARC_UK1.ifc"
    output_dir = r"c:/Users/FlorenciaGomez/Desktop/KEM_test"
    export_ifc_to_csvs(ifc_path, output_dir)