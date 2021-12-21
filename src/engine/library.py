def is_surface_empty(surface):
    width, height = surface.get_size()
    if colorkey := surface.get_colorkey():
        for i in range(width):
            for j in range(height):
                if surface.get_at((i, j)) != colorkey:
                    return False
    else:
        for i in range(width):
            for j in range(height):
                if surface.get_at((i, j))[3] != 255:
                    return False
    return True
