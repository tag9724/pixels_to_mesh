from ..utils.getHexColorFromRgba import getHexColorFromRgba

from .getUVsTileDimensions import getUVsTileDimensions
from .assignFacesUVsFromColorGroup import assignFacesUVsFromColorGroup


def assignUVsFromColorsGroupAndTexture(colors_group, bm, texture):

    pixels = texture.pixels[:]
    pixels_amount = len(pixels)

    pixel_index = 0
    color_index = 0

    hexs_set = set()

    uv_layer = bm.loops.layers.uv.verify()
    uvsTileDimensions = getUVsTileDimensions(texture.size[0], texture.size[1])

    while pixel_index < pixels_amount:

        hex = getHexColorFromRgba(
            (
                int(pixels[pixel_index] * 255),
                int(pixels[pixel_index + 1] * 255),
                int(pixels[pixel_index + 2] * 255),
                int(pixels[pixel_index + 3] * 255),
            )
        )

        if hex not in hexs_set and hex in colors_group:

            # Make sure we don't add UVs twice for the same color
            hexs_set.add(hex)

            assignFacesUVsFromColorGroup(
                color_group=colors_group[hex],
                uv_layer=uv_layer,
                uvsTileDimensions=uvsTileDimensions,
                color_index=color_index,
            )

        pixel_index += 4
        color_index += 1
