import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator, Scene

from bpy_extras.io_utils import ImportHelper
from bpy_extras.image_utils import load_image

from bmesh.ops import dissolve_limit

from .modules.assignNewMaterialFromColorsGroup import assignNewMaterialFromColorsGroup
from .modules.assignUVsFromColorsGroupAndTexture import (
    assignUVsFromColorsGroupAndTexture,
)
from .modules.getColorsGroupMeshData import getColorsGroupMeshData
from .modules.createBmeshPlaneFromImageDimensions import (
    createBmeshPlaneFromImageDimensions,
)


class PM_ImportImageToMesh(Operator, ImportHelper):
    """Pixels to Mesh - Create mesh with imported image"""

    bl_idname = "object.import_image_to_mesh"
    bl_label = "Import image to mesh"
    bl_description = "Test Operator"
    bl_options = {"REGISTER", "UNDO"}

    filter_glob: StringProperty(
        default="*.jpg;*.jpeg;*.png;*.tif;*.tiff;*.bmp", options={"HIDDEN"}
    )

    mesh_name: StringProperty(
        name="Mesh Name",
        default="Pixels to Mesh",
        description="Define the name of the generated mesh",
    )
    apply_disolve: BoolProperty(
        name="Apply disolve",
        description="Merge all square by matching colors",
        default=False,
    )
    remove_transparent_pixels: BoolProperty(
        name="Remove transparent pixels",
        description="Cut every part of the mesh where pixels are fully transparent",
        default=True,
    )

    existing_material: StringProperty(
        name="Assign existing material",
        description="Instead of generating a new material the one selected here will be set on the Mesh."
        + "\nLeave blank to generate a new material automatically."
        + "\n\nNote that no texture will be generated and no UVs will be set unless you also set a existing texture to use in the settings.",
    )
    existing_texture: StringProperty(
        name="Assign existing texture",
        description=""
        + "The generated material will use this texture, all UVs are going to be set based on it."
        + "\nLeave blank to generate a new texture automatically."
        + "\n\nNote that if you also define a existing material to apply on the mesh only UVs will be generated, "
        + "the texture will not be assigned on the material.",
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        box.label(text="Mesh Name")
        box.prop(self, "mesh_name", icon_only=True)
        box.prop(self, "apply_disolve")
        box.prop(self, "remove_transparent_pixels")

        layout.separator()
        layout.label(text="Advanced settings")

        box = layout.box()
        box.label(text="Assign existing material ( Optional )")
        box.prop_search(self, "existing_material", bpy.data, "materials", text="")

        box.label(text="Assign existing texture ( Optional )")
        box.prop_search(self, "existing_texture", bpy.data, "images", text="")

    def execute(self, context):
        mesh_name = self.mesh_name
        existing_material = bpy.data.materials.get(self.existing_material)
        existing_texture = bpy.data.images.get(self.existing_texture)

        image = load_image(imagepath=self.filepath)
        bm = createBmeshPlaneFromImageDimensions(image.size)
        colors_group = getColorsGroupMeshData(bm, image, self.remove_transparent_pixels)

        # Create 3D object
        me = bpy.data.meshes.new("Mesh")
        me.name = mesh_name

        # Create a new material or use the one set in settings
        if existing_material:
            me.materials.append(existing_material)

            if existing_texture:
                assignUVsFromColorsGroupAndTexture(
                    colors_group=colors_group, bm=bm, texture=existing_texture
                )

        else:
            assignNewMaterialFromColorsGroup(
                bm=bm,
                me=me,
                colors_group=colors_group,
                name=mesh_name,
                texture=existing_texture,
            )

        # Disolve mesh if option was set
        if self.apply_disolve:
            dissolve_limit(bm, angle_limit=0.1, edges=bm.edges, delimit={"UV"})
            dissolve_limit(bm, angle_limit=0.1, verts=bm.verts, delimit={"UV"})

        # Add the mesh and free bmesh instance
        bm.to_mesh(me)
        bm.free()

        # Add the created mesh to the scene
        obj = bpy.data.objects.new(mesh_name, me)
        bpy.context.collection.objects.link(obj)

        # Free image from Blend file
        bpy.data.images.remove(image)

        return {"FINISHED"}
