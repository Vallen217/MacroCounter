import os
import re
from datetime import datetime

class MacroCounter:
    def __init__(self, target_dir, target_f):
        self.target_dir = target_dir
        self.target_f = target_f
        self.data = {"Cal": [], "Fat": [], "Carb": [], "Protein": []}
        self.totals = [0, 0, 0, 0]

    def check_existence(self):
        if os.path.exists(self.target_dir):
            pass
        else:
            os.mkdir(self.target_dir)
        os.chdir(self.target_dir)

        try:
            with open(self.target_f, 'x') as _:
                pass
        except FileExistsError:
            pass

    # saves the file data to rewrite it in write_file() with the new data
    def compile_data(self, file_name):
        with open(file_name, 'r') as rf:
            for line in rf:
                if line == "\n":
                    break
                if re.match("\d+\.\dg?", line):
                    for i, datum in enumerate(line.split()):
                        if "g" in datum[-1]:
                            datum = datum[0:-1]
                        datum = float(datum)
                        # caffeine fueled logic
                        if i % 4 == 0:
                            self.data["Cal"].append(datum)
                        if (i - 1) % 4 == 0:
                            self.data["Fat"].append(datum)
                        if i % 2 == 0 and i % 4 != 0:
                            self.data["Carb"].append(datum)
                        if (i - 1) % 2 == 0 and (i - 1) % 4 != 0:
                            self.data["Protein"].append(datum)
        return

    # append new data entries
    def update_file(self):
        print(
                "\n(q) - Quit loop\n"
                "(Quit only after entering data into all 4 entries)\n"
        )
        while True:
            try:
                self.data["Cal"].append(float(input("Calorie: ")))
                self.data["Fat"].append(float(input("Fat: ")))
                self.data["Carb"].append(float(input("Carb: ")))
                self.data["Protein"].append(float(input("Protein: ")))
            except ValueError:
                break
            if str(input().lower()) == "q":
                break
        return self.write_file()

    def write_file(self):
        self.totals = [sum(self.data[key]) for key in self.data]
        pad = lambda word: " " * (12 - len(str(word)))
        ratio = 100 / (self.totals[1] + self.totals[2] + self.totals[3])
        temp = [f"{round(ratio * self.totals[i], 1)}%" for i in range(1, 4)]
        relative_per = [f"{v}{pad(v)}" for v in temp]


        with open(self.target_f, 'w') as wf:
            wf.write(
                    f"Cal:{pad('Cal:')}Fat:{pad('Fat:')}"
                    f"Carb:{pad('Carb:')}Protein:{pad('Protein:')}"
            )

        with open(self.target_f, 'a') as af:
            for i in range(len(self.data["Cal"])):
                af.write("\n")
                for key in self.data:
                    if key == "Cal":
                        af.write(f"{self.data[key][i]}{pad(self.data[key][i])}")
                    else:
                        af.write(f"{self.data[key][i]}g{pad(f'{self.data[key][i]}g')}")

            af.write(
                    f"\n\nTotal Amounts & Relative Percentages:\n"
                    f"{self.totals[0]}{pad(self.totals[0])}"
                    f"{self.totals[1]}g{pad(f'{self.totals[1]}g')}"
                    f"{self.totals[2]}g{pad(f'{self.totals[2]}g')}"
                    f"{self.totals[3]}g"
                    f"\n{' ' * 12}{relative_per[0]}"
                    f"{relative_per[1]}{relative_per[2]}"
                    )
        return display_data(self.target_f)

def display_data(file):
    print()
    with open(file, 'r') as rf:
        for data in rf:
            print(data.rstrip("\n"))
    print("\n")

def display_monthly_data(directory):
    pad = lambda word: " " * (12 - len(str(word)))
    totals = [0, 0, 0, 0]
    os.chdir(directory)
    file_list = os.listdir(directory)

    for file in file_list:
        with open(f"{directory}/{file}") as rf:
            lines = rf.readlines()

        temp = [lines[i+2].split() for i, line in\
                enumerate(lines) if line == "\n"]
        for j in range(4):
            if "g" in temp[0][j]:
                temp[0][j] = temp[0][j][0:-1]
            totals[j] += float(temp[0][j])

    rel_monthly_per = [f"{round((100 / (sum(totals[1:]))) *  totals[i], 1)}%"\
            for i in range(1, 4)]
    mean_amounts = [round(totals[i] / len(file_list), 1) for i in range(4)]

    print(
            f"\nCal:{pad('Cal:')}Fat:{pad('Fat:')}"
            f"Carb:{pad('Carb:')}Protein:{pad('Protein:')}\n"
    )
    print(f"Contemporary monthly total amounts: ")
    print(f"{totals[0]}{pad(totals[0])}", end="")
    [print(f"{v}g{pad(f'{v}g')}", end='') for v in totals[1:]]

    print("\n\nMean daily amounts: ")
    print(f"{mean_amounts[0]}{pad(mean_amounts[0])}", end="")
    [print(f"{v}g{pad(f'{v}g')}", end='') for v in mean_amounts[1:]]

    print("\n\nMean daily relative percentages: ")
    print(pad(""), end="")
    [print(f"{v}{pad(v)}", end="") for v in rel_monthly_per]
    print("\n")

def view_previous_data(parent_directory, operation):
    print("\nEnter a relative directory from:")
    [print(dir) for dir in os.listdir(parent_directory)]
    directory_name = str(input("\n"))
    target_directory = os.path.join(parent_directory, directory_name)

    if operation == "pm":
        return display_monthly_data(target_directory)

    else:
        print("\nEnter a file to view from:")
        [print(file) for file in os.listdir(target_directory)]
        file_name = str(input("\n"))
        if ".txt" not in file_name:
            file_name = f"{file_name}.txt"
        target_file = os.path.join(target_directory, file_name)
        return display_data(target_file)

def main():
    parent_directory = '/home/vallen/Documents/Health/Macronutritional_intake'
    directory_name = f'{datetime.now().year}-{datetime.now().month}'
    target_directory = os.path.join(parent_directory, directory_name)
    file_name = f'{datetime.now().day}.txt'
    target_file = os.path.join(target_directory, file_name)

    counter = MacroCounter(target_directory, target_file)
    counter.check_existence()

    print(
        "\n(cf) - Create new file"
        "\n(uf) - Update file"
        "\n(pf) - Display previous files"
        "\n(pm) - Display previous monthly data"
        "\n(df) - Display file"
        "\n(dm) - Display monthly data"
        "\n(q) - Quit the program"
    )

    # calling functions inside a while loop feels wrong... but it works well.
    while True:
        operation = str(input("-")).lower()
        if operation == "q":
            break

        if operation == "pf" or operation == "pm":
            view_previous_data(parent_directory, operation)

        if re.match("m[0-9]+", operation):
            predefined_file = '/home/vallen/Workspace/MacroCounter'\
                                f'/Predefined_Meals/{operation}.txt'
            # 1st function call is to save pre-existing file data.
            # 2nd function call is to append predefined data to the file.
            counter.compile_data(target_file)
            counter.compile_data(predefined_file)
            counter.write_file()

        if operation == "cf":  # this "ui option" is purely for aesthetics.
            pass
        if operation == "uf":
            counter.compile_data(target_file)
            counter.update_file()
        if operation == "dm":
            display_monthly_data(target_directory)
        if operation == "df":
            display_data(target_file)
    return

if __name__ == "__main__":
    main()  
# csv? never met her.
# what's pathlib?
