def getUVsTileDimensions(texture_width=8, texture_height= 8):
    uv_tile_size = 1 / texture_width
    uv_tile_center = uv_tile_size / 2

    # BUG: replace size with tile.width & tile.heigth, Non squared texture don't work
    return {"size": uv_tile_size, "center": uv_tile_center, "width": texture_width}
