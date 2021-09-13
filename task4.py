import sys
import json
import datetime
import os
import collections


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


def add_dict_value(key, value, dict_):
    """Add value to specified dictionary"""
    if key in dict_:
        dict_[key] += "\t" + value + "\n"
    else:
        dict_[key] = "\t" + value + "\n"


def main():
    filesdir = "database"
    jsonfile = os.path.join(filesdir, "forecast-5-12-2020.json")

    report = "report-task4.txt"
    filereport = os.path.join(filesdir, report)

    with open(jsonfile) as data_file:
        data = json.load(data_file)

    # --- find datetimes with the same humidity ---
    try:
        tz = data["city"]["timezone"]  # get timezone shift in seconds from data
        tz_delta = datetime.timedelta(seconds=tz)  # create timedelta from tz
        result = {}
        for element in data["list"]:  # iterate over subelements of list
            date = to_localtime(element["dt"], tz_delta).date()  # get data of current list element
            time = to_localtime(element["dt"], tz_delta).time()  # get time of current list element

            datetimes = str(date) + " " + str(time)
            add_dict_value(element["main"]["humidity"], datetimes, result)

    except KeyError as ex:
        print(f"Error: Unable to find key '{ex.args[0]}'")
        print("Maybe JSON have inappropriate structure")
        sys.exit(1)  # exit with code 1 indicating error

    # output
    print()
    od = collections.OrderedDict(sorted(result.items()))

    for key, values in od.items():
        result_output(f"The humidity {key} was in these days: ", filereport)
        result_output(values, filereport)


if __name__ == "__main__":
    main()
