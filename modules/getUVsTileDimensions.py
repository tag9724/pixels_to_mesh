def getUVsTileDimensions(texture_width=8, texture_height=8):
    tile_x_size = 1 / texture_width
    tile_x_center = tile_x_size / 2

    tile_y_size = 1 / texture_height
    tile_y_center = tile_y_size / 2

    return {
        "width": texture_width,
        "height": texture_height,
        "tile_x_size": tile_x_size,
        "tile_x_center": tile_x_center,
        "tile_y_size": tile_y_size,
        "tile_y_center": tile_y_center,
    }
