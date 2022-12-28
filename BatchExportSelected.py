bl_info = {
    "name": "Batch Export",
    "author": "Steven Raybell",
    "description": "Provides batch export of selected objects in common formats",
    "version": (0, 2),
    "blender": (3, 4, 0),
    "location": "File > Export",
    "category": "Import-Export"
}

import bpy
import os

def batch_export_obj(self, context):
    # Get the current blend file
    blend_file = context.blend_data

    # Check if the blend file has not been saved
    if blend_file.is_saved == False:
        # Display the alert
        self.report({'ERROR'}, "The file has not been saved. Unable to determine where to export OBJs!")
        return

    # Get the path where the blend file is located
    basedir = bpy.path.abspath('//objs/')
    
    # Check whether the specified path exists or not
    isExist = os.path.exists(basedir)
    if not isExist:
       # Create a new directory because it does not exist
       os.makedirs(basedir)

    # store selection
    obs = context.selected_objects

    # Deselect all objects
    bpy.ops.object.select_all(action='DESELECT')

    for ob in obs:
        # Select each object
        ob.select_set(True)

        # Make sure that we only export meshes
        if ob.type == 'MESH':
            # Export the currently selected object to its own file based on its name
            bpy.ops.wm.obj_export(
                filepath=os.path.join(basedir, ob.name + '.obj'),
                export_selected_objects=True,
                export_materials=False,
                export_uv=False,
                export_normals=False,
                apply_modifiers=True,
                export_eval_mode='DAG_EVAL_VIEWPORT',
                forward_axis='NEGATIVE_Z'
                )
        # Deselect the object and move on to another if any more are left
        ob.select_set(False)
        
    self.report({'INFO'}, "The operation has completed! Check in: " + basedir)

class ExportSelectedAsObjOperator(bpy.types.Operator):
    """Exports all selected objects as OBJ files"""
    bl_idname = "export.selected_as_obj"
    bl_label = "Batch Export Selected Objects as OBJ"

    def execute(self, context):
        batch_export_obj(self, context)
        return {'FINISHED'}

def menu_func_export(self, context):
    self.layout.operator(ExportSelectedAsObjOperator.bl_idname)

def register():
    bpy.utils.register_class(ExportSelectedAsObjOperator)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ExportSelectedAsObjOperator)

if __name__ == "__main__":
    register()
