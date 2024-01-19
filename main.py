import bpy

class WM_OP_myOP(bpy.types.Operator):
    """Open dialog

    Args:
        bpy (_type_): _description_
    """
    bl_label  = "Ajustar modelo 3D"
    bl_idname = "wm.myop"

    text = bpy.props.StringProperty(name=" Enter Text", default="")


    def execute(self, context):
        return {'FINISHED'}
    
    def invoke(self,context,event):
        return context.window_manager.invoke_props_dialog(self)
    
def register():
    """Registramos la clase personalizada en Blender
    """
    bpy.utils.register_class(WM_OP_myOP)

def unregister():
    bpy.utils.unregister_class(WM_OP_myOP)

if __name__ == "__main__":
    register()
    bpy.ops.wm.myop('INVOKE_DEFAULT')

    