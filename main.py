import time
import platform
from visual_elements.sun import draw_sun
from api.weather_data import get_weather_forecast, extract_today_max_temp
from api.fetch_departures import fetch_departures, group_departures, get_next_departures
from config.config import (
    dict_departures_to_city,
    station_id,
    duration_minutes,
    str_timezone,
    longitude,
    latitude,
)


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

# sample values (not used)
sample_bus_lines = {
    " 1": [8, 18, 30, 45, 60, 75, 90, 106],
    " 3": [2, 12, 22, 36, 51, 66, 81, 97, 112],
    " 8": [14, 34, 54],
    "70": [12, 27, 42, 57, 72, 87, 103, 118],
}

sample_time = "22:35"
sample_temperature = "17°C"

# Import departure data from HafasClient
departures = fetch_departures(station_id, duration_minutes)
grouped_departures = group_departures(departures)

departures_dict = {}
for key, (name, direction) in dict_departures_to_city.items():
    next_departures = get_next_departures(
        grouped_departures, name, [direction], str_timezone
    )
    departures_dict[name] = next_departures

# Import weather data from Open-Meteo API
weather_data = get_weather_forecast(latitude, longitude, str_timezone)
temperature_data = extract_today_max_temp(weather_data)


def display_bus_times(departures, temperature_data):
    # Sort bus lines based on the next departure time, pushing empty lists to the end
    sorted_departures = {
        k: v
        for k, v in sorted(
            departures.items(),
            key=lambda item: (item[1][0] if item[1] else float("inf")),
        )
    }

    # Clear the matrix before updating
    matrix.Clear()

    # Display each line, adjust spacing according to the new font size
    for i, (line, times) in enumerate(sorted_departures.items()):
        # Extract number from the key and format it
        number = "".join(filter(str.isdigit, line))
        formatted_number = f" {number}" if len(number) == 1 else number

        # Check if there are times available
        if times:
            # Format times with leading blank space
            formatted_times = [f"{time:2}" for time in times]

            if len(times) >= 2:  # Ensure there are at least two departure times
                text = f"{formatted_number}:{formatted_times[0]} {formatted_times[1]}"
            else:  # If there's only one time
                text = f"{formatted_number}:{formatted_times[0]}"
        else:
            # Handle empty times gracefully
            text = f"{formatted_number}: "

        # Drawing text to the matrix
        graphics.DrawText(matrix, font, 2, 7 + i * 8, base_color, text)

    graphics.DrawText(matrix, font, 44, 10, base_color, temperature_data)

    draw_sun(
        matrix=matrix,
        core_start_x=51,
        core_start_y=20,
        core_size=5,
        ray_length=5,
        color=yellow,
    )


try:
    while True:
        display_bus_times(departures_dict, temperature_data)
        time.sleep(60)  # Update the display every x second
except KeyboardInterrupt:
    matrix.Clear()  # Clear the display when stopping the script
