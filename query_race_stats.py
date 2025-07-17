"""
This code was auto-generated with GitHub Copilot, with as minimal intervention as possible.  As the first
file in the project, I started off prompting with a request to write an entire file, and the code very
quickly became difficult to maintain.  Furthermore, the initial pass as calling the API had a hallucination
of a web endpoint that did not exist.  Coercing fixes into this method became more difficult over time, and
I re-prompted from scratch a couple of times.
"""

import requests
import pandas as pd
from datetime import datetime
import logging
from time import sleep
import os
from common import setup_logging, CACHE_FILE_DRIVER_STATS


BASE_URL = "https://api.openf1.org/v1"

def get_races(start_year=2020):
    """
    Fetch all race sessions (session_type 'Race') from start_year to current year.
    Uses the /sessions endpoint, as /races does not exist in the OpenF1 API.
    """
    current_year = datetime.now().year
    races = []
    for year in range(start_year, current_year + 1):
        url = f"{BASE_URL}/sessions"
        params = {"year": year, "session_type": "Race"}
        logging.info(f"API call: {url} | params: {params}")
        sleep(1)  # To avoid hitting API rate limits
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()
        logging.info(f"Entries returned: {len(data)}")
        races.extend(data)
    return races

def get_drivers_for_race(session_key):
    """Fetch all drivers for a given race session."""
    url = f"{BASE_URL}/drivers"
    params = {"session_key": session_key}
    logging.info(f"API call: {url} | params: {params}")
    sleep(1)  # To avoid hitting API rate limits
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    logging.info(f"Entries returned: {len(data)}")
    return data

def get_laps_for_race(session_key, driver_number):
    """Fetch all laps for a given driver in a race session."""
    url = f"{BASE_URL}/laps"
    params = {"session_key": session_key, "driver_number": driver_number}
    logging.info(f"API call: {url} | params: {params}")
    sleep(1)
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    logging.info(f"Entries returned: {len(data)}")
    return data

def get_grid_and_finish_positions(session_key, driver_number):
    """
    Fetch grid and finish positions for a driver in a race session.
    Uses the /position endpoint. The entry with the earliest 'date' is the grid position,
    and the entry with the latest 'date' is the finishing position.
    """
    url = f"{BASE_URL}/position"
    params = {"session_key": session_key, "driver_number": driver_number}
    logging.info(f"API call: {url} | params: {params}")
    sleep(1)
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    logging.info(f"Entries returned: {len(data)}")

    if not data:
        return None, None

    # Sort by date to find earliest and latest
    sorted_data = sorted(data, key=lambda x: x.get("date", ""))
    grid_position = sorted_data[0].get("position") if sorted_data else None
    final_position = sorted_data[-1].get("position") if sorted_data else None

    return grid_position, final_position

def main():
    cache_file = CACHE_FILE_DRIVER_STATS
    # Try to load cached DataFrame
    if os.path.exists(cache_file):
        df = pd.read_csv(cache_file)
        logging.info(f"Loaded cache with {len(df)} rows.")
    else:
        df = pd.DataFrame()
        logging.info("No cache found, starting with empty DataFrame.")

    races = get_races(start_year=2023)

    # Group races by year and country, keep only the most recent race per country per year
    races_by_year_country = {}
    for race in races:
        year = race.get("year")
        country = race.get("country_name")
        key = (year, country)
        if key not in races_by_year_country:
            races_by_year_country[key] = race
        else:
            # Compare date_start to keep the most recent
            prev_race = races_by_year_country[key]
            if race.get("date_start", "") > prev_race.get("date_start", ""):
                races_by_year_country[key] = race

    # Now group by year for further processing
    races_by_year = {}
    for (year, _), race in races_by_year_country.items():
        races_by_year.setdefault(year, []).append(race)
    for year in races_by_year:
        races_by_year[year] = sorted(races_by_year[year], key=lambda r: r.get("date_start"))

    # For quick lookup if cache exists
    cached_keys = set()
    if not df.empty:
        cached_keys = set(zip(df["session_key"], df["driver_number"]))

    for year, year_races in races_by_year.items():
        # Find the lowest session_key for this year
        session_keys = [race.get("session_key") for race in year_races]

        race_number = 0  # Increment on first usage
        for race in year_races:
            session_key = race.get("session_key")
            country = race.get("country_name")
            location = race.get("location")
            date = race.get("date_start")
            race_number = race_number + 1

            drivers = get_drivers_for_race(session_key)

            for driver in drivers:
                driver_number = driver.get("driver_number")
                cache_key = (session_key, driver_number)
                if cache_key in cached_keys:
                    logging.info(f"Skipping cached driver {driver_number} for session {session_key}")
                    continue

                driver_name = driver.get("full_name")
                broadcast_name = driver.get("broadcast_name")
                team_name = driver.get("team_name")
                country_code = driver.get("country_code")

                # Lap times
                laps = get_laps_for_race(session_key, driver_number)
                lap_times = [lap.get("lap_duration") for lap in laps if lap.get("lap_duration") is not None]
                best_lap_time = min(lap_times) if lap_times else None
                avg_lap_time = sum(lap_times) / len(lap_times) if lap_times else None

                # Grid and finish positions
                grid_position, final_position = get_grid_and_finish_positions(session_key, driver_number)
                if grid_position is not None and final_position is not None:
                    position_change = (grid_position - final_position)
                else:
                    position_change = None

                row = {
                    "season_year": year,
                    "race_number": race_number,
                    "session_key": session_key,
                    "race_location": location,
                    "country": country,
                    "date": date,
                    "driver_number": driver_number,
                    "driver_name": driver_name,
                    "broadcast_name": broadcast_name,
                    "team_name": team_name,
                    "country_code": country_code,
                    "best_lap_time": best_lap_time,
                    "avg_lap_time": avg_lap_time,
                    "position_change": position_change,
                    "grid_position": grid_position,
                    "final_position": final_position
                }

                # Append new row and update cache
                df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                df.to_csv(cache_file, index=False)
                cached_keys.add(cache_key)
                logging.info(f"Added and cached driver {driver_number} for session {session_key}")

    logging.info(df.head())
    logging.info(f"Final cache file had {len(df)} rows.")


if __name__ == "__main__":
    setup_logging()
    main()
