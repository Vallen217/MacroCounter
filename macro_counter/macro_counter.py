"""Track and record macronutritional information and calories.

macro_counter primarily writes user inputed data onto .txt files
systematically separated by days, and placed in directories separated by months and years,
which are located in "/home/$USER/Documents/Health/Macronutritional_intake".
"""
import os
import re
from datetime import datetime


def pad(word):
    """Generate uniform spacing for .txt files.

    Args:
        word (String): A string.

    Returns:
        A number of whitespaces = 12 - len(word).
    """
    return " " * (12 - len(str(word)))


class MacroCounter:
    """Refer to line: 1 - 6.

    Attributes:
        target_directory: The directory containing the `target_files`.
        target_file: Targeted file you wish to access within the `target_directory`.
        data: Multidimentional array of macronutrional information \
                i.e. [[calories], [fat], [carbohydrates], [protein]].
        totals: Array of the sums of each array from `data`.
    """

    def __init__(self, target_directory, target_file):
        """Object constructor.

        Args:
            target_directory (string: absolute directory path): targeted directory.
            target_file (string: absolute file path): targeted file.
        """
        self.target_directory = target_directory
        self.target_file = target_file
        self.data = [], [], [], []
        self.totals = [0, 0, 0, 0]

    def check_existence(self, predefined=False):
        """Create the file and/or directories if they don't already exist.

        Args:
            predefined (boolean): Returns `predefined` if True.

        Returns:
            None.
        """
        if os.path.exists(self.target_directory):
            pass
        else:
            os.mkdir(self.target_directory)
        os.chdir(self.target_directory)

        if not os.path.exists(self.target_file):
            with open(self.target_file, "x", encoding="utf-8"):
                pass

        if predefined is True:
            return predefined_meals()
        return None  # 'return None' statement to satisfy pylint diagnostics

    # saves the file data to rewrite it in write_file() with the new data.
    def compile_data(self, file_name, clean_data=False):
        """Read lines of data from `file_name` and appends it to `self.data`.

        Args:
            file_name (string: absolute file path): Targeted file.
            clean_data (boolean): cleans each array in `self.data` if true.

        """
        # self.data must be cleared to properly recompile data in some cases
        if clean_data:
            for i in range(len(self.data)):
                self.data[i].clear()

        with open(file_name, "r", encoding="utf-8") as read_file:
            for line in read_file:
                if line == "\n":
                    break

                if re.match(r"\d+\.\dg?", line):
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

    def collect_data(self):
        """Collect macronutrional data from user input and append it to `self.data`.

        Returns:
            `self.write_data()`
        """
        print(
            "\n(rl#)  - Removes the last n file entry lines"
            "\n(rlq#) - Removes the last n file entry lines and quit "
            "\n(q)    - Quit the loop\n"
            "\nPress any key to continue"
        )
        while True:
            operation = str(input("-")).lower()
            if operation == "q":
                break

            if re.match("rlq?[0-9]*", operation):
                iterations = (
                    int(operation[3:]) if "q" in operation else int(operation[2:])
                )
                for i in range(iterations):
                    for j in range(4):
                        self.data[j].pop()

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
        """Write information stored in `self.data` to `self.target_file`.

        Returns:
            `display_data(self.target_file)`
        """
        self.totals = [sum(self.data[i]) for i in range(len(self.data))]
        ratio = 100 / (self.totals[1] + self.totals[2] + self.totals[3])
        temp = [f"{round(ratio * self.totals[i], 1)}%" for i in range(1, 4)]
        relative_per = [f"{v}{pad(v)}" for v in temp]

        with open(self.target_file, "w", encoding="utf-8") as write_file:
            write_file.write(
                f"Cal:{pad('Cal:')}Fat:{pad('Fat:')}"
                f"Carb:{pad('Carb:')}Protein:{pad('Protein:')}"
            )

        with open(self.target_file, "a", encoding="utf-8") as append_file:
            for i in range(len(self.data[0])):
                append_file.write("\n")
                for j in range(4):
                    if j == 0:
                        append_file.write(
                            f"{self.data[j][i]}" f"{pad(self.data[j][i])}"
                        )
                    else:
                        append_file.write(
                            f"{self.data[j][i]}g" f"{pad(f'{self.data[j][i]}g')}"
                        )

            append_file.write(
                f"\n\nTotal Amounts & Relative Percentages:\n"
                f"{self.totals[0]}{pad(self.totals[0])}"
                f"{self.totals[1]}g{pad(f'{self.totals[1]}g')}"
                f"{self.totals[2]}g{pad(f'{self.totals[2]}g')}"
                f"{self.totals[3]}g"
                f"\n{' ' * 12}{relative_per[0]}"
                f"{relative_per[1]}{relative_per[2]}"
            )
        return display_data(self.target_file)


# This is an appalling mess, but it works.
def predefined_meals():
    """Access point for predefined meal files in "macro_counter/macro_counter/predefined_meals/", \
        e.g. creating new, modifying, and/or displaying `predefined_meal` files.

    Returns:
        `main()`.
    """
    target_directory = (
        "/home/vallen/Workspace/macro_counter/macro_counter/predefined_meals"
    )
    print(
        "\n(cf)  - Create new predefined meal"
        "\n(mf)  - Modify predefined meal"
        "\n(df)  - Display predefined meals"
        "\n(q)   - Quit the loop"
    )
    while True:
        operation = str(input("-")).lower()
        if operation == "q":
            return main()

        if operation == "cf":
            file_name = f"m{len(os.listdir(target_directory)) + 1}.txt"
            target_file = os.path.join(target_directory, file_name)
            counter = MacroCounter(target_directory, target_file=target_file)
            counter.check_existence(predefined=True)

        if operation == "mf":
            print("Enter a file to modify from:")
            for file in os.listdir(target_directory):
                print(file)

            try:
                file_name = str(input("-"))
                if ".txt" not in file_name:
                    file_name = f"{file_name}.txt"

                if file_name not in os.listdir(target_directory):
                    raise FileNotFoundError

            except FileNotFoundError:
                print("Error: invalid file name.")
                return predefined_meals()

            target_file = os.path.join(target_directory, file_name)
            counter = MacroCounter(target_directory, target_file)
            counter.compile_data(target_file, clean_data=True)
            counter.collect_data()

        if operation == "df":
            view_previous_data(target_directory, operation, predefined=True)


def display_data(file):
    """Print file contents to the terminal.

    Args:
        file (string: absolute file path): Prints the content of the given file.
    """
    print()
    with open(file, "r", encoding="utf-8") as read_file:
        for data in read_file:
            print(data.rstrip("\n"))
    print("\n")


def display_monthly_data(directory):
    """Compile and print data about the sum, mean, and relative percentages \
                of all files within `directory` to the terminal.

    Args:
        directory (string: absolute directory path): targeted directory.
    """
    totals = [0, 0, 0, 0]
    os.chdir(directory)
    file_list = os.listdir(directory)

    for file in file_list:
        with open(f"{directory}/{file}", encoding="utf-8") as read_file:
            lines = read_file.readlines()
        temp = [lines[i + 2].split() for i, line in enumerate(lines) if line == "\n"]
        for j in range(4):
            if "g" in temp[0][j]:
                temp[0][j] = temp[0][j][0:-1]
            # Ignore the GeneralTypeError below. This operation works fine.
            totals[j] += float(temp[0][j])

    relative_monthly_percent = [
        f"{round((100 / (sum(totals[1:]))) *  totals[i], 1)}%" for i in range(1, 4)
    ]
    mean_amounts = [round(totals[i] / len(file_list), 1) for i in range(4)]

    print(
        f"\nCal:{pad('Cal:')}Fat:{pad('Fat:')}"
        f"Carb:{pad('Carb:')}Protein:{pad('Protein:')}\n"
    )
    print("Contemporary monthly total amounts: ")
    print(f"{totals[0]}{pad(totals[0])}", end="")
    for val in totals[1:]:
        print(f"{val}g{pad(f'{val}g')}", end="")

    print("\n\nMean daily amounts: ")
    print(f"{mean_amounts[0]}{pad(mean_amounts[0])}", end="")
    for val in mean_amounts[1:]:
        print(f"{val}g{pad(f'{val}g')}", end="")

    print("\n\nMean daily relative percentages: ")
    print(pad(""), end="")
    for val in relative_monthly_percent:
        print(f"{val}{pad(val)}", end="")
    print("\n")


def view_previous_data(parent_directory, operation, predefined=False):
    """Print information of antique files and/or directories to the terminal.

    Args:
        parent_directory (string: absolute directory path): \
                The parent directory of the targeted directory.
        operation (string): A string input passed from the calling code \
                to determine what information to display
        predefined (boolean): Predifined files have largely divergant pathing.

    Returns:
        `display_monthly_data(target_directory)` or `display_data(target_file)`
        depending on what `operation` was passed from the calling code.
    """
    if not predefined:
        print("\nEnter a relative directory from:")
        for directory in os.listdir(parent_directory):
            print(directory)

        try:
            directory_name = str(input("\n-"))
            if directory_name not in os.listdir(parent_directory):
                raise FileNotFoundError

        except FileNotFoundError:
            print("Error: invalid directory.")
            return None  # 'return None' statement to satisfy pylint diagnostics

        target_directory = os.path.join(parent_directory, directory_name)

    else:
        target_directory = parent_directory

    if operation == "dpm":
        return display_monthly_data(target_directory)

    print("\nEnter a file to view from:")
    for file in os.listdir(target_directory):
        print(file)

    try:
        file_name = str(input("\n-"))
        if ".txt" not in file_name:
            file_name = f"{file_name}.txt"

        if file_name not in os.listdir(target_directory):
            raise FileNotFoundError

    except FileNotFoundError:
        print("Error: invalid file.")
        return None  # 'return None' statement to satisfy pylint diagnostics

    target_file = os.path.join(target_directory, file_name)
    return display_data(target_file)


def main():
    """Entry point for program execution.

    Returns:
        Everything else.
    """
    print(
        "\n(mf)  - Modify file"
        "\n(dpf) - Display previous files"
        "\n(dpm) - Display previous monthly data"
        "\n(df)  - Display file"
        "\n(dm)  - Display monthly data"
        "\n(pd)  - Predefined meals"
        "\n(m#)  - Append predefined meal m#"
        "\n(q)   - Quit the program"
    )

    parent_directory = "/home/vallen/Documents/Health/Macronutritional_intake"
    directory_name = f"{datetime.now().year}-{datetime.now().month}"
    target_directory = os.path.join(parent_directory, directory_name)
    file_name = f"{datetime.now().day}.txt"
    target_file = os.path.join(target_directory, file_name)

    counter = MacroCounter(target_directory, target_file)
    counter.check_existence()

    while True:
        operation = str(input("-")).lower()
        if operation == "q":
            break

        if operation == "pd":
            return predefined_meals()

        if operation in ("dpf", "dpm"):
            view_previous_data(parent_directory, operation)

        if re.match("m[0-9]+", operation):
            predefined_file = (
                "/home/vallen/Workspace/macro_counter"
                f"/macro_counter/predefined_meals/{operation}.txt"
            )
            # 1st function call is to save pre-existing file data.
            # 2nd function call is to append predefined data to the file.
            counter.compile_data(target_file, clean_data=True)
            counter.compile_data(predefined_file)
            counter.write_file()

        if operation == "mf":
            counter.compile_data(target_file, clean_data=True)
            counter.collect_data()
        if operation == "df":
            display_data(target_file)
        if operation == "dm":
            display_monthly_data(target_directory)
    return None  # 'return None' statement to satisfy pylint diagnostics


if __name__ == "__main__":
    main()
