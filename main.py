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
import logging
from logging.handlers import RotatingFileHandler


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

# load font
font = graphics.Font()
font.LoadFont("./fonts/5x8.bdf")

# create color
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
# departures = fetch_departures(station_id, duration_minutes)
# grouped_departures = group_departures(departures)

# Import weather data from Open-Meteo API
weather_data = get_weather_forecast(latitude, longitude, str_timezone)
temperature_data = extract_today_max_temp(weather_data)


def sort_departures(departures):
    return {
        k: v
        for k, v in sorted(
            departures.items(),
            key=lambda item: (item[1][0] if item[1] else float("inf")),
        )
    }


def update_departure_times(matrix, font, base_color, sorted_departures):
    # Assuming the matrix has specific methods to redraw areas; if not, you will need custom logic.
    for i, (line, times) in enumerate(sorted_departures.items()):
        number = "".join(filter(str.isdigit, line))
        formatted_number = f" {number}" if len(number) == 1 else number

        text = f"{formatted_number}:"
        if times:
            formatted_times = [f"{time:2}" for time in times]
            if len(times) >= 2:
                text += f"{formatted_times[0]} {formatted_times[1]}"
            else:
                text += f"{formatted_times[0]}"

        # Redraw only the line where changes occur
        graphics.DrawText(matrix, font, 2, 7 + i * 8, base_color, text)


def display_static_elements(matrix, font, base_color, temperature_data):
    graphics.DrawText(matrix, font, 44, 10, base_color, temperature_data)
    draw_sun(matrix, 51, 20, 5, 5, yellow)


def setup_logging():
    logger = logging.getLogger("MyAppLogger")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler("my_app.log", maxBytes=10240, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def main_display_loop(
    matrix,
    station_id,
    duration_minutes,
    dict_departures_to_city,
    str_timezone,
    departures_api_interval,
    weather_api_interval,
    update_interval,
    logger,
):
    logger.info("Starting the display loop")
    last_departures_api_call = 0
    last_weather_api_call = 0
    last_update = 0
    grouped_departures = None
    departures_dict = {}
    previous_sorted_departures = {}

    try:
        while True:
            current_time = time.time()

            if current_time - last_departures_api_call > departures_api_interval:
                try:
                    departures = fetch_departures(station_id, duration_minutes)
                    grouped_departures = group_departures(departures)
                    last_departures_api_call = current_time
                    logger.info("Departures data fetched successfully")
                except Exception as e:
                    logger.error(f"API ERROR (Departures): {e}")

            if current_time - last_weather_api_call > weather_api_interval:
                try:
                    weather_data = get_weather_forecast(
                        latitude, longitude, str_timezone
                    )
                    temperature_data = extract_today_max_temp(weather_data)
                    last_weather_api_call = current_time
                    logger.info("Weather data fetched successfully")
                except Exception as e:
                    logger.error(f"W_API ERROR (Weather): {e}")

            if grouped_departures and current_time - last_update > update_interval:
                # matrix.Clear()

                for key, (name, direction) in dict_departures_to_city.items():
                    next_departures = get_next_departures(
                        grouped_departures, name, [direction], str_timezone
                    )
                    departures_dict[name] = next_departures

                current_sorted_departures = sort_departures(departures_dict)
                if current_sorted_departures != previous_sorted_departures:
                    # this is where the previous results need to be cleared first (or in the following function)
                    matrix.Clear()
                    update_departure_times(
                        matrix, font, base_color, current_sorted_departures
                    )
                    # update other elements
                    display_static_elements(matrix, font, base_color, temperature_data)
                    previous_sorted_departures = current_sorted_departures
                last_update = current_time
                logger.debug("Display updated")

            time.sleep(1)

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
    finally:
        logger.info("Shutting down the display loop")


# Use the setup_logging function at the start of your application
logger = setup_logging()

# Constants for intervals
DEPARTURES_API_CALL_INTERVAL = 120  # 2 minutes
WEATHER_API_CALL_INTERVAL = 60 * 60 * 6  # every 6 hours
UPDATE_INTERVAL = 10  # 10 seconds

# Start the display loop
main_display_loop(
    matrix,
    station_id,
    duration_minutes,
    dict_departures_to_city,
    str_timezone,
    DEPARTURES_API_CALL_INTERVAL,
    WEATHER_API_CALL_INTERVAL,
    UPDATE_INTERVAL,
    logger,
)
