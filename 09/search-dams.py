"""
This program imports a dataset including records
about dams. It enables the user to search for dams by
category: either dam name or location state
Name: Andrew Henin
Date: April 2022
"""
from hydrodam_lab import *

def main():

    dataList = readData()
    createObject(dataList)
    user_input = getCat()
    while user_input != 3:
        if user_input == 1:
            name = input("Dam name (or prefix)? ").lower()
            nameIdx = nameSearch(name, dataList)
            if nameIdx == -1:
                printMsg(user_input)
            else:
                nresult = createResults(dataList, nameIdx, name)
                display(nresult)

        elif user_input == 2:
            loc = input("Location (state)? ").lower()
            lresult = locSearch(loc, dataList)
            if len(lresult) == 0:
                printMsg(user_input)
            else:
                display(lresult)

        user_input = getCat()


    print()
    print("Goodbye!")



def readData():
    """
    This function imports the data and calls other function to optimize the list.
    parameters: none
    returns: datalist -a list with all dams records
    """

    file = open("/data/cs21/hydropower/hydropower.csv", "r")
    dataList = file.readlines()
    file.close()
    fixList(dataList)

    return dataList




def fixList(dataList):
    """
    This function manipulates the imported data list and fixes it by preparing
    it for use.
    parameters: dataList -which is the list of raw data
    returns: none
    """

    for i in range(len(dataList)):
        dataList[i] = dataList[i].rstrip()
        dataList[i] = dataList[i].split(",")



def createObject(dataList):
    """
    This function has a for loop that converts the elements of dataList
    to a list of objects that are of the class "HydroDam."
    parameters: dataList -the fixed list of imported data
    returns: none
    """

    for i in range(len(dataList)):
        newobj = HydroDam(dataList[i][0], dataList[i][1], dataList[i][2], \
dataList[i][3], float(dataList[i][4]), float(dataList[i][5]), \
int(dataList[i][6]))
        dataList[i] = newobj



def getCat():
    """
    This function prompts the user to enter which category they
    want to search by. They would enter "1" to search by dam name
    or "2" to search by state. If they want to quit, they will enter 3.
    parameters: none
    returns: user_input -which is either 1, 2, or 3
    """

    print()
    print("Please select one of the following choices:")
    print("1. Search by dam name")
    print("2. Search by dam location (state)")
    print("3. Quit")
    print()

    user_input = input("Choice? ")

    return getValid(user_input)




def getValid(user_input):
    """
    This function checks if the user input is valid, prints the
    appropriate messages and prompts them to input till they input
    a valid number.
    parameters: input -which is the user input
    returns: user_input -which is the valid input after input reiterations
    """

    while user_input not in ["1", "2", "3"]:
        print()
        print("Invalid choice, try again.")
        print()
        getCat()

    return int(user_input)



def nameSearch(name, dataList):
    """
    This function carries out binary search to find the records
    with the input name. It adds the whole record to an accumulator list.
    parameters: name -the user input of the name they are looking for.
    returns: nresult -a list with the search results
    """

    low = 0
    high = len(dataList) - 1

    while (low <= high):
        mid = (low + high)//2
        if dataList[mid].get_name().lower().startswith(name):
            return mid
        elif name < dataList[mid].get_name().lower()[0:len(name)]:
            high = mid - 1
        elif name > dataList[mid].get_name().lower()[0:len(name)]:
            low = mid + 1

    return -1


def createResults(dataList, index, search):
    """
    This function appends the initial match with the nearby matches into
    a list that is ready to be displayed.
    parameters: dataList -the grand list with all HydroDam objects
                index   -the index where the search starts
                search   -the user input for which the search is done
    reutrns: ready a list with all search results
    """

    ready = []
    backMatches = lookForwardBackward(dataList, index - 1, search, -1)
    for i in range(len(backMatches)):
        ready.append(backMatches[i])
    ready.append(dataList[index])
    frontMatches = lookForwardBackward(dataList, index + 1, search, 1)
    for i in range(len(frontMatches)):
        ready.append(frontMatches[i])

    return ready



def locSearch(loc, dataList):
    """
    This function carries out linear search to find the records that are in the
    same location. It calls another function to create a list with results.
    Parameters: loc -the user input of the state name
    dataList -the list with all the records
    """

    indices = []

    for i in range(len(dataList)):
        if loc in dataList[i].get_state().lower():
            indices.append(i)

    return arrange(indices, dataList)



def arrange(indices, dataList):
    """
    This function prepares a list with the search results
    parameters: indices -a list of indeices where matches were found
                dataList -the list of data that contains all records
    returns: ready -a comlete list with search matches ready to be used
    """

    ready = []
    for i in range(len(indices)):
        ready.append(dataList[indices[i]])

    return ready


def display(result):
    """
    This function prints the results of the search.
    parameters: result -a list with the search matches
    returns: none
    """

    print()
    print("%15s %15s %10s %12s %7s %7s %7s" % ("Dam Name", "Watercourse", \
    "County", "State", "Height", "Lenght", "Year"))
    print("-"*80)
    for i in range(len(result)):
        print("%15s %15s %10s %12s %7.1f %7.1f %7d" % (result[i].get_name()[0:15], \
result[i].get_watercourse()[0:15], result[i].get_county()[0:10], \
result[i].get_state()[0:8], result[i].get_height(), \
result[i].get_length(), result[i].get_year()))
    print()
    print()



def printMsg(user_input):
    """
    This function prints out the appropriate messages when no search matches
    are found.
    parameters: user_input -the choice input of the user
    returns: none
    """
    print()
    if user_input == 1:
        print("Could not find any records matching that name")

    elif user_input == 2:
        print("Could not find any records matching that location")
    print()



main()
