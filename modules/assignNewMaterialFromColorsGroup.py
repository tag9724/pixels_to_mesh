import bpy
from ..utils.toPowSquare import toPowSquare


def assignNewMaterialFromColorsGroup(bm, colors_group):

    # Name of Texture & Material
    name = "Pixels to Mesh"

    # Create new Material
    material = bpy.data.materials.new(name=name)
    material.use_nodes = True

    # Get mesh UVs Layer
    uv_layer = bm.loops.layers.uv.verify()

    # Create Texture image
    texture_dimensions = toPowSquare(len(colors_group))
    texture = bpy.data.images.new(
        name=name, height=texture_dimensions, width=texture_dimensions, alpha=True
    )

    for color in colors_group:
        group = colors_group[color]
        pixel_index = group["index"] * 4

        texture.pixels[pixel_index + 0] = group["f_rgba"][0]
        texture.pixels[pixel_index + 1] = group["f_rgba"][1]
        texture.pixels[pixel_index + 2] = group["f_rgba"][2]
        texture.pixels[pixel_index + 3] = group["f_rgba"][3]

        # UV Tile ( 8 * 8 ) = 0.125 * 0.125, middle is 0.125 / 2 = 0.0625
        uv_tile_size = 1 / texture_dimensions
        uv_tile_middle = uv_tile_size / 2

        uv_y = int(group["index"] / texture_dimensions)
        uv_x = group["index"] % texture_dimensions

        for face in group["faces"]:

            for vert in face.loops:
                vert[uv_layer].uv[0] = uv_tile_middle + uv_x * uv_tile_size
                vert[uv_layer].uv[1] = uv_tile_middle + uv_y * uv_tile_size

    # Assign texture to material
    texImage = material.node_tree.nodes.new("ShaderNodeTexImage")
    texImage.location = [-350, 300]
    texImage.image = texture

    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Specular"].default_value = 0
    bsdf.inputs["Roughness"].default_value = 1
    bsdf.inputs["Sheen Tint"].default_value = 0

    material.node_tree.links.new(bsdf.inputs["Base Color"], texImage.outputs["Color"])

    return material
