def getHexColorFromRgba(rgba=(0, 0, 0, 0)):
    """
    Return Hex string including alpha channel

    :params tuple rgba: RGBA int values [0,255]
    """
    return "#{:02x}{:02x}{:02x}{:02x}".format(rgba[0], rgba[1], rgba[2], rgba[3])
