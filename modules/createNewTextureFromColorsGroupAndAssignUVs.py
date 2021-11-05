import bpy

from ..utils.toPowSquare import toPowSquare

from .getUVsTileDimensions import getUVsTileDimensions
from .assignFacesUVsFromColorGroup import assignFacesUVsFromColorGroup


def createNewTextureFromColorsGroupAndAssignUVs(
    colors_group, bm, name="Pixels to Mesh"
):
    uv_layer = bm.loops.layers.uv.verify()

    dimensions = toPowSquare(len(colors_group))
    uvsTileDimensions = getUVsTileDimensions(dimensions, dimensions)

    texture = bpy.data.images.new(
        name=name, height=dimensions, width=dimensions, alpha=True
    )

    for color in colors_group:
        color_group = colors_group[color]
        pixel_index = color_group["index"] * 4

        texture.pixels[pixel_index + 0] = color_group["f_rgba"][0]
        texture.pixels[pixel_index + 1] = color_group["f_rgba"][1]
        texture.pixels[pixel_index + 2] = color_group["f_rgba"][2]
        texture.pixels[pixel_index + 3] = color_group["f_rgba"][3]

        assignFacesUVsFromColorGroup(
            color_group=color_group,
            uv_layer=uv_layer,
            uvsTileDimensions=uvsTileDimensions,
            color_index=color_group["index"],
        )

    return texture
