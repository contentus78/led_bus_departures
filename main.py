import time

# use platform to determine whether to load emulator or hardware controls
import platform


def is_development_system():
    return "x86_64" in platform.platform().lower()


if is_development_system():
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics
else:
    from RGBMatrix import RGBMatrix, RGBMatrixOptions, graphics


# setup the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat"
options.brightness = 80
matrix = RGBMatrix(options=options)

# load font and create color
font = graphics.Font()
font.LoadFont("./fonts/5x8.bdf")
color = graphics.Color(255, 165, 0)

# Sample bus lines and their simulated departure times in minutes
bus_lines = [
    {"line": " 1", "times": [5, 15]},
    {"line": " 3", "times": [3, 13]},
    {"line": " 8", "times": [7, 17]},
    {"line": "70", "times": [1, 11]},
]

white = graphics.Color(255, 255, 255)
sample_time = "22:35"
sample_temperature = "17°C"

yellow = graphics.Color(255, 255, 0)


def display_bus_times(bus_lines):
    # Sort bus lines based on the next departure time
    bus_lines.sort(key=lambda x: x["times"][0])

    # Clear the matrix before updating
    matrix.Clear()

    # Display each line, adjust spacing according to the new font size
    for i, bus in enumerate(bus_lines):
        text = f"{bus['line']}:{' '.join(map(str, bus['times']))}"
        # Adjust the y position calculation based on the new font height
        graphics.DrawText(matrix, font, 2, 7 + i * 8, color, text)

    # Sun part
    # Display additional information
    graphics.DrawText(matrix, font, 40, 7, white, sample_time)
    graphics.DrawText(matrix, font, 40, 15, white, sample_temperature)

    core_start_x, core_start_y = 45, 20
    core_size = 6
    # Draw sun core
    for i in range(core_size):
        graphics.DrawLine(
            matrix,
            core_start_x,
            core_start_y + i,
            core_start_x + core_size - 1,
            core_start_y + i,
            yellow,
        )

    # Calculate offsets for rays based on core position
    # Horizontal rays
    graphics.DrawLine(
        matrix,
        core_start_x - 6,
        core_start_y + 2,
        core_start_x - 1,
        core_start_y + 2,
        yellow,
    )
    graphics.DrawLine(
        matrix,
        core_start_x + core_size,
        core_start_y + 2,
        core_start_x + core_size + 5,
        core_start_y + 2,
        yellow,
    )

    # Vertical rays
    graphics.DrawLine(
        matrix,
        core_start_x + 2,
        core_start_y - 3,
        core_start_x + 2,
        core_start_y - 1,
        yellow,
    )
    graphics.DrawLine(
        matrix,
        core_start_x + 2,
        core_start_y + core_size,
        core_start_x + 2,
        core_start_y + core_size + 3,
        yellow,
    )

    # Diagonal rays
    # Upper left
    graphics.DrawLine(
        matrix,
        core_start_x - 3,
        core_start_y - 3,
        core_start_x - 1,
        core_start_y - 1,
        yellow,
    )
    # Lower left
    graphics.DrawLine(
        matrix,
        core_start_x - 3,
        core_start_y + core_size + 2,
        core_start_x - 1,
        core_start_y + core_size,
        yellow,
    )
    # Upper right
    graphics.DrawLine(
        matrix,
        core_start_x + core_size + 2,
        core_start_y - 3,
        core_start_x + core_size,
        core_start_y - 1,
        yellow,
    )
    # Lower right
    graphics.DrawLine(
        matrix,
        core_start_x + core_size + 2,
        core_start_y + core_size + 2,
        core_start_x + core_size,
        core_start_y + core_size,
        yellow,
    )


try:
    while True:
        display_bus_times(bus_lines)
        time.sleep(60)  # Update the display every x second
except KeyboardInterrupt:
    matrix.Clear()  # Clear the display when stopping the script
