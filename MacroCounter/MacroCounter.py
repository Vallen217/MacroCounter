import os
import re
from datetime import datetime

class MacroCounter:
    def __init__(self, target_directory, target_file):
        self.target_directory = target_directory
        self.target_file = target_file
        self.data = [], [], [], []
        self.totals = [0, 0, 0, 0]

    def check_existence(self, predefined=False):
        if os.path.exists(self.target_directory):
            pass
        else:
            os.mkdir(self.target_directory)
        os.chdir(self.target_directory)

        try:
            with open(self.target_file, 'x') as _:
                pass

        except FileExistsError:
            pass

        if predefined == True:
            return predefined_meals()
        else:
            return

    # saves the file data to rewrite it in write_file() with the new data.
    def compile_data(self, file_name, clean_data=False):
        # self.data must be cleared to properly recompile data in certain cases
        if clean_data:
            [self.data[i].clear() for i in range(len(self.data))]

        with open(file_name, 'r') as rf:
            for line in rf:
                if line == "\n":
                    break
                
                if re.match("\d+\.\dg?", line):
                    for i, datum in enumerate(line.split()):
                        if "g" in datum[-1]:
                            datum = datum[0:-1]
                        datum = float(datum)

                        # caffeine fueled logic.
                        if i % 4 == 0:
                            self.data[0].append(datum)
                        if (i - 1) % 4 == 0:
                            self.data[1].append(datum)
                        if i % 2 == 0 and i % 4 != 0:
                            self.data[2].append(datum)
                        if (i - 1) % 2 == 0 and (i - 1) % 4 != 0:
                            self.data[3].append(datum)
        return

    def modify_file(self):
        print(
                "\n(rln)  - Removes the last n file entry lines"
                "\n(rlqn) - Removes the last n file entry lines and quit "
                "\n(q)    - Quit the loop\n"
                "\nPress any key to continue"
        )
        while True:
            operation = str(input("-")).lower()
            if operation == "q":
                break

            if re.match("rlq?[0-9]*", operation):
                iterations = int(operation[3:]) if "q" in operation\
                        else int(operation[2:])
                for i in range(iterations):
                    [self.data[j].pop() for j in range(4)]
                if "q" in operation:
                    break

            try:
                self.data[0].append(float(input("Calorie: ")))
                self.data[1].append(float(input("Fat: ")))
                self.data[2].append(float(input("Carb: ")))
                self.data[3].append(float(input("Protein: ")))

            except ValueError:
                break
            
        # catch potential index errors.
        for i in range(4):
            if len(self.data[i]) != len(self.data[3]):
                self.data[i].pop()
        return self.write_file()

    def write_file(self):
        self.totals = [sum(self.data[i]) for i in range(len(self.data))]
        pad = lambda word: " " * (12 - len(str(word)))
        ratio = 100 / (self.totals[1] + self.totals[2] + self.totals[3])
        temp = [f"{round(ratio * self.totals[i], 1)}%" for i in range(1, 4)]
        relative_per = [f"{v}{pad(v)}" for v in temp]

        with open(self.target_file, 'w') as wf:
            wf.write(
                    f"Cal:{pad('Cal:')}Fat:{pad('Fat:')}"
                    f"Carb:{pad('Carb:')}Protein:{pad('Protein:')}"
            )

        with open(self.target_file, 'a') as af:
            for i in range(len(self.data[0])):
                af.write("\n")
                for j in range(4):
                    if j == 0:
                        af.write(f"{self.data[j][i]}"
                                f"{pad(self.data[j][i])}")
                    else:
                        af.write(f"{self.data[j][i]}g"
                        f"{pad(f'{self.data[j][i]}g')}")

            af.write(
                    f"\n\nTotal Amounts & Relative Percentages:\n"
                    f"{self.totals[0]}{pad(self.totals[0])}"
                    f"{self.totals[1]}g{pad(f'{self.totals[1]}g')}"
                    f"{self.totals[2]}g{pad(f'{self.totals[2]}g')}"
                    f"{self.totals[3]}g"
                    f"\n{' ' * 12}{relative_per[0]}"
                    f"{relative_per[1]}{relative_per[2]}"
                    )
        return display_data(self.target_file)

# This is appalling, but it works.
def predefined_meals():
    target_directory= '/home/vallen/Workspace/MacroCounter/MacroCounter/Predefined_Meals'
    print(
        "\n(cp)  - Create new predefined meal"
        "\n(mp)  - Modify predefined meal"
        "\n(dp)  - Display predefined meals"
        "\n(q)   - Quit the loop"
        "\n"
    )

    operation = str(input("-")).lower()
    if operation == "q":
        return main()

    if operation == "cp":
        file_name = f"m{len(os.listdir(target_directory)) + 1}.txt"
        target_file = os.path.join(target_directory, file_name)
        counter = MacroCounter(target_directory, target_file=target_file)
        counter.check_existence(predefined=True)

    if operation == "mp":
        print("Enter a file to modify from:")
        [print(file) for file in os.listdir(target_directory)]

        try:
            file_name = str(input())
            if ".txt" not in file_name:
                file_name = f"{file_name}.txt"

            if file_name not in os.listdir(target_directory):
                raise FileNotFoundError

        except FileNotFoundError:
            print(f"Error: '{file_name}' is not a valid file")
            return predefined_meals() 

        target_file = os.path.join(target_directory, file_name)
        counter = MacroCounter(target_directory, target_file)
        counter.compile_data(target_file, clean_data=True)
        counter.modify_file()
    
    if operation == "dp":
        view_previous_data(target_directory, operation, predefined=True)
        return predefined_meals()

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
        temp = [lines[i+2].split() for\
                i, line in enumerate(lines) if line == "\n"]
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

def view_previous_data(parent_directory, operation, predefined=False):
    if not predefined:
        print("\nEnter a relative directory from:")
        [print(dir) for dir in os.listdir(parent_directory)]

        try:
            directory_name = str(input("\n"))
            if directory_name not in os.listdir(parent_directory):
                raise FileNotFoundError

        except FileNotFoundError:
            print(f"Error: '{directory_name}' is not a valid directory.")
            return

        target_directory = os.path.join(parent_directory, directory_name)

    else:
        target_directory= parent_directory

    if operation == "dpm":
        return display_monthly_data(target_directory)

    else:
        print("\nEnter a file to view from:")
        [print(file) for file in os.listdir(target_directory)]

        try:
            file_name = str(input("\n"))
            if ".txt" not in file_name:
                file_name = f"{file_name}.txt"

            if file_name not in os.listdir(target_directory):
                raise FileNotFoundError

        except FileNotFoundError:
            print(f"Error: '{file_name}' is not a valid file.")
            return

        target_file = os.path.join(target_directory, file_name)
        return display_data(target_file)

def main():
    print(
        "\n(mf)  - Modify file"
        "\n(dpf) - Display previous files"
        "\n(dpm) - Display previous monthly data"
        "\n(df)  - Display file"
        "\n(dm)  - Display monthly data"
        "\n(pd)  - Predefined meals"
        "\n(q)   - Quit the program"
        )

    parent_directory = '/home/vallen/Documents/Health/Macronutritional_intake'
    directory_name = f'{datetime.now().year}-{datetime.now().month}'
    target_directory = os.path.join(parent_directory, directory_name)
    file_name = f'{datetime.now().day}.txt'
    target_file = os.path.join(target_directory, file_name)

    counter = MacroCounter(target_directory, target_file)
    counter.check_existence()
    
    while True:
        operation = str(input("-")).lower()
        if operation == "q":
            break

        if operation == "pd":
            return predefined_meals()

        if operation == "dpf" or operation == "dpm":
            view_previous_data(parent_directory, operation)

        if re.match("m[0-9]+", operation):
            predefined_file = '/home/vallen/Workspace/MacroCounter'\
                    f'/MacroCounter/Predefined_Meals/{operation}.txt'
            # 1st function call is to save pre-existing file data.
            # 2nd function call is to append predefined data to the file.
            counter.compile_data(target_file, clean_data=True)
            counter.compile_data(predefined_file)
            counter.write_file()

        if operation == "mf":
            counter.compile_data(target_file, clean_data=True)
            counter.modify_file()
        if operation == "df":
            display_data(target_file)
        if operation == "dm":
            display_monthly_data(target_directory)
    return

if __name__ == "__main__":
    main()
