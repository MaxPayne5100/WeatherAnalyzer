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

    report = "report-task3.txt"
    filereport = os.path.join(filesdir, report)

    with open(jsonfile) as data_file:
        data = json.load(data_file)

    # --- find the warmest and the coldest days ---
    try:
        tz = data["city"]["timezone"]  # get timezone shift in seconds from data
        tz_delta = datetime.timedelta(seconds=tz)  # create timedelta from tz
        max_temp = 0
        min_temp = data["list"][0]["main"]["temp"]
        max_days, min_days = [], []
        for element in data["list"]:  # iterate over subelements of list
            if element["main"]["temp"] > max_temp:  # check if temp of each element is higher than max
                max_temp = element["main"]["temp"]  # set new max temp
            if element["main"]["temp"] < min_temp:  # check if temp of each element is lower than min
                min_temp = element["main"]["temp"]  # set new mix temp

        for element in data["list"]:  # iterate over subelements of list
            date = to_localtime(element["dt"], tz_delta).date()  # get date in local time format
            if element["main"]["temp"] == max_temp:
                max_days.append(date)
            if element["main"]["temp"] == min_temp:
                min_days.append(date)

    except KeyError as ex:
        print(f"Error: Unable to find key '{ex.args[0]}'")
        print("Maybe JSON have inappropriate structure")
        sys.exit(1)  # exit with code 1 indicating error

    # output
    print()
    for date in max_days:
        result_output(f"The warmest day is {date}, with temperature {max_temp} C", filereport)

    for date in min_days:
        result_output(f"The coldest day is {date}, with temperature {min_temp} C", filereport)


if __name__ == "__main__":
    main()
