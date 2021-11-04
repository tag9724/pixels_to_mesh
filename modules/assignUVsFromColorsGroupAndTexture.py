from ..utils.getHexColorFromRgba import getHexColorFromRgba

from .getUVsTileDimensions import getUVsTileDimensions
from .assignFacesUVsFromColorGroup import assignFacesUVsFromColorGroup


def assignUVsFromColorsGroupAndTexture(colors_group, bm, texture):

    pixels = texture.pixels[:]
    pixels_amount = len(pixels)

    pixel_index = 0
    color_index = 0

    uv_layer = bm.loops.layers.uv.verify()
    uvsTileDimensions = getUVsTileDimensions(texture.size[0])

    print("\nExisting texture : width ( ", texture.size[0], " )\n")

    while pixel_index < pixels_amount:

        hex = getHexColorFromRgba(
            (
                int(pixels[pixel_index] * 255),
                int(pixels[pixel_index + 1] * 255),
                int(pixels[pixel_index + 2] * 255),
                int(pixels[pixel_index + 3] * 255),
            )
        )

        if hex in colors_group:
            assignFacesUVsFromColorGroup(
                color_group=colors_group[hex],
                uv_layer=uv_layer,
                uvsTileDimensions=uvsTileDimensions,
                color_index=color_index,
            )

        pixel_index += 4
        color_index += 1
