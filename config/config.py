# HafasClient API parameters
station_id = "954125"  # ID for Hermann-Liebmann/Eisenbahnstr., Leipzig
duration_minutes = 60  # determines how far in the future the API call requests

# OpenMeteo API parameters
## Coordinates for bus stop Hermann-Liebmann-Str. / Eisenbahnstr.
latitude = 51.34549642077572
longitude = 12.405958803670908

# Parameters for output
## Dictionary to specify which directions are relevant
dict_departures_to_city = {
    1: ("STR 1", "Lausen"),
    3: ("STR 3", "Knautkleeberg"),
    8: ("STR 8", "Grünau-Nord"),
    70: ("Bus 70", "Markkleeberg, S-Bf."),
}

str_timezone = "Europe/Berlin"
