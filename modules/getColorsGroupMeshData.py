import bmesh


def getColorsGroupMeshData(bm, image, should_remove_transparent=False):

    """Return colors_group {
        "faces": List,
        "hex": String,
        "rgba": Tuple,
        "f_rgba": Tuple,
    }
    """

    pixels = image.pixels[:]
    pixel_index = 0

    colors_group = {}
    delete_faces = []
    color_index = 0

    # Get list of faces by identical colors

    for face in bm.faces:

        f_rgba = (
            pixels[pixel_index + 0],
            pixels[pixel_index + 1],
            pixels[pixel_index + 2],
            pixels[pixel_index + 3],
        )

        rgba = (
            int(f_rgba[0] * 255),
            int(f_rgba[1] * 255),
            int(f_rgba[2] * 255),
            int(f_rgba[3] * 255),
        )

        pixel_index += 4

        # Transparent pixels will be removed
        if should_remove_transparent and rgba[3] <= 0:
            delete_faces.append(face)
            continue

        color = "#{:02x}{:02x}{:02x}{:02x}".format(rgba[0], rgba[1], rgba[2], rgba[3])

        # Append new entry in colors_group
        if colors_group.get(color) == None:
            colors_group[color] = {
                "index": color_index,
                "faces": [face],
                "hex": color,
                "rgba": rgba,
                "f_rgba": f_rgba,
            }

            color_index += 1

        # Just add current face in existing colors_group data
        else:
            colors_group[color]["faces"].append(face)

    # Delete Transparent faces
    if should_remove_transparent:
        bmesh.ops.delete(bm, geom=delete_faces, context="FACES")

    return colors_group
