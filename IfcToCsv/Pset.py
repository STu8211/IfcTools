import ifcopenshell
import csv

def export_ifc_to_csvs(ifc_path, output_dir):
    ifc = ifcopenshell.open(ifc_path)

    # file 1: Psets
    with open(f"{output_dir}/psets.csv", mode='w', newline='', encoding='utf-8') as csvfile:
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

if __name__ == "__main__":
    ifc_path = r"c:/Users/FlorenciaGomez/Desktop/KEM_test/KEM_DM_ARC_UK1.ifc"
    output_dir = r"c:/Users/FlorenciaGomez/Desktop/KEM_test"
    export_ifc_to_csvs(ifc_path, output_dir)