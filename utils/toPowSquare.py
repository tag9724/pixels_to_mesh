import math


def toPowSquare(pixels=0):
    if pixels < 65:
        return 8

    return 2 ** math.floor(math.log2(pixels - 1) / 2 + 1)
