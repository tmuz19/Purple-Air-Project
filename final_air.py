"""This program displays PurpleAir air quality data. """

import csv
from enum import Enum
filename = 'purple_air.csv'


class Stats(Enum):
    """ Used to indicate which statistic is requested. """
    MIN = 0
    AVG = 1
    MAX = 2


class EmptyDatasetError(Exception):
    """ Error raised when a method relies on a non-empty dataset
    but the dataset is empty.
    """
    pass


class NoMatchingItems(Exception):
    """ Error raised when there is no data at the requested row and
    column.
    """
    pass


class DataSet:
    """ the DataSet class will present summary tables based on
    information imported from a .csv file
    """

    def __init__(self, header=""):
        self._zips = dict()
        self._times = list()
        self._data = None
        self.header = header

    @property
    def header(self):
        """ Return the value of the _header property. """
        return self._header

    @header.setter
    def header(self, new_header: str):
        """ Set the value of the _header property """
        if len(new_header) <= 30:
            self._header = new_header
        else:
            raise ValueError

    def _initialize_labels(self):
        """ Examine the category labels in self.__data and create a set
        for each category containing the labels.
        """
        self._zips = dict()
        temp_tod = set()
        for item in self._data:
            self._zips[item[0]] = True
            temp_tod.add(item[1])
        self._times = list(temp_tod)

    def load_default_data(self):
        self._data = [('12345', 'Morning', 1.1),
                      ('94022', 'Morning', 2.2),
                      ('94040', 'Morning', 3.0),
                      ('94022', 'Midday', 1.0),
                      ('94040', 'Morning', 1.0),
                      ('94022', 'Evening', 3.2)]
        self._initialize_labels()

    def _cross_table_statistics(self, descriptor_one: str,
                                descriptor_two: str):
        if not self._data:
            raise EmptyDatasetError

        value_list = [float(item[2]) for item in self._data if
                      item[0] == descriptor_one and item[1] == descriptor_two]

        if len(value_list) == 0:
            raise NoMatchingItems

        return min(value_list), sum(value_list) / len(value_list), \
            max(value_list)

    def display_cross_table(self, stat: Stats):
        """ Given a stat from DataSet.Stats, produce a table that
        shows the value of that stat for every pair of labels from the
        two categories.
        """

        if not self._data:
            print("Please load a dataset first")
            return
        print()
        print(f"{' ':7}", end="")
        for item in self._times:
            print(f"{item:>8}", end="")
        print()
        for item_one, value in self._zips.items():
            if not value:
                continue
            print(f"{item_one:<7}", end="")
            for item_two in self._times:
                try:
                    value = self._cross_table_statistics(item_one,
                                                         item_two)[stat.value]
                    print(f"{value:>8.2f}", end="")
                except NoMatchingItems:
                    print(f"{'N/A':>8}", end="")
            print()

    def get_zips(self):
        return self._zips.copy()

    def toggle_zip(self, target_zip: str):
        """ Given a category and label, toggle the label between
        active and inactive
        """
        if target_zip not in self._zips:
            raise LookupError
        self._zips[target_zip] = not self._zips[target_zip]

    def load_file(self):
        with open(filename, newline='') as file:
            data = [(data[1], data[4],data[5])for data in csv.reader(file)][1:]
            print(f"{len(data)} lines of data were downloaded")
        self._data = data
        self._initialize_labels()


def print_menu():
    """ Display the main menu text. """
    print("Main Menu")
    print("1 - Print Average Particulate Concentration by Zip Code and Time")
    print("2 - Print Minimum Particulate Concentration by Zip Code and Time")
    print("3 - Print Maximum Particulate Concentration by Zip Code and Time")
    print("4 - Adjust Zip Code Filters")
    print("5 - Load Data")
    print("9 - Quit")


def menu(my_dataset: DataSet):
    """ present user with options to access the PurpleAir dataset """

    print()
    while True:
        print()
        print(my_dataset.header)
        print_menu()
        try:
            selection = int(input("What is your choice? "))
        except ValueError:
            print("Please enter a number only")
            continue
        if selection == 1:
            my_dataset.display_cross_table(Stats.AVG)
        elif selection == 2:
            my_dataset.display_cross_table(Stats.MIN)
        elif selection == 3:
            my_dataset.display_cross_table(Stats.MAX)
        elif selection == 4:
            manage_filters(my_dataset)
        elif selection == 5:
            my_dataset.load_file()
        elif selection == 9:
            print("Goodbye!  Thank you for using the database")
            break
        else:
            print("That's not a valid selection")


def main():
    """ Run the purple air database application. """
    name = input("Please enter your name: ")
    message = "Hi " + name + ", welcome to the Air Quality database."
    print(message)
    while True:
        print("Enter a header for the menu: ")
        header = input()
        try:
            purple_air = DataSet(header)
            break
        except ValueError:
            print("Header must be less than or equal to thirty "
                  "characters long")
    menu(purple_air)


def manage_filters(my_dataset: DataSet):
    """ Allow the user to see all the labels in a category, and
    whether they are active.  The user can toggle the active
    status of any label.
    Note: dataset.get_active_labels() may raise EmptyDatasetError
    """
    zips_list = list(my_dataset.get_zips())
    if not zips_list:
        print("Please load a dataset first")
        return
    while True:
        zips_dict = my_dataset.get_zips()
        print("The following labels are in the dataset:")
        for item, label in enumerate(zips_list, 1):
            print(f"{item}: {label:<10} "
                  f"{'ACTIVE' if zips_dict[label] else 'INACTIVE'} ")
        selection = input("Please select an item to toggle or press "
                          "enter/return when you are finished.")
        if selection == '':
            break
        try:
            num_selection = int(selection) - 1
        except ValueError:
            print("Please enter a number or enter/return to exit")
            continue
        if 0 <= num_selection < len(zips_list):
            my_dataset.toggle_zip(zips_list[num_selection])
        else:
            print("Please enter a number from the list")


if __name__ == "__main__":
    main()
r"""
---Sample Run 1---
Please enter your name: Talha
Hi Talha, welcome to the Air Quality database.
Enter a header for the menu: 
Cleaner Air


Cleaner Air
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 1
Please load a dataset first

Cleaner Air
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 5
6147 lines of data were downloaded

Cleaner Air
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 1

        Morning  Midday   Night Evening
94028      1.54    2.92    1.58    2.26
94304      1.36    2.89    1.23    1.17
94022      1.50    2.92    1.32    1.22
94024      1.71    3.27    1.69    3.42
94040      1.86    3.28    2.47    4.57
94087      2.24    3.92    2.31    4.77
94041      2.41    3.52    3.43    4.53
95014      1.06    3.29    2.19    2.38

Cleaner Air
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 2

        Morning  Midday   Night Evening
94028      0.00    0.00    0.00    0.00
94304      0.00    0.00    0.00    0.00
94022      0.00    0.00    0.00    0.00
94024      0.00    0.00    0.00    0.00
94040      0.00    0.00    0.00    0.00
94087      0.00    0.00    0.00    0.00
94041      0.00    0.00    0.00    0.00
95014      0.00    0.00    0.00    0.00

Cleaner Air
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 3

        Morning  Midday   Night Evening
94028     25.72   24.21   25.00   79.88
94304      9.66   20.93    9.92    9.73
94022     12.90   26.59   14.38   11.53
94024     15.12   29.17    9.67   37.57
94040     10.49   25.95   20.34   44.05
94087      9.39   26.48   13.14   38.11
94041      8.02   25.89   19.67   31.82
95014      9.95   25.00   37.82   69.05

Cleaner Air
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 4
The following labels are in the dataset:
1: 94028      ACTIVE 
2: 94304      ACTIVE 
3: 94022      ACTIVE 
4: 94024      ACTIVE 
5: 94040      ACTIVE 
6: 94087      ACTIVE 
7: 94041      ACTIVE 
8: 95014      ACTIVE 
Please select an item to toggle or press enter/return when you are finished.8
The following labels are in the dataset:
1: 94028      ACTIVE 
2: 94304      ACTIVE 
3: 94022      ACTIVE 
4: 94024      ACTIVE 
5: 94040      ACTIVE 
6: 94087      ACTIVE 
7: 94041      ACTIVE 
8: 95014      INACTIVE 
Please select an item to toggle or press enter/return when you are finished.

Cleaner Air
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 3

        Morning  Midday   Night Evening
94028     25.72   24.21   25.00   79.88
94304      9.66   20.93    9.92    9.73
94022     12.90   26.59   14.38   11.53
94024     15.12   29.17    9.67   37.57
94040     10.49   25.95   20.34   44.05
94087      9.39   26.48   13.14   38.11
94041      8.02   25.89   19.67   31.82

Cleaner Air
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 9
Goodbye!  Thank you for using the database

Process finished with exit code 0
"""