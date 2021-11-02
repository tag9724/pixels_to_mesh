bl_info = {
    "name": "Pixels to Mesh",
    "author": "tag9724",
    "description": "Convert an image to a mesh",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "",
    "warning": "",
    "category": "Generic",
}


import bpy
from .PM_ImportImageToMesh import PM_ImportImageToMesh


def import_menu_func(self, context):
    self.layout.separator()
    self.layout.operator(PM_ImportImageToMesh.bl_idname, icon="IMAGE_RGB_ALPHA")


def register():
    bpy.utils.register_class(PM_ImportImageToMesh)
    bpy.types.VIEW3D_MT_mesh_add.append(import_menu_func)


def unregister():
    bpy.utils.unregister_class(PM_ImportImageToMesh)
    bpy.types.VIEW3D_MT_mesh_add.remove(import_menu_func)
