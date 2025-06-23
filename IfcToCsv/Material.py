import ifcopenshell
import csv

def export_ifc_to_csvs(ifc_path, output_dir):
    ifc = ifcopenshell.open(ifc_path)
    with open(f"{output_dir}/materials_by_element.csv", mode='w', newline='', encoding='utf-8') as csvfile:
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
                writer.writerow([
                    elemento.GlobalId if hasattr(elemento, 'GlobalId') else "Not defined",
                    elemento.is_a() if hasattr(elemento, 'is_a') else "Not defined",
                    elemento.Name if hasattr(elemento, 'Name') else "Not defined",
                    mat_name
                ])

if __name__ == "__main__":
    ifc_path = r'C:\Users\FlorenciaGomez\SIDE\SIDE - Team\17_Severin\05_KI\IFC Models for Training\_IFC-Modelle nach Autorensoftware\Allplan_1300_TWP_B+P_5_F.ifc'
    output_dir = r"c:/Users/FlorenciaGomez/Desktop/KEM_test"
    export_ifc_to_csvs(ifc_path, output_dir)