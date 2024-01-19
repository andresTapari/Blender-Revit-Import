from importDaePanel import (register_class,classes,OBJECT_OT_RevitDAEImportOperator)
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

bl_info = {
    "name": "Revir Import Tool",
    "blender": (3, 0, 0),
    "category": "Import-Export",
    "location": "File > Import-Export",
    "description": "Addon para importar archivos .dae con opciones adicionales de correccion de geomterias, mallas y materiales.",
    "author": "AndresTapa",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "support": "COMMUNITY",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"
}

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
    