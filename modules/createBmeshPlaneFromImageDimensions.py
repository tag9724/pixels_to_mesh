import bmesh


def createBmeshPlaneFromImageDimensions(dimensions=[0, 0]):

    """Return bmesh plane instance"""

    # Create Bmesh instance
    bm = bmesh.new()

    size = 0
    scale = (0, 0, 0)

    if dimensions[0] > dimensions[1]:
        scale = (dimensions[0] / dimensions[1], 1, 1)
        size = 0.25 * dimensions[0]

    else:
        scale = (1, dimensions[1] / dimensions[0], 1)
        size = 0.25 * dimensions[1]

    # Create Grid Geometry
    bmesh.ops.create_grid(
        bm, size=size, x_segments=dimensions[0] + 1, y_segments=dimensions[1] + 1
    )

    # Apply Scale to ensure tile are squared
    bmesh.ops.scale(bm, vec=scale, verts=bm.verts)

    return bm
