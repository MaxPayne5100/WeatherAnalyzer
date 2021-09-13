import sys
import json
import datetime
import os


def result_output(message, filename):
    """Print message to console and file"""
    with open(filename, mode='a', encoding='utf-8') as file:
        file.write(message)
        file.write(os.linesep)
    print(message)


def to_localtime(timestamp, tz_delta):
    """Convert timestamp to datetime and add tz_delta"""
    dt = datetime.datetime.utcfromtimestamp(timestamp)  # read entry's dt
    dt += tz_delta  # convert dt from utc0 to local time
    return dt


def main():
    filesdir = "database"
    jsonfile = os.path.join(filesdir, "forecast-5-12-2020.json")

    report = "report-task5.txt"
    filereport = os.path.join(filesdir, report)

    with open(jsonfile) as data_file:
        data = json.load(data_file)

    # --- find temperature when wind speed was maximum ---
    try:
        tz = data["city"]["timezone"]  # get timezone shift in seconds from data
        tz_delta = datetime.timedelta(seconds=tz)  # create timedelta from tz

        results = []  # results (date, temperature, nax wind speed) will be written here
        max_wind_speed = 0  # current max wind speed

        for entry in data["list"]:  # iterate over subelements of list
            if entry["wind"]["speed"] > max_wind_speed:
                max_wind_speed = entry["wind"]["speed"]

        for entry in data["list"]:  # iterate over subelements of list
            if entry["wind"]["speed"] == max_wind_speed:
                date = to_localtime(entry["dt"], tz_delta).date()  # get date in local time format
                results.append((entry["wind"]["speed"],
                               entry["main"]["temp"],
                               date))

    except KeyError as ex:
        print(f"Error: Unable to find key '{ex.args[0]}'")
        print("Maybe JSON have inappropriate structure")
        sys.exit(1)  # exit with code 1 indicating error

    # output
    print()
    for max_wind_speed, temp, date in results:
        result_output(f"The highest wind speed is {max_wind_speed} meters/sec "
                      f"on {date}, with temperature {temp} C", filereport)


if __name__ == "__main__":
    main()
