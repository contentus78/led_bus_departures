import datetime
from collections import defaultdict
from zoneinfo import ZoneInfo
from pyhafas import HafasClient
from pyhafas.profile import DBProfile
from math import floor


def fetch_departures(station_id, duration_minutes):
    try:
        client = HafasClient(profile=DBProfile())
        departures = client.departures(
            station=station_id,
            date=datetime.datetime.now(),
            duration=duration_minutes,
        )
        return departures
    except Exception as e:
        print(f"Failed to fetch departures: {e}")
        return []  # Return an empty list on failure


def group_departures(departures):
    grouped_by_name = defaultdict(list)
    for departure in departures:
        departure_details = {
            "name": departure.name,
            "direction": departure.direction,
            "dateTime": departure.dateTime.strftime("%Y-%m-%d %H:%M:%S"),
        }
        grouped_by_name[departure.name].append(departure_details)
    return grouped_by_name


def get_next_departures(data, name, directions):
    # Set the timezone to Berlin, which is the correct timezone for Germany
    timezone = ZoneInfo("Europe/Berlin")
    current_time = datetime.datetime.now(timezone)
    departures = []

    if name in data:
        for entry in data[name]:
            if (
                entry["direction"] in directions
            ):  # Check if the direction matches any in the list
                # Ensure departure_time is in the correct timezone
                departure_time = datetime.datetime.strptime(
                    entry["dateTime"], "%Y-%m-%d %H:%M:%S"
                ).replace(tzinfo=timezone)
                # Calculate the difference in minutes
                delta = (departure_time - current_time).total_seconds() / 60
                delta = floor(delta)
                # Filter to add only future departures
                if delta > 0:
                    departures.append(delta)

    departures.sort()
    return departures


if __name__ == "__main__":
    from config.dict_departures import dict_departures_to_city

    station_id = "954125"  # ID for Hermann-Liebmann/Eisenbahnstr., Leipzig
    duration_minutes = 120
    departures = fetch_departures(station_id, duration_minutes)
    grouped_departures = group_departures(departures)

    # Iterating through the dictionary and printing the results
    for key, (name, direction) in dict_departures_to_city.items():
        next_departures = get_next_departures(
            grouped_departures, name, [direction]
        )  # Make sure to pass direction in a list
        print(f"Departures for {name} to {direction}: {next_departures}")
