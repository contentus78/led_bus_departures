
def import_rgbmatrix_or_emulator():
    import platform

    # Use platform() to determine whether script is running on Pi or dev machine
    def is_development_system():
        return "x86_64" in platform.platform().lower()

    if is_development_system():
        from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics  # type: ignore
        print("Emulator imported.")
    else:
        from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics  # type: ignore
        print("RGBMatrix imported.")