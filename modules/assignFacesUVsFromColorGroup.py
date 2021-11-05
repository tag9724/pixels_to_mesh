def assignFacesUVsFromColorGroup(
    color_group, uv_layer, uvsTileDimensions, color_index=0
):

    uv_y = int(color_index / uvsTileDimensions["width"])
    uv_x = color_index % uvsTileDimensions["width"]

    for face in color_group["faces"]:

        for vert in face.loops:

            vert[uv_layer].uv[0] = (
                uvsTileDimensions["tile_x_center"]
                + uv_x * uvsTileDimensions["tile_x_size"]
            )

            vert[uv_layer].uv[1] = (
                uvsTileDimensions["tile_y_center"]
                + uv_y * uvsTileDimensions["tile_y_size"]
            )
