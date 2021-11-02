import bpy
import bpy_extras
import bmesh

from bpy.props import StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper
from bpy_extras.image_utils import load_image
from bpy.types import Operator


from .modules.assignNewMaterialFromColorsGroup import assignNewMaterialFromColorsGroup
from .modules.getColorsGroupMeshData import getColorsGroupMeshData
from .modules.createBmeshPlaneFromImageDimensions import (
    createBmeshPlaneFromImageDimensions,
)

from .utils.toPowSquare import toPowSquare


class PM_ImportImageToMesh(Operator, ImportHelper):
    """Pixels to Mesh - Create mesh with imported image"""

    bl_idname = "test.open_filebrowser"
    bl_label = "Import image as mesh"

    filter_glob: StringProperty(
        default="*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp", options={"HIDDEN"}
    )

    apply_disolve: BoolProperty(
        name="Apply disolve",
        description="Merge all square by matching colors",
        default=True,
    )

    remove_transparent_pixels: BoolProperty(
        name="Remove transparent pixels",
        description="Cut every part of the mesh where pixels are fully transparent",
        default=True,
    )

    mesh_name: StringProperty(
        name="Mesh name",
        default="Pixels to Mesh",
        description="Define the name of the generated mesh",
    )

    def execute(self, context):

        mesh_name = self.mesh_name

        image = bpy_extras.image_utils.load_image(imagepath=self.filepath)
        bm = createBmeshPlaneFromImageDimensions(image.size)
        colors_group = getColorsGroupMeshData(bm, image, self.remove_transparent_pixels)
        material = assignNewMaterialFromColorsGroup(bm, colors_group)

        # Disolve mesh if option was set
        if self.apply_disolve:
            bmesh.ops.dissolve_limit(
                bm, angle_limit=0.1, edges=bm.edges, delimit={"UV"}
            )
            bmesh.ops.dissolve_limit(
                bm, angle_limit=0.1, verts=bm.verts, delimit={"UV"}
            )

        # Finish up, write the bmesh into a new mesh
        me = bpy.data.meshes.new("Mesh")
        me.name = mesh_name
        me.materials.append(material)

        bm.to_mesh(me)
        bm.free()

        # Add the created mesh to the scene
        obj = bpy.data.objects.new(mesh_name, me)
        bpy.context.collection.objects.link(obj)

        return {"FINISHED"}
