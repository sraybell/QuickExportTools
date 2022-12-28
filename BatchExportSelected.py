bl_info = {
    "name": "Batch Export",
    "author": "Steven Raybell",
    "description": "Provides batch export operators of selected objects for selected formats.",
    "version": (0, 3),
    # all 3.0 versions should be supported, but really it's only being tested on 3.4
    "blender": (3, 4, 0),
    "location": "File > Export",
    "category": "Import-Export"
}


import os
import bpy


def filter_selection(var):
    types = ["MESH"]
    if (var.type in types):
        return True
    else:
        return False


def batch_export_obj(self, context):
    blend_file = context.blend_data

    if blend_file.is_saved is False:
        self.report({'ERROR'}, "The file has not been saved. " +
                    "Unable to determine where to export OBJs!")
        return

    basedir = bpy.path.abspath('//objs/')
    isExist = os.path.exists(basedir)
    if not isExist:
        os.makedirs(basedir)

    # store selection
    obs = context.selected_objects

    bpy.ops.object.select_all(action='DESELECT')

    meshes = filter(filter_selection, obs)
    for mesh in meshes:
        mesh.select_set(True)

        bpy.ops.wm.obj_export(
            filepath=os.path.join(basedir, '{}.obj'.format(mesh.name)),
            export_selected_objects=True,
            export_materials=False,
            export_uv=False,
            export_normals=False,  # to keep the file smaller printing
            apply_modifiers=True,
            export_eval_mode='DAG_EVAL_VIEWPORT',
            forward_axis='NEGATIVE_Z'
        )
        # Deselect the object and move on to another if any more are left
        mesh.select_set(False)

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