def assignFacesUVsFromColorGroup(
    color_group, uv_layer, uvsTileDimensions, color_index=0
):

    uv_y = int(color_index / uvsTileDimensions["width"])
    uv_x = color_index % uvsTileDimensions["width"]

    for face in color_group["faces"]:

        for vert in face.loops:

            vert[uv_layer].uv[0] = (
                uvsTileDimensions["center"] + uv_x * uvsTileDimensions["size"]
            )

            vert[uv_layer].uv[1] = (
                uvsTileDimensions["center"] + uv_y * uvsTileDimensions["size"]
            )
