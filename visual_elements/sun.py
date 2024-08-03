import platform

# Use platform() to determine whether script is running on Pi or dev machine
def is_development_system():
    return "x86_64" in platform.platform().lower()

if is_development_system():
    from RGBMatrixEmulator import graphics  # type: ignore
else:
    from rgbmatrix import graphics  # type: ignore


def draw_sun(matrix, core_start_x, core_start_y, core_size, ray_length, color):
    '''
    core_start: position of left top pixel of sun core
    core_size: pixel length of core side, shoud preferably be odd for symmetry
    '''
    # Draw sun core
    for i in range(core_size):
        graphics.DrawLine(
            matrix,
            core_start_x,
            core_start_y + i,
            core_start_x + core_size -1,
            core_start_y + i,
            color
        )

    # Draw horizontal rays (start in the middle at half core size)
    ## Left ray
    graphics.DrawLine(
        matrix,
        core_start_x - ray_length,
        core_start_y + core_size / 2,
        core_start_x - 1,
        core_start_y + core_size / 2,
        color,
    )

    ## Right ray
    graphics.DrawLine(
        matrix,
        core_start_x + core_size,
        core_start_y + core_size / 2,
        core_start_x + core_size + ray_length -1,
        core_start_y + core_size / 2,
        color,
    )

    # Draw vertical rays
    ## Top ray
    graphics.DrawLine(
        matrix,
        core_start_x + core_size / 2,
        core_start_y - 1,
        core_start_x + core_size / 2,
        core_start_y - ray_length,
        color,
    )

    ## Bottom ray
    graphics.DrawLine(
        matrix,
        core_start_x + core_size / 2,
        core_start_y + core_size,
        core_start_x + core_size / 2,
        core_start_y + core_size + ray_length -1,
        color,
    )
    
    # Diagonal rays
    ## Upper left ray
    graphics.DrawLine(
        matrix,
        core_start_x - ray_length / 2 - 1,
        core_start_y - ray_length / 2 - 1,
        core_start_x - 1,
        core_start_y - 1,
        color,
    )

    ## Lower left ray
    graphics.DrawLine(
        matrix,
        core_start_x - ray_length / 2 - 1,
        core_start_y + core_size + 1 + ray_length / 2,
        core_start_x -1,
        core_start_y + core_size,
        color,
    )

    ## Upper right ray
    graphics.DrawLine(
        matrix,
        core_start_x + core_size,
        core_start_y - 1,
        core_start_x + core_size + ray_length / 2 + 1,
        core_start_y - ray_length / 2 - 1,
        color,
    )

    ## Lower right ray
    graphics.DrawLine(
        matrix,
        core_start_x + core_size,
        core_start_y + core_size,
        core_start_x + core_size + ray_length / 2 + 1,
        core_start_y + core_size + ray_length / 2 + 1,
        color,
    )
    