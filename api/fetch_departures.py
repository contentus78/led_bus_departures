from datetime import datetime, timedelta
from collections import defaultdict
from zoneinfo import ZoneInfo
from pyhafas import HafasClient
from pyhafas.profile import DBProfile
from math import floor


def fetch_departures(station_id: str, duration_minutes: int) -> list:
    try:
        client = HafasClient(profile=DBProfile())
        departures = client.departures(
            station=station_id,
            date=datetime.now(),
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
            "delay": departure.delay,
        }
        grouped_by_name[departure.name].append(departure_details)
    return grouped_by_name


def filter_departures_by_direction(data, name, directions):
    """Filters departures by direction."""
    if name not in data:
        return []
    return [entry for entry in data[name] if entry["direction"] in directions]


def calculate_departure_times(departures, current_time, str_timezone):
    """Calculates departure times considering delays."""
    timezone = ZoneInfo(str_timezone)
    results = []
    for entry in departures:
        departure_time = datetime.strptime(
            entry["dateTime"], "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=timezone)
        delay_seconds = entry["delay"].total_seconds() if entry["delay"] else 0
        delta_minutes = (
            departure_time + timedelta(seconds=delay_seconds) - current_time
        ).total_seconds() / 60
        if (delta_minutes := floor(delta_minutes)) > 0:
            results.append(delta_minutes)
    return results


def get_next_departures(data, name, directions, str_timezone):
    """Fetches next departures given data, a station name, and directions."""
    current_time = datetime.now(ZoneInfo(str_timezone))
    filtered_departures = filter_departures_by_direction(data, name, directions)
    departures = calculate_departure_times(
        filtered_departures, current_time, str_timezone
    )
    departures.sort()
    return departures


if __name__ == "__main__":
    from config.config import (
        dict_departures_to_city,
        station_id,
        duration_minutes,
        str_timezone,
    )

    departures = fetch_departures(station_id, duration_minutes)
    grouped_departures = group_departures(departures)

    departures_dict = {}
    for key, (name, direction) in dict_departures_to_city.items():
        next_departures = get_next_departures(
            grouped_departures, name, [direction], str_timezone
        )
        departures_dict[name] = next_departures

    print(departures_dict)

    # # Iterating through the dictionary and printing the results
    # for key, (name, direction) in dict_departures_to_city.items():
    #     # Using the new function names and ensuring directions are passed as a list
    #     next_departures = get_next_departures(grouped_departures, name, [direction])
    #     print(f"Departures for {name} to {direction}: {next_departures}")
