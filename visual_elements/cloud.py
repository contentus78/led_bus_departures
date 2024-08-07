import platform


# region Determine Platform
# Use platform() to determine whether script is running on Pi or dev machine
def is_development_system():
    return "x86_64" in platform.platform().lower()


if is_development_system():
    from RGBMatrixEmulator import graphics  # type: ignore
else:
    from rgbmatrix import graphics  # type: ignore
# endregion


def draw_cloud():
    pass
