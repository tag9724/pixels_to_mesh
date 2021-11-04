import bpy

from .assignUVsFromColorsGroupAndTexture import assignUVsFromColorsGroupAndTexture
from .createNewTextureFromColorsGroupAndAssignUVs import (
    createNewTextureFromColorsGroupAndAssignUVs,
)


def assignNewMaterialFromColorsGroup(
    bm, me, colors_group, name="Pixels to Mesh", texture=None
):
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True

    # Assigns UVs ( and create texture if necessary )
    if texture == None:
        texture = createNewTextureFromColorsGroupAndAssignUVs(colors_group, bm, name)
    else:
        assignUVsFromColorsGroupAndTexture(colors_group, bm, texture)

    # Assign texture to material
    texImage = material.node_tree.nodes.new("ShaderNodeTexImage")
    texImage.location = [-350, 300]
    texImage.image = texture

    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Specular"].default_value = 0
    bsdf.inputs["Roughness"].default_value = 1
    bsdf.inputs["Sheen Tint"].default_value = 0

    material.node_tree.links.new(bsdf.inputs["Base Color"], texImage.outputs["Color"])
    me.materials.append(material)
