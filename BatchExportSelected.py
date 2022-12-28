bl_info = {
    "name": "Batch Export",
    "author": "Steven Raybell",
    "description": "Provides batch export operators of selected objects for selected formats.",
    "version": (0, 4),
    "blender": (3, 4, 0),
    "location": "File > Export",
    "category": "Import-Export"
}


import os
import bpy


PROPS = [
    ('export_normals_chk', bpy.props.BoolProperty(name='Export Normals', default=False)),
    ('export_uvs_chk', bpy.props.BoolProperty(name='Export UVs', default=False)),
    ('apply_modifiers_chk', bpy.props.BoolProperty(name='Apply Modifiers', default=True))
]


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
            export_uv=context.scene.export_uvs_chk,
            export_normals=context.scene.export_normals_chk,
            apply_modifiers=context.scene.apply_modifiers_chk,
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
    bl_options = {'REGISTER'}

    def execute(self, context):
        batch_export_obj(self, context)
        return {'FINISHED'}


class BatchExportPanel(bpy.types.Panel):
    bl_label = 'Batch Export'
    bl_idname = 'OBJECT_PT_batchexportpanel_1'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'
    bl_context = ".objectmode"

    @classmethod
    def poll(self, context):
        return context.object is not None

    def draw(self, context):

        col = self.layout.column()
        for (prop_name, _) in PROPS:
            row = col.row()
            row.prop(context.scene, prop_name)

        col.operator(
            ExportSelectedAsObjOperator.bl_idname,
            icon_value=674,
            text="Selected as OBJ")


def menu_func_export(self, context):
    self.layout.operator(ExportSelectedAsObjOperator.bl_idname)


def register():
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)

    bpy.utils.register_class(ExportSelectedAsObjOperator)
    # bpy.utils.register_class(BatchExportPreferences)
    bpy.utils.register_class(BatchExportPanel)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)

    # bpy.utils.unregister_class(BatchExportPreferences)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ExportSelectedAsObjOperator)
    bpy.utils.unregister_class(BatchExportPanel)


if __name__ == "__main__":
    register()
