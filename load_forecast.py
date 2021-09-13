import os
import sys
import urllib.request
import webbrowser
import traceback
import datetime
from datetime import datetime as dt
import glob


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


def main():
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

    database = os.path.abspath("database")

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


if __name__ == "__main__":
    main()
