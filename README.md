# LED Display Bus Departures
A little project to display bus departure times and weather information on a LED panel. The project uses the Hafas API to fetch live departure data and open-meteo for live weather data. Data and display are refreshed every full minute.

## How to install and run
- Software: requirements.txt contains dependencies
- Hardware used:
    - Raspberry Pi Zero WH
    - Adafruit RGB Matrix Bonnet
    - Adafruit 64x32 RGB LED Matrix 5mm Grid

The project can be run without a LED Panel using the RGBMatrixEmulator library. In this case a LED board is simulated in the browser.
The script uses a simple function to determine if it runs on x86_64 (my development system, your setup might differ) and decides which library to load.

## To-do
- Automatic shutdown of the panel or brightness reduction during night
- Individual colored frames for line numbers for better recognition
- Additional weather symbols and connection to existing weather API
    - Cloud
    - Cloud with light rain
    - Cloud with heavy rain
    - Cloud with rain and lightning
    - Cloud with snow

## Nice to have / Undecided
- Is rounding down for the departure times the right call? Edge Case 2:59, appears as 2min = unreachable but is actually reachable
- Different color when departure is delayed?
- Display current time?
- Animations for weather symbols?