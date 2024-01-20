import bpy
from bpy.props import (StringProperty,
                       PointerProperty,
                       BoolProperty
                       )

from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )
                       
class MyProperties(PropertyGroup):
    path : StringProperty(
        name="",
        description="Path to File",
        default="*.dae",
        maxlen=1024,
        subtype='FILE_PATH')

    import_units: BoolProperty(
        name="keepUnits",
        default=True,
        description="Mantener Unidades."
    )
    
    repair_mesh: BoolProperty(
        name="fixMesh",
        default=True,
        description="Repara las mallas en la importacion."
    )
    
    merge_repeated_materials: BoolProperty(
        name="fixMesh",
        default=True,
        description="Fusionar materiales repetidos"
    )

    repair_alpha_channel: BoolProperty(
        name="repair_alfa_channel",
        default=True,
        description="Repara el canal alfa."
    )

class OBJECT_OT_RevitDAEImportOperator(bpy.types.Operator):
    bl_idname = "wm.revit_dae_import_operator"
    bl_label = "Importar .dae"

    def execute(self, context):
        # Aquí colocas la lógica de importación
        path = bpy.context.scene.my_tool.path
        repair_mesh = bpy.context.scene.my_tool.repair_mesh
        repair_alpha_channel = bpy.context.scene.my_tool.repair_alpha_channel
        import_units = bpy.context.scene.my_tool.import_units
        merge_materials = bpy.context.scene.my_tool.merge_repeated_materials

        print(f"Importando {path}")
        print(f"Reparar Mallas: {repair_mesh}")
        print(f"Reparar Canal Alfa: {repair_alpha_channel}")

        # Logica de importacion
        bpy.ops.wm.collada_import(filepath=path, import_units=import_units)


        if repair_mesh:  
            repair_meshes_in_project()
       
        if repair_alpha_channel:
           repair_alfa_channel_in_project()

        if merge_materials:
            merge_duplicate_materials()

        return {'FINISHED'}
  
class OBJET_REVIT_DAE_ImportTool(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Revir Import Tool"
    bl_idname = "OBJET_REVIT_DAE_ImportTool"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Revit Import Tool'

    def draw(self, context):
        layout = self.layout
        scn = context.scene
        col = layout.column(align=True)

        # Primer grupo de layout_box
        box = layout.box()
        box.label(text="Ruta al archivo .dae:")
        box.prop(scn.my_tool, "path", text="")

        # Segundo grupo de layout_box
        box = layout.box()
        box.label(text="Opciones:")
        box.prop(scn.my_tool, "import_units", text="Mantener unidades")
        box.prop(scn.my_tool, "repair_mesh", text="Reparar mallas")
        box.prop(scn.my_tool, "repair_alpha_channel", text="Reparar canal alfa")
        box.prop(scn.my_tool, "merge_repeated_materials", text="Fusionar materiales repetidos")

        # Agrega un botón de importación
        layout.operator("wm.revit_dae_import_operator", text="Importar")
                
        # print the path to the console
        print (scn.my_tool.path)

classes = (
    MyProperties,
    OBJET_REVIT_DAE_ImportTool
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)
    register_class(OBJECT_OT_RevitDAEImportOperator)
    
    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    unregister_class(OBJECT_OT_RevitDAEImportOperator)
    del bpy.types.Scene.my_tool


# Metodos:
    
def repair_alfa_channel_in_project():
    # Selecciona el objeto activo
    obj = bpy.context.active_object

    # Activa el modo de edición
    bpy.ops.object.mode_set(mode='EDIT')

    # Selecciona todos los vértices
    bpy.ops.mesh.select_all(action='SELECT')

    # Remueve los vértices duplicados
    bpy.ops.mesh.remove_doubles()

    # Desactiva el modo de edición
    bpy.ops.object.mode_set(mode='OBJECT')
    pass

def repair_meshes_in_project():
    # Obtener la lista de todos los materiales en la escena
    materiales = bpy.data.materials

    # Iterar sobre cada material
    for material in materiales:
        # Verificar si el material tiene un nodo Principled BSDF 
        # (Puede variar según el tipo de material que estés usando)
        if material.use_nodes:
        # Obtener el nodo Principled BSDF
            principled_node = material.node_tree.nodes.get("Principled BSDF")
            # Verificar si el nodo Principled BSDF existe en el material
            if principled_node:
                # Configurar el canal alfa del nodo Principled BSDF a 1
                principled_node.inputs["Alpha"].default_value = 1
                # Configurar Roughness:
                principled_node.inputs["Roughness"].default_value = 1
                # Configurar metallic:
                principled_node.inputs["Metallic"].default_value = 0

def merge_duplicate_materials():
    # Obtener la lista de todos los objetos en la escena
    all_objects = bpy.context.scene.objects

    # Diccionario para almacenar material_name: material
    material_dict = {}

    # Iterar sobre todos los objetos
    for obj in all_objects:
        if obj.type == 'MESH':
            # Iterar sobre los materiales del objeto
            for slot_index, material_slot in enumerate(obj.material_slots):
                if material_slot.material:
                    material_name = material_slot.material.name

                    # Verificar si el material ya existe en el diccionario
                    if material_name not in material_dict:
                        material_dict[material_name] = material_slot.material

                    # Asignar el material del diccionario al objeto
                    obj.material_slots[slot_index].material = material_dict[material_name]

    # Eliminar los materiales duplicados
    for material in bpy.data.materials:
        if material.users == 0:
            bpy.data.materials.remove(material)


if __name__ == "__main__":
    register()
