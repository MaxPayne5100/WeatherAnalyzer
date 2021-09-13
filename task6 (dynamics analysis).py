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


def get_common_days(data, data2):
    """Get common days for 'data', 'data2' from two json files"""
    tz = data["city"]["timezone"]  # get timezone shift in seconds from data
    tz_delta = datetime.timedelta(seconds=tz)  # create timedelta from tz

    dates, dates2 = [], []

    [dates.append(to_localtime(entry["dt"], tz_delta).date())
     for entry in data["list"]]
    [dates2.append(to_localtime(entry["dt"], tz_delta).date())
     for entry in data2["list"]]

    return sorted(set(dates) & set(dates2))


def find_average_temp(data, dates):
    """Find average temperature for each day from 'dates'"""
    tz = data["city"]["timezone"]  # get timezone shift in seconds from data
    tz_delta = datetime.timedelta(seconds=tz)  # create timedelta from tz

    avg_temps = {}  # results (date, t_avg) will be written here
    curr_date = dates[0]
    t_sum = 0  # sum of temperatures for the current date
    t_n = 0  # number of measurements for the current date

    for entry in data["list"]:  # iterate over subelements of list
        date = to_localtime(entry["dt"], tz_delta).date()  # date of curr entry

        if date in dates:
            if date == curr_date:  # if date hasn't changed
                t_sum += entry["main"]["temp"]  # update sum
                t_n += 1  # update quantity
                t_avg = t_sum / t_n  # calculate average
                avg_temps[curr_date] = t_avg  # append to results
            else:
                curr_date = date  # update current date
                t_sum = entry["main"]["temp"]  # update sum
                t_n = 1  # update quantity

    return avg_temps


def main():
    filesdir = "database"
    jsonfile = "forecast-5-12-2020.json"
    jsonfile2 = "forecast-6-12-2020.json"
    jsonfilepath = os.path.join(filesdir, jsonfile)
    jsonfilepath2 = os.path.join(filesdir, jsonfile2)

    data_date = ".".join(jsonfile.split(".")[0].split("-")[1:])
    data_date2 = ".".join(jsonfile2.split(".")[0].split("-")[1:])

    report = "report-task6.txt"
    filereport = os.path.join(filesdir, report)

    with open(jsonfilepath) as data_file:
        data = json.load(data_file)
    with open(jsonfilepath2) as data_file:
        data2 = json.load(data_file)

    # --- analyze temperature changes from two json files for common days ---
    try:
        common_days = get_common_days(data, data2)
        avg_temps = find_average_temp(data, common_days)
        avg_temps2 = find_average_temp(data2, common_days)
        diff = {}

        for key in avg_temps.keys():
            diff[key] = avg_temps2[key] - avg_temps[key]

    except KeyError as ex:
        print(f"Error: Unable to find key '{ex.args[0]}'")
        print("Maybe JSON have inappropriate structure")
        sys.exit(1)  # exit with code 1 indicating error

    # output
    print()
    result_output("*** Динаміка зміни середньої температури за "
                  "спільні дні з двох json файлів ***\n", filereport)
    heading = (' | '.join(elem.ljust(30)
                          for elem in (f"Дата",
                                       f"Температура [дані з {data_date}]",
                                       f"Температура [дані з {data_date2}]",
                                       f"Різниця")))
    result_output(heading, filereport)
    result_output("-" * int(len(heading)), filereport)

    for key in avg_temps.keys():
        result_output(' | '.join(elem.ljust(30)
                                 for elem in (str(key),
                                              f"{avg_temps[key]:.2f} C",
                                              f"{avg_temps2[key]:.2f} C",
                                              f"{diff[key]:.2f} C")),
                      filereport)
    result_output("-" * int(len(heading)), filereport)


if __name__ == "__main__":
    main()
