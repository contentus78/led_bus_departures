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
color = graphics.Color(255, 255, 255)

# Sample bus lines and their simulated departure times in minutes
bus_lines = [
    {"line": "Tram 1", "times": [5, 15]},
    {"line": "Tram 3", "times": [3, 13]},
    {"line": "Tram 8", "times": [7, 17]},
    {"line": "Bus 70", "times": [1, 11]},
]


def display_bus_times(bus_lines):
    # Sort bus lines based on the next departure time
    # bus_lines.sort(key=lambda x: x["times"][0])

    # Clear the matrix before updating
    matrix.Clear()

    # Display each line, adjust spacing according to the new font size
    for i, bus in enumerate(bus_lines):
        text = f"{bus['line']}: {' '.join(map(str, bus['times']))} min"
        # Adjust the y position calculation based on the new font height
        graphics.DrawText(matrix, font, 2, 7 + i * 8, color, text)


try:
    while True:
        display_bus_times(bus_lines)
        time.sleep(60)  # Update the display every x second
except KeyboardInterrupt:
    matrix.Clear()  # Clear the display when stopping the script
