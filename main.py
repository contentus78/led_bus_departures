import time
import platform
from visual_elements.sun import draw_sun
from visual_elements.cloud import draw_cloud
from api.weather_data import (
    get_weather_forecast,
    extract_today_max_temp,
    extract_current_temp,
)
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


def sort_departures(departures):
    return {
        k: v
        for k, v in sorted(
            departures.items(),
            key=lambda item: (item[1][0] if item[1] else float("inf")),
        )
    }


def update_departure_times(matrix, font, base_color, sorted_departures):
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

        graphics.DrawText(matrix, font, 2, 7 + i * 8, base_color, text)


def draw_temperature_output(matrix, font, base_color, temperature_data):
    graphics.DrawText(matrix, font, 44, 10, base_color, temperature_data)


def draw_weather_symbol():
    # draw_cloud()
    draw_sun(matrix, 51, 20, 5, 5, yellow)
    # More weather symbols and API input to decide between them missing for the moment


def setup_logging():
    logger = logging.getLogger("MyAppLogger")
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler("my_app.log", maxBytes=10240, backupCount=3)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


class DisplayController:
    def __init__(
        self, matrix, station_id, duration_minutes, city_departures, timezone, logger
    ):
        self.matrix = matrix
        self.station_id = station_id
        self.duration_minutes = duration_minutes
        self.city_departures = city_departures
        self.timezone = timezone
        self.logger = logger
        self.grouped_departures = None
        self.departures_dict = {}
        self.sorted_departures = {}
        self.temperature_data = None

    def fetch_and_group_departures(self):
        try:
            departures = fetch_departures(self.station_id, self.duration_minutes)
            self.grouped_departures = group_departures(departures)
            self.logger.debug("Departures data fetched successfully")
        except Exception as e:
            self.logger.error(f"API ERROR (Departures): {e}")

    def fetch_weather_data(self):
        try:
            weather_data = get_weather_forecast(latitude, longitude, self.timezone)
            # self.temperature_data = extract_today_max_temp(weather_data)
            self.temperature_data = extract_current_temp(weather_data)
            self.logger.debug("Weather data fetched successfully")
        except Exception as e:
            self.logger.error(f"API ERROR (Weather): {e}")

    def calculate_next_departures(self):
        try:
            for key, (name, direction) in self.city_departures.items():
                next_departures = get_next_departures(
                    self.grouped_departures, name, [direction], self.timezone
                )  # pass [direction] as list because function expects list of directions
                self.departures_dict[name] = next_departures
        except Exception as e:
            self.logger.error(f"Error while calculating next departures: {e}")

    def sort_next_departures(self):
        self.sorted_departures = sort_departures(self.departures_dict)

    def update_display(self):
        self.matrix.Clear()
        update_departure_times(self.matrix, font, base_color, self.sorted_departures)
        draw_temperature_output(self.matrix, font, base_color, self.temperature_data)
        draw_weather_symbol()

    def run(self):
        """
        APIs are fetched once every minute 10 seconds before the full minute.
        The screen is updated at 01 seconds of every full minute.
        This interval was chosen since minute is the maximum granularity available in the data.
        """
        self.logger.info("Starting the display loop")
        # Display startup message
        graphics.DrawText(matrix, font, 2, 22, yellow, "WaitforAPI...")

        try:
            while True:

                current_time = time.localtime()
                seconds_till_50 = 50 - current_time.tm_sec
                if seconds_till_50 < 0:
                    seconds_till_50 += 60  # correct for negative values
                time.sleep(seconds_till_50)

                self.fetch_and_group_departures()
                self.fetch_weather_data()

                current_time = time.localtime()
                seconds_till_01 = 60 - current_time.tm_sec
                time.sleep(seconds_till_01)

                self.calculate_next_departures()
                self.sort_next_departures()
                self.update_display()  # Since I do not know if partial updates are possible, one method for all
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
        finally:
            self.logger.info("Shutting down the display loop")


# Execute script:
logger = setup_logging()

controller = DisplayController(
    matrix, station_id, duration_minutes, dict_departures_to_city, str_timezone, logger
)

controller.run()
