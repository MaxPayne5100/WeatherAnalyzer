import json
import os
from pprint import pprint


def main():
    filesdir = "database"
    jsonfile = os.path.join(filesdir, "forecast-5-12-2020.json")

    with open(jsonfile) as data_file:
        data = json.load(data_file)

    pprint(data)
    print()

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


if __name__ == "__main__":
    main()
