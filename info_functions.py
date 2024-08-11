import csv
from datetime import datetime, timedelta
import os
import json

# List of month names to match the file naming convention
month_names = [
    "august",
    "september",
    "october",
    "november",
    "december",
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
]


def parse_time(year, month, day_number, time_str):
    """Helper function to parse time from the CSV and convert it into a datetime object."""
    date_str = f"{year}-{month:02d}-{int(day_number):02d}"
    time_format = "%Y-%m-%d %H:%M"

    # Handle cases where the time is 'NC'
    if time_str == "NC":
        return None

    return datetime.strptime(f"{date_str} {time_str}", time_format)


def get_event_infos_for_file(csv_file, year, month):
    events = []

    if not os.path.exists(csv_file):
        print(f"CSV file {csv_file} not found.")
        return events

    with open(csv_file, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            day_number = row["Day Number"]

            # High Tide 1
            high_tide1_time = parse_time(
                year, month, day_number, row["High tide"].split()[0]
            )
            if high_tide1_time:
                high_tide1_height = row["High tide"].split()[1]
                coef1 = row["Coef"]
                event_info_high1 = {
                    "summary": f"High Tide ({high_tide1_height}) coef {coef1}",
                    "start": {
                        "dateTime": high_tide1_time.isoformat(),
                        "timeZone": "Europe/Paris",
                    },
                    "end": {
                        "dateTime": (
                            high_tide1_time + timedelta(minutes=15)
                        ).isoformat(),
                        "timeZone": "Europe/Paris",
                    },
                }
                events.append(event_info_high1)

            # Low Tide 1
            low_tide1_time = parse_time(
                year, month, day_number, row["Low tide"].split()[0]
            )
            if low_tide1_time:
                low_tide1_height = row["Low tide"].split()[1]
                coef1 = row["Coef"]
                event_info_low1 = {
                    "summary": f"Low Tide ({low_tide1_height}) coef {coef1}",
                    "start": {
                        "dateTime": low_tide1_time.isoformat(),
                        "timeZone": "Europe/Paris",
                    },
                    "end": {
                        "dateTime": (
                            low_tide1_time + timedelta(minutes=15)
                        ).isoformat(),
                        "timeZone": "Europe/Paris",
                    },
                }
                events.append(event_info_low1)

            # High Tide 2
            high_tide2_time = parse_time(
                year, month, day_number, row["High tide 2"].split()[0]
            )
            if high_tide2_time:
                high_tide2_height = row["High tide 2"].split()[1]
                coef2 = row["Coef 2"]
                event_info_high2 = {
                    "summary": f"High Tide ({high_tide2_height}) coef {coef2}",
                    "start": {
                        "dateTime": high_tide2_time.isoformat(),
                        "timeZone": "Europe/Paris",
                    },
                    "end": {
                        "dateTime": (
                            high_tide2_time + timedelta(minutes=15)
                        ).isoformat(),
                        "timeZone": "Europe/Paris",
                    },
                }
                events.append(event_info_high2)

            # Low Tide 2
            low_tide2_time = parse_time(
                year, month, day_number, row["Low tide 2"].split()[0]
            )
            if low_tide2_time:
                low_tide2_height = row["Low tide 2"].split()[1]
                coef2 = row["Coef 2"]
                event_info_low2 = {
                    "summary": f"Low Tide ({low_tide2_height}) coef {coef2}",
                    "start": {
                        "dateTime": low_tide2_time.isoformat(),
                        "timeZone": "Europe/Paris",
                    },
                    "end": {
                        "dateTime": (
                            low_tide2_time + timedelta(minutes=15)
                        ).isoformat(),
                        "timeZone": "Europe/Paris",
                    },
                }
                events.append(event_info_low2)

    return events


def get_all_events():
    all_events = []

    # Define starting and ending points
    start_year = 2024
    start_month_index = 0  # Index in month_names for August 2024
    end_year = 2025
    end_month_index = 11  # Index in month_names for July 2025

    # Loop through months from August 2024 to July 2025
    year = start_year
    for i in range(start_month_index, end_month_index + 1):
        month_name = month_names[i]
        if i >= 5:  # January to July 2025
            year = 2025
        month = i + 8 if i < 5 else i - 4

        csv_file = f"data/{month_name}-{year}.csv"
        events = get_event_infos_for_file(csv_file, year, month)
        all_events.extend(events)

        # save to JSON file
    with open("data/all_events.json", "w") as file:
        json.dump(all_events, file, indent=4)

    return all_events
