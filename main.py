import time
import platform
from visual_elements.sun import draw_sun
from api.weather_data import get_weather_forecast, extract_today_max_temp


# Use platform() to determine whether script is running on Pi or dev machine
def is_development_system():
    return "x86_64" in platform.platform().lower()


if is_development_system():
    from RGBMatrixEmulator import RGBMatrix, RGBMatrixOptions, graphics  # type: ignore

    print("Development system detected, emulator imported.")
else:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics  # type: ignore

    print("Production system detected, RGBMatrix imported.")


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
base_color = graphics.Color(255, 165, 0)
white = graphics.Color(255, 255, 255)
yellow = graphics.Color(255, 255, 0)
# green for 1, 3 box: (101, 179, 46)

# Define sample values
bus_lines = [
    {"line": " 1", "times": [5, 15]},
    {"line": " 3", "times": [3, 13]},
    {"line": " 8", "times": [7, 17]},
    {"line": "70", "times": [1, 11]},
]
sample_time = "22:35"
sample_temperature = "17°C"

# Import weather data from Open-Meteo API
# Coordinates for bus stop Hermann-Liebmann-Str. / Eisenbahnstr.
latitude = 51.34549642077572
longitude = 12.405958803670908
timezone = "Europe/Berlin"

weather_data = get_weather_forecast(latitude, longitude, timezone)
temperature_data = extract_today_max_temp(weather_data)


def display_bus_times(bus_lines, temperature_data):
    # Sort bus lines based on the next departure time
    bus_lines.sort(key=lambda x: x["times"][0])

    # Clear the matrix before updating
    matrix.Clear()

    # Display each line, adjust spacing according to the new font size
    for i, bus in enumerate(bus_lines):
        text = f"{bus['line']}:{' '.join(map(str, bus['times']))}"
        # Adjust the y position calculation based on the new font height
        graphics.DrawText(matrix, font, 2, 7 + i * 8, base_color, text)

    graphics.DrawText(matrix, font, 41, 10, base_color, temperature_data)

    draw_sun(
        matrix=matrix,
        core_start_x=45,
        core_start_y=20,
        core_size=5,
        ray_length=5,
        color=yellow,
    )


try:
    while True:
        display_bus_times(bus_lines, temperature_data)
        time.sleep(60)  # Update the display every x second
except KeyboardInterrupt:
    matrix.Clear()  # Clear the display when stopping the script
