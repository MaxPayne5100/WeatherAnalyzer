import os
import tkinter as tk
from tkinter import ttk


def show_file(parent, filename):
    with open(filename, "r") as task_result:
        data = task_result.read()
    result_window = tk.Toplevel(parent)
    name = os.path.splitext(os.path.basename(filename))[0]
    result_window.title(name)
    tk.Message(result_window, text=data).pack()


def show_task4():
    """Show task 4 results in accordion"""
    parsed_data = {}
    with open("reports/task4.txt") as task_result:
        data = task_result.readlines()
    current_humidity = None
    for line in data:
        if line == os.linesep:
            continue
        if line.startswith("The"):
            current_humidity = line
            parsed_data[current_humidity] = []
        else:
            parsed_data[current_humidity].append(line)

    result_window = tk.Toplevel()
    result_window.title("task4")
    for humidity in parsed_data:
        t = ToggledFrame(result_window, text=humidity,
                         relief='raised', borderwidth=1)
        t.pack(fill="x", expand=1, pady=2, padx=2, anchor='n')

        for date in parsed_data[humidity]:
            ttk.Label(t.sub_frame, text=date).pack()


def show_task6():
    """Show task 6 results in table in new window"""
    parsed_data = []
    with open("reports/task6.txt") as task_result:
        data = task_result.readlines()
    for line in data:
        line_lst = line.split('|')
        if len(line_lst) == 4:
            for i in range(len(line_lst)):
                line_lst[i] = line_lst[i].rstrip()
            parsed_data.append(line_lst)
    result_window = tk.Toplevel()
    result_window.title("task6")
    Table(result_window, parsed_data)


class ToggledFrame(tk.Frame):

    def __init__(self, parent, text="", *args, **options):
        tk.Frame.__init__(self, parent, *args, **options)

        self.show = tk.IntVar()
        self.show.set(0)

        self.title_frame = ttk.Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        ttk.Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = ttk.Checkbutton(self.title_frame,
                width=2, text='+', command=self.toggle, variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = tk.Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')


class Table:
    """Table as grid of Entries"""
    def __init__(self, parent, data):
        """
        Create table from data and add it to parent
        parent - parent window
        data - iterable of iterables with data to show
        """
        total_rows = len(data)
        total_columns = len(data[0])

        # code for creating table
        # title
        for j in range(total_columns):
            self.e = tk.Entry(parent, width=30, fg='blue',
                              font=('Arial', 16, 'bold'))

            self.e.grid(row=0, column=j)
            self.e.insert(tk.END, data[0][j])

        # contents
        for i in range(1, total_rows):
            for j in range(total_columns):
                self.e = tk.Entry(parent, width=30, fg='black',
                                  font=('Arial', 16))

                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, data[i][j])


class App(tk.Frame):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.master.title("Weather")

        task1_lbl = tk.Label(self,
                             text="Середні значення температури по днях:")
        task1_lbl.grid(row=0, column=0)
        task1_btn = tk.Button(self, text="Перегляд",
                              command=lambda: show_file(self, "reports/task1.txt"))
        task1_btn.grid(row=0, column=1)

        task2_lbl = tk.Label(self, text="Максимальна вологість по днях:")
        task2_lbl.grid(row=1, column=0)
        task2_btn = tk.Button(self, text="Перегляд",
                              command=lambda: show_file(self, "reports/task2.txt"))
        task2_btn.grid(row=1, column=1)

        task3_lbl = tk.Label(self, text="Найтепліші та найхолодніші дні:")
        task3_lbl.grid(row=2, column=0)
        task3_btn = tk.Button(self, text="Перегляд",
                              command=lambda: show_file(self, "reports/task3.txt"))
        task3_btn.grid(row=2, column=1)

        task4_lbl = tk.Label(self, text="Дні з однаковою вологістю:")
        task4_lbl.grid(row=3, column=0)
        task4_btn = tk.Button(self, text="Перегляд", command=show_task4)
        task4_btn.grid(row=3, column=1)

        task5_lbl = tk.Label(self, text="Температура при максимальній швидкості вітру:")
        task5_lbl.grid(row=4, column=0)
        task5_btn = tk.Button(self, text="Перегляд",
                              command=lambda: show_file(self, "reports/task5.txt"))
        task5_btn.grid(row=4, column=1)

        task6_lbl = tk.Label(self, text="Динаміка зміни темеператури за спільні дні:")
        task6_lbl.grid(row=5, column=0)
        task6_btn = tk.Button(self, text="Перегляд", command=show_task6)
        task6_btn.grid(row=5, column=1)

        self.pack()


def main():
    root = tk.Tk()
    root.resizable(False, False)
    app = App()
    root.mainloop()


if __name__ == '__main__':
    main()
