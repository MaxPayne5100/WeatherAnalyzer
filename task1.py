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

    report = "report-task1.txt"
    filereport = os.path.join(filesdir, report)

    with open(jsonfile) as data_file:
        data = json.load(data_file)

    # --- find average temperature for each day ---
    try:
        tz = data["city"]["timezone"]  # get timezone shift in seconds from data
        tz_delta = datetime.timedelta(seconds=tz)  # create timedelta from tz

        avg_temps = {}  # results (date, t_avg) will be written here
        curr_date = to_localtime(data["list"][0]["dt"], tz_delta).date()
        t_sum = 0  # sum of temperatures for the current date
        t_n = 0  # number of measurements for the current date

        for entry in data["list"]:  # iterate over subelements of list

            date = to_localtime(entry["dt"], tz_delta).date()  # date of curr entry

            if date == curr_date:  # if date hasn't changed
                t_sum += entry["main"]["temp"]  # update sum
                t_n += 1  # update quantity
                t_avg = t_sum / t_n  # calculate average
                avg_temps[curr_date] = t_avg  # append to results
            else:
                curr_date = date  # update current date
                t_sum = entry["main"]["temp"]  # update sum
                t_n = 1  # update quantity

    except KeyError as ex:
        print(f"Error: Unable to find key '{ex.args[0]}'")
        print("Maybe JSON have inappropriate structure")
        sys.exit(1)  # exit with code 1 indicating error

    # output
    print()
    for date, t_avg in avg_temps.items():
        result_output(f"{date}: average temperature {t_avg:.2f} C", filereport)


if __name__ == "__main__":
    main()
