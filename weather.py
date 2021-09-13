import os
import sys
import urllib.request
import webbrowser
import traceback
import datetime
from datetime import datetime as dt
import glob
import json
import collections
import subprocess
from sys import platform

# region Constants
CONST_DEL_SIZE = 15
filesdir = "database"
reportsdir = "reports"
# endregion


def print_traceback():
    """Ask user if he wants to see traceback and show it if yes"""
    while True:
        show = input("Print traceback (y/n): ")
        if show == "y":
            tb = traceback.format_exc()  # get traceback of last caught exc
            print(tb)
            return
        elif show == "n":
            return
        print("Invalid input")


def request_if_available():
    """
    Check if file with weather data for today already exists.
    If yes, it's path will be returned.
    Else new file will be requested from OpenWeather and its path returned.
    """
    make_request = True
    url = ("https://api.openweathermap.org/data/2.5/forecast"
           "?lat=49.8397&lon=24.0297"
           "&exclude=current,minutely,daily,alerts"
           "&mode=json"
           "&appid=795a5a5bc057a06ee6e8f9238347ea9d&units=metric")  # json file URL

    print("\nПочаток ...")

    day = str(datetime.date.today().day)
    month = str(datetime.date.today().month)
    year = str(datetime.date.today().year)
    today = day + '.' + month + '.' + year

    print(f"Сьогодні: {today}")

    database = os.path.abspath(filesdir)

    if not os.path.exists(database):
        os.makedirs(database)

    if not len(os.listdir(database)) == 0:
        part = glob.glob(os.path.join(database, '*.json'))
        part.sort(key=os.path.getmtime, reverse=True)

        print("\n*** Доступні json файли ***")
        [print(f" {os.path.split(filename)[1]}\t"
               f"{dt.fromtimestamp(os.path.getmtime(filename)).date()}\n")
         for filename in part]

        for filename in part:
            if dt.fromtimestamp(os.path.getmtime(filename)).date() ==\
                    datetime.date.today():
                make_request = False

    if make_request:
        filename = "forecast-" + "-".join(today.split(".")) + ".json"  # save file locally with this filename
        filepath = os.path.join(database, filename)  # get absolute path to saved file

        try:
            remotefile = urllib.request.urlopen(url)  # try to get file by url

        except urllib.request.HTTPError as ex:  # handle HTTPError
            print(f"HTTP Error {ex.code} {ex.reason}")  # print reason
            print_traceback()  # print traceback if user needs it
            sys.exit(1)  # exit program with return code 1 indicating error

        except urllib.request.URLError as ex:  # handle URLError
            print(f"Invalid URL: {ex.reason}")  # print reason
            print_traceback()  # print traceback if user needs it
            sys.exit(1)  # exit program with return code 1 indicating error

        with open(filepath, "wb") as fsave:  # open file for save
            fsave.write(remotefile.read())  # write data from remote file

        remotefile.close()  # close remote file

        print(f"\n... Зроблено запит до {url}")
        print("\n... Відкриття json файлу із сьогоднішніми даними")

        # os.startfile works only on Windows, so we used webbrowser module
        # because it is cross platform
        webbrowser.open_new_tab(filepath)  # open saved file in default browser or app

        return filepath  # return path of loaded file

    else:
        return os.path.abspath(part[0])  # return existing file for today


def explore_data(data):
    # ------------ вивчення структури документа ------------
    # корінь документа
    print("Тип цілого документа:", type(data).__name__)
    print("Документ має", len(data), "елементів")
    print("Ключі кожного елемента:",
          *data.keys())
    print("Тип кожного елемента як цілого:",
          *[type(ob).__name__ for ob in data])
    print("Типи значень окремих елементів документа за ключами:",
          *[type(data[ob]).__name__ for ob in data.keys()])
    print("\n")

    # елемент 'city'
    print("Тип елемента 'city':", type(data["city"]).__name__)
    print("\nЗначення цілого елемента 'city':\n", data['city'])
    print("\nКлючі елемента 'city':", *data["city"].keys())
    print("\nПоелементний перелік частин 'city':")
    print(*[subvalue for subvalue in data["city"].items()], sep="\n")
    print("\n")

    # елемент 'list'
    print("Тип елемента 'list':", type(data["list"]).__name__)
    print("Кількість елементів в 'list':", len(data["list"]))
    print("Тип першого піделемента в 'list'", type(data["list"][0]).__name__)
    print("\nЗначення цілого першого піделемента в 'list':\n", data['list'][0])
    print("\nКлючі першого піделемента в 'list':", *data["list"][0].keys())
    print("\nПоелементний перелік частин першого піделемента в 'list':")
    print(*[subvalue for subvalue in data["list"][0].items()], sep="\n")
    print("\n")

    # елемент 'main'
    print("Тип елемента 'main':", type(data["list"][0]["main"]).__name__)
    print("\nКлючі елемента 'main':", *data["list"][0]["main"].keys())
    print("\nПоелементний перелік частин першого елемента 'main':")
    print(*[subvalue for subvalue in data["list"][0]["main"].items()], sep="\n")


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


def find_avg_temp(data):
    """Find average temperature for each day"""
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

    return avg_temps


def find_max_humidity(data):
    """For each day find max humidity and hour when it is predicted"""
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

    return results


def find_warm_cold(data):
    """Find the warmest and the coldest days"""
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

    return max_days, max_temp, min_days, min_temp


def add_dict_value(key, value, dict_):
    """Add value to specified dictionary"""
    if key in dict_:
        dict_[key] += "\t" + value + "\n"
    else:
        dict_[key] = "\t" + value + "\n"


def find_same_humidity(data):
    """Find datetimes with the same humidity"""
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

    return result


def find_max_windspeed_temp(data):
    """Find temperature when wind speed is maximum"""
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

    return results


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


def find_average_temp_from_dates(data, dates):
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
    print()
    print("*" * CONST_DEL_SIZE + " Main process " + "*" * CONST_DEL_SIZE)

    filepath = request_if_available()  # get filename of current data file

    with open(filepath) as data_file:
        data = json.load(data_file)  # load weather data

    print()
    explore_data(data)  # explore data format

    if not os.path.exists(reportsdir):
        os.makedirs(reportsdir)  # create reports dir if not exists

    # task1
    report1 = os.path.join(reportsdir, "task1.txt")
    avg_temps = find_avg_temp(data)
    print()
    open(report1, "w").close()
    for date, t_avg in avg_temps.items():
        result_output(f"{date}: average temperature {t_avg:.2f} C",
                      report1)

    # task2
    report2 = os.path.join(reportsdir, "task2.txt")
    max_hs = find_max_humidity(data)
    print()
    open(report2, "w").close()
    for date, time, h_max in max_hs:
        result_output(f"{date}: maximum humidity {h_max}% expected at {time}",
                      report2)

    # task3
    report3 = os.path.join(reportsdir, "task3.txt")
    max_days, max_temp, min_days, min_temp = find_warm_cold(data)
    print()
    open(report3, "w").close()
    for date in max_days:
        result_output(f"The warmest day is {date}, with temperature {max_temp} C",
                      report3)
    for date in min_days:
        result_output(f"The coldest day is {date}, with temperature {min_temp} C",
                      report3)

    # task4
    report4 = os.path.join(reportsdir, "task4.txt")
    same_hs = find_same_humidity(data)
    print()
    open(report4, "w").close()
    od = collections.OrderedDict(sorted(same_hs.items()))
    for key, values in od.items():
        result_output(f"The humidity {key} was in these days: ", report4)
        result_output(values, report4)

    # task5
    report5 = os.path.join(reportsdir, "task5.txt")
    temps = find_max_windspeed_temp(data)
    open(report5, "w").close()
    for max_wind_speed, temp, date in temps:
        result_output(f"The highest wind speed is {max_wind_speed} meters/sec "
                      f"on {date}, with temperature {temp} C", report5)

    # task 6
    report6 = os.path.join(reportsdir, "task6.txt")
    filepath2 = input("\nPlease, input second json file from 'database' directory: ")
    filepath2 = os.path.join(filesdir, filepath2)

    data_date = ".".join(os.path.basename(filepath)
                         .split(".")[0].split("-")[1:])
    data_date2 = ".".join(os.path.basename(filepath2)
                          .split(".")[0].split("-")[1:])

    with open(filepath2) as data_file:
        data2 = json.load(data_file)

    # --- analyze temperature changes from two json files for common days ---
    try:
        common_days = get_common_days(data, data2)
        avg_temps = find_average_temp_from_dates(data, common_days)
        avg_temps2 = find_average_temp_from_dates(data2, common_days)
        diff = {}

        for key in avg_temps.keys():
            diff[key] = avg_temps2[key] - avg_temps[key]

    except KeyError as ex:
        print(f"Error: Unable to find key '{ex.args[0]}'")
        print("Maybe JSON have inappropriate structure")
        sys.exit(1)  # exit with code 1 indicating error

    print()
    open(report6, "w").close()
    heading = (' | '.join(elem.ljust(35)
                          for elem in (f"Date",
                                       f"Temperature [data from {data_date}]",
                                       f"Temperature [data from {data_date2}]",
                                       f"Diff")))
    result_output(heading, report6)
    result_output("-" * int(len(heading)), report6)

    for key in avg_temps.keys():
        result_output(' | '.join(elem.ljust(35)
                                 for elem in (str(key),
                                              f"{avg_temps[key]:.2f} C",
                                              f"{avg_temps2[key]:.2f} C",
                                              f"{diff[key]:.2f} C")),
                      report6)
    result_output("-" * int(len(heading)), report6)

    print()
    print("*" * CONST_DEL_SIZE + " Subprocess " + "*" * CONST_DEL_SIZE)

    # execute weather_gui.py
    if platform == "linux" or platform == "linux2":
        subprocess.run(["python3", "weather_gui.py"])
    elif platform == "win32":
        subprocess.run(["python", "weather_gui.py"])

    print()
    print("*" * CONST_DEL_SIZE + " Main process " + "*" * CONST_DEL_SIZE)

    print()
    print("To end main process press Enter")
    input()


if __name__ == "__main__":
    main()
