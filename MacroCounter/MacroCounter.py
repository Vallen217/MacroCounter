import os
import re
from datetime import datetime

class main:
    def __init__(self, target_dir, target_f):
        self.target_dir = target_dir
        self.target_f = target_f

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

    def update_file(self):
        data = {"Cal": [], "Fat": [], "Carb": [], "Protein": []}
        print(f"DATA: {data}")
        # saves the file data to rewrite it in compile_data with the new data
        with open(self.target_f, 'r') as rf:
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
                            data["Cal"].append(datum)
                        if (i - 1) % 4 == 0:
                            data["Fat"].append(datum)
                        if i % 2 == 0 and i % 4 != 0:
                            data["Carb"].append(datum)
                        if (i - 1) % 2 == 0 and (i - 1) % 4 != 0:
                            data["Protein"].append(datum)
        print(f"DATA TWO: {data}")
        # new data entries
        while True:
            try:
                data["Cal"].append(float(input("Calorie: ")))
                data["Fat"].append(float(input("Fat: ")))
                data["Carb"].append(float(input("Carb: ")))
                data["Protein"].append(float(input("Protein: ")))
            except ValueError:
                break
            if str(input().lower()) == "q":
                break

        totals = [sum(data[key]) for key in data]
        print(f"\n\nupdate_file:\nDATA: {data}\nTOTALS: {totals}\n")
        return counter.compile_data(data, totals)

    def compile_data(self, data, totals):

        print(f"\n\ncompile_data:\nDATA: {data}\nTOTALS: {totals}\n")

        pad = lambda word: " " * (12 - len(str(word)))

        with open(self.target_f, 'w') as wf:
            wf.write(
                    f"Cal:{pad('Cal:')}Fat:{pad('Fat:')}"
                    f"Carb:{pad('Carb:')}Protein:{pad('Protein:')}"
            )

        with open(self.target_f, 'a') as af:
            for i in range(len(data["Cal"])):
                af.write("\n")
                for key in data:
                    if key == "Cal":
                        af.write(f"{data[key][i]}{pad(data[key][i])}")
                    else:
                        af.write(f"{data[key][i]}g{pad(f'{data[key][i]}g')}")

            af.write(
                    f"\n\nTotal Amounts & Relative Percentages:\n"
                    f"{totals[0]}{pad(totals[0])}"
                    f"{totals[1]}g{pad(f'{totals[1]}g')}"
                    f"{totals[2]}g{pad(f'{totals[2]}g')}"
                    f"{totals[3]}g"
            )

            ratio = 100 / (totals[1] + totals[2] + totals[3])
            temp = [f"{round(ratio * totals[i], 1)}%" for i in range(1, 4)]
            relative_per = [f"{v}{pad(v)}" for v in temp]
            af.write(f"\n{' ' * 12}{relative_per[0]}"
                    f"{relative_per[1]}{relative_per[2]}"
            )
        display_data(target_file)

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


if __name__ == "__main__":
    operation = str(input(
            "(cf) - Create new file: \n"
            "(uf) - Update file: \n"
            "(pf) - Display previous files:\n"
            "(pm) - Display previous monthly data: \n"
            "(df) - Display file: \n"
            "(dm) - Display monthly data: \n\n"
    )).lower()
    parent_directory = '/home/vallen/Documents/Health/Macronutritional_intake'

    if operation == "pf" or operation == "pm":
        directory_name = str(input(
                "Enter a relative directory path from: "
                f"{os.listdir(parent_directory)}:\n"
        ))
        target_directory = os.path.join(parent_directory, directory_name)
        if operation == "pm":
            display_monthly_data(target_directory)

        else:
            file_name = str(input(
                "Enter a file to view from: "
                f"{os.listdir(target_directory)}:\n)"
            ))
            if ".txt" not in file_name:
                file_name = f"{file_name}.txt"
            target_file = os.path.join(target_directory, file_name)
            display_data(target_file)

    else:
        directory_name = f'{datetime.now().year}-{datetime.now().month}'
        target_directory = os.path.join(parent_directory, directory_name)
        file_name = f'{datetime.now().day}.txt'
        target_file = os.path.join(target_directory, file_name)

        counter = main(target_directory, target_file)

        #if re.match("m[0-9]+", operation):
        #   predefined_file = '/home/vallen/Workspace/MacroCounter'\
        #                        f'/Predefined_Meals/{operation}.txt'
        #    counter.check_existence()
        #    counter.update_file(predefined_file)
        if operation == "cf":
            counter.check_existence() # to give a sense of control
        if operation == "uf":
            counter.check_existence()
            counter.update_file()
        if operation == "dm":
            display_monthly_data(target_directory)
        if operation == "df":
            display_data(target_file)

# csv? never met her.
# what's pathlib?
# TODO: rewrite this entire mess.
# debug previous file data is not written along with new data entries @line: 34
# format file view @line: 165.
