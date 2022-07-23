"""
This program allows the user to filter the HydroDam dataset
and sort by different fields.
Name: Andrew Henin
Date: April 2022
"""

from hydrodam_lab import *

def main():
    dataList = readData()
    createObjects(dataList)
    currList = dataList.copy()


    choice = getInput()
    while choice != "6":
        if choice == "1":
            state = input("State Name? ").lower()
            currList = filterState(currList, state)
            printResults(currList, choice)

        elif choice == "2":
            min = validYear(0, "min")
            max = validYear(min, "max")
            currList = filterYear(currList, min, max)
            printResults(currList, choice)

        elif choice == "3":
            mySort(currList, "state")
            printResults(currList, choice)

        elif choice == "4":
            mySort(currList, "year")
            printResults(currList, choice)

        elif choice == "5":
            currList = dataList.copy()
            print("\nResetting list to all dams\n")

        choice = getInput()

    print()
    print("Goodbye!")



def readData():
    """
    This function reads the data from the dataset file and calls another
    function to create a viable data list
    parameters: none
    returns: dataList
    """
    file = open("/data/cs21/hydropower/hydropower.csv", "r")
    dataList = file.readlines()
    file.close()
    fixList(dataList)

    return dataList



def fixList(list):
    """
    This function fixes the list by changing it into lists of records
    inside one list
    parameters: list
    """
    for i in range(len(list)):
        list[i] = list[i].rstrip()
        list[i] = list[i].split(",")



def getInput():
    """
    This function prompts the user to choose one of the choices: to filter
    (either by state name or year), to sort (either by name or year), to reset
    list to all dams, or to quit.
    parameters: none
    returns: choice -if choice is valid
             or it calls itself in case of invalid inputs
    """

    print()
    print("Please select one of the following choices:")
    print("1. Filter dams by state name")
    print("2. Filter dams by year")
    print("3. Sort by state name")
    print("4. Sort by year")
    print("5. Reset list to all dams")
    print("6. Quit")
    print()

    choice = input("Choice? ")
    if choice in ["1", "2", "3", "4", "5", "6"]:
        return choice

    return getInput()



def createObjects(list):
    """
    This function converts the list into a list of HydroDam objects.
    parameters: list
    returns: none
    """

    for i in range(len(list)):
        newobj = HydroDam(list[i][0], list[i][1], list[i][2], list[i][3], \
float(list[i][4]), float(list[i][5]), int(list[i][6]))
        list[i] = newobj



def validYear(min, str):
    """
    This function checks if the year input is valid
    parameters: min -the minimum year input for comparison with the max year
                str -a string to optimize the message to user
    returns: int(year) -the final valid year input of type integer
    """

    print(str, "year?", end = ' ')
    year = input()
    while not year.isdigit():
        print("\nInvalid year, try again.\n")
        print(str, "year?", end = ' ' )
        year = input()

    if str == "max":
        while min > int(year):
             print("\nInvalid year, try again.\n")
             print(str, "year?", end = ' ' )
             year = input()

    return int(year)



def filterState(currList, state):
    """
    This function filters the current list according to input name
    parameters: currList -the current edited list of items
                state     -the input name of the state based on which
                          list will be filtered
    returns: newlist     -a list with all the final filtered records
    """

    newlist = []
    for i in range(len(currList)):
        if state in currList[i].get_state().lower():
            newlist.append(currList[i])

    return newlist



def filterYear(currList, min, max):
    """
    This function filters the current list according to the year input
    parameters: currList -the current list on which edits are applied
                min      -minimum year of the filtered records
                max      -maximum year of the filtered records
    returns: newlist
    """

    newlist = []
    for i in range(len(currList)):
        if (currList[i].get_year() >= min) and (currList[i].get_year() <= max):
            newlist.append(currList[i])

    return newlist



def mySort(list, str):
    """
    This function sorts the current list based on either name or year
    parameters: list -the current, most updated list of items
                str  -the string which decides the type of sort
    returns: None
    """

    if str == "state":
        for i in range(len(list)-1):
            min_idx = i
            for j in range(i+1, len(list)):
                if list[min_idx].get_state() > list[j].get_state():
                    min_idx = j
            list[i], list[min_idx] = list[min_idx], list[i]

    elif str == "year":
        for i in range(len(list)-1):
            min_idx = i
            for j in range(i+1, len(list)):
                if list[min_idx].get_year() > list[j].get_year():
                    min_idx = j
            list[i], list[min_idx] = list[min_idx], list[i]



def printResults(currList, choice):
    """
    This function prints the final results of either filtering or sorting
    parameters: currList -the final list with the results
    returns: None
    """

    if choice in ["1", "2"]:
        print("\nFound", len(currList), "matching records\n")
    elif choice == "3":
        print("\n Sorted by state\n")
    elif choice == "4":
        print("\n Sorted by year\n")


    print("%15s %15s %10s %12s %7s %7s %7s" % ("Dam Name", "Watercourse", \
    "County", "State", "Height", "Lenght", "Year"))
    print("-"*80)
    for i in range(len(currList)):
        print("%15s %15s %10s %12s %7.1f %7.1f %7d" % (currList[i].get_name()[0:15], \
currList[i].get_watercourse()[0:15], currList[i].get_county()[0:10], \
currList[i].get_state()[0:8], currList[i].get_height(), \
currList[i].get_length(), currList[i].get_year()))
    print()
    print()


main()
