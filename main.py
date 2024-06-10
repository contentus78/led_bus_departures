import time
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

# setup the matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat"
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

    core_start_x, core_start_y = 40, 17
    graphics.DrawRect(matrix, core_start_x, core_start_y, 6, 6, yellow)

    # Draw rays extending from the sun core
    # Horizontal and vertical rays
    graphics.DrawLine(matrix, 1, 7, 6, 7, yellow)
    graphics.DrawLine(matrix, 13, 7, 18, 7, yellow)
    graphics.DrawLine(matrix, 9, 1, 9, 3, yellow)
    graphics.DrawLine(matrix, 9, 10, 9, 14, yellow)

    # Diagonal rays
    graphics.DrawLine(matrix, 4, 4, 1, 1, yellow)
    graphics.DrawLine(matrix, 4, 10, 1, 13, yellow)
    graphics.DrawLine(matrix, 14, 4, 17, 1, yellow)
    graphics.DrawLine(matrix, 14, 10, 17, 13, yellow)


try:
    while True:
        display_bus_times(bus_lines)
        time.sleep(60)  # Update the display every x second
except KeyboardInterrupt:
    matrix.Clear()  # Clear the display when stopping the script
