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

    report = "report-task2.txt"
    filereport = os.path.join(filesdir, report)

    with open(jsonfile) as data_file:
        data = json.load(data_file)

    # --- for each day find max humidity and hour when it is predicted ---
    try:
        tz = data["city"]["timezone"]  # get timezone shift in seconds from data
        tz_delta = datetime.timedelta(seconds=tz)  # create timedelta from tz

        results = []  # results (date, time, h_max) will be written here
        dt0 = to_localtime(data["list"][0]["dt"], tz_delta)  # dt from 0 entry
        curr_date = dt0.date()  # current date
        t_max = None  # time of maximum humidity
        h_max = 0  # current max humidity
        for entry in data["list"]:  # iterate over subelements of list
            dt = to_localtime(entry["dt"], tz_delta)  # dt of curr entry
            if dt.date() == curr_date:  # if date hasn't changed
                humidity = entry["main"]["humidity"]
                if humidity >= h_max:
                    h_max = humidity  # update maximum
                    t_max = dt.time()  # update time of max humidity
            else:
                results.append((curr_date, t_max, h_max))  # append to results
                curr_date = dt.date()  # update current date
                h_max = 0  # reset maximum humidity
                t_max = None  # reset time of max

    except KeyError as ex:
        print(f"Error: Unable to find key '{ex.args[0]}'")
        print("Maybe JSON have inappropriate structure")
        sys.exit(1)  # exit with code 1 indicating error

    # output
    print()
    for date, time, h_max in results:
        result_output(f"{date}: maximum humidity {h_max}% expected at {time}", filereport)


if __name__ == "__main__":
    main()
