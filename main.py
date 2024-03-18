# Jonathan Johnson
# Student ID: 011009146
# 03/18/24

from datetime import time
from truck import Truck
from package import Package
from hashtable import ChainingHashTable
import csv

myHash = ChainingHashTable()

# --------------------------------------- Load Data ---------------------------------------

# create instances of packages using csv data and add them to a list
packageList = list()
def loadPackageData(filename):
    csv_directory = "CSV/"  # Specify the directory name
    file_path = csv_directory + filename  # Construct the full file path
    try:
        with open(file_path) as packageInfo:  # Open the CSV file using the full file path
            packageData = csv.reader(packageInfo, delimiter=',')
            next(packageData)
            for package in packageData:
                pPackageID = int(package[0])
                pAddress = package[1]
                pCity = package[2]
                pState = package[3]
                pZip = package[4]
                pDeliveryDeadline = package[5]
                pMass = package[6]
                pNotes = package[7]
                pStatus = "at the hub"
                pDeliveryTime = None
                packageData = Package(pPackageID, pAddress, pCity, pState, pZip, pDeliveryDeadline, pMass, pNotes, pStatus, pDeliveryTime)
                myHash.insert(pPackageID, packageData)
                packageList.append(package)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found in directory '{csv_directory}'.")

# load the distances from csv data and add them to a list
distanceList = list()
def loadDistanceData(filename):
    csv_directory = "CSV/"
    file_path = csv_directory + filename
    try:
        with open(file_path) as distanceInfo:
            distanceData = csv.reader(distanceInfo, delimiter=',')
            next(distanceData)
            for distance in distanceData:
                distanceList.append(distance)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found in directory '{csv_directory}'.")

# load addresses from csv data and add them to a list
addressList = list()
def loadAddressData(filename):
    csv_directory = "CSV/"
    file_path = csv_directory + filename
    try:
        with open(file_path) as addressInfo:
            addressData = csv.reader(addressInfo, delimiter=',')
            next(addressData)
            for address in addressData:
                addressList.append(address)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found in directory '{csv_directory}'.")


# load in the csv files
loadPackageData('Package.csv')
loadDistanceData('Distance.csv')
loadAddressData('Address.csv')

# --------------------------------------- Various Methods ---------------------------------------

def getAddressIDFromPackageID(packageID):
    addressReturned = None
    for index, package in enumerate(packageList):
        if packageID == index + 1:
            addressReturned = package[1]
    for address in addressList:
        if addressReturned == address[2]:
            return int(address[0])

def getDistance(packageA, packageB):
    return float(distanceList[packageA][packageB])

# --------------------------------------- Algorithm ---------------------------------------

def nearestNeighbor(truck):
    packageNNRoute = []
    currentRoute = []
    for package in truck.packages:
        currentRoute.append(package.PackageID)


    nearestInitialDistance = float('inf')
    nearestPackage = None
    for package in currentRoute:
        distance = getDistance(0, getAddressIDFromPackageID(package))
        if distance < nearestInitialDistance:
            nearestInitialDistance = distance
            nearestPackage = package
    packageNNRoute.append(nearestPackage)
    currentRoute.remove(nearestPackage)


    while len(currentRoute) > 0:
        nearestDistance = float('inf')
        for package in currentRoute:
            distance = getDistance(getAddressIDFromPackageID(packageNNRoute[-1]), getAddressIDFromPackageID(package))
            if distance < nearestDistance:
                nearestDistance = distance
                nearestPackage = package
        packageNNRoute.append(nearestPackage)
        currentRoute.remove(nearestPackage)
    return packageNNRoute


# --------------------------------------- Trucks ---------------------------------------

truck1 = Truck(1, 0, 0, set())
truck2 = Truck(2, 0, 0, set())
truck3 = Truck(3, 0, 0, set())

packageTruck1_ids = [14, 15, 16, 34, 20, 21, 13, 39, 4, 40, 19, 27, 35, 12, 23, 11]
for package_id in packageTruck1_ids:
    truck1.add(myHash.search(package_id))
truck1nnRoute = nearestNeighbor(truck1)
packageTruck2_ids = [6, 31, 32, 25, 26, 3, 18, 36, 38, 28, 9, 10, 2, 33, 17, 22]
for package_id in packageTruck2_ids:
    truck2.add(myHash.search(package_id))
truck2nnRoute = nearestNeighbor(truck2)
packageTruck3_ids = [37, 5, 30, 8, 7, 29, 1, 24]
for package_id in packageTruck3_ids:
    truck3.add(myHash.search(package_id))
truck3nnRoute = nearestNeighbor(truck3)

# --------------------------------------- Menu Methods ---------------------------------------

def getTimeAndMileage(truckNNRoute):
    totalMileage = 0
    truckLocation = 0
    mileageList = []
    for i in truckNNRoute:
        totalMileage = totalMileage + getDistance(truckLocation, getAddressIDFromPackageID(i))
        mileageList.append(totalMileage)
        truckLocation = getAddressIDFromPackageID(i)

    if truckNNRoute == truck2nnRoute:
        startTime = (9 * 60) + 15
    else:
        startTime = 8 * 60
    lastTravelDistance = 0
    travelTimeMinutes = []
    deliveryTimeList = []
    for i in mileageList:
        travelTimeMinutes.append(round((i - lastTravelDistance) / 0.3))
        lastTravelDistance = i
    for i in travelTimeMinutes:
        startTime += i
        hours, minutes = divmod(startTime, 60)
        deliveryTimeList.append(f"{hours:02d}:{minutes:02d}")
    return mileageList, deliveryTimeList

TimeMileageListsTruck1 = getTimeAndMileage(truck1nnRoute)
TimeMileageListsTruck2 = getTimeAndMileage(truck2nnRoute)
TimeMileageListsTruck3 = getTimeAndMileage(truck3nnRoute)

def totalMileageCalculation():
    truck3ReturnTrip = getDistance(12, 0)
    totalMileage = TimeMileageListsTruck1[0][-1] + TimeMileageListsTruck2[0][-1] + truck3ReturnTrip + TimeMileageListsTruck3[0][-1]
    truck1Mileage = TimeMileageListsTruck1[0][-1]
    truck2Mileage = TimeMileageListsTruck2[0][-1]
    truck3Mileage = TimeMileageListsTruck3[0][-1] + truck3ReturnTrip
    return totalMileage, truck1Mileage, truck2Mileage, truck3Mileage

# Define the selectPackagesBetweenTime function
def selectPackagesBetweenTime(startTime, endTime):
    selected_packages = []
    for packageID in range(1, 41):
        packageDeliveryTime = time.fromisoformat(myHash.search(packageID).DeliveryTime)
        if startTime <= packageDeliveryTime <= endTime:
            selected_packages.append(myHash.search(packageID))
    return selected_packages

def addDeliveryTimesToPackages(truckNNRoute, TimeMileageList):
    timeNum = 0
    for package_id in truckNNRoute:
        Package.updateDeliveryTime(myHash.search(package_id), TimeMileageList[1][timeNum])
        timeNum = timeNum + 1

addDeliveryTimesToPackages(truck1nnRoute, TimeMileageListsTruck1)
addDeliveryTimesToPackages(truck2nnRoute, TimeMileageListsTruck2)
addDeliveryTimesToPackages(truck3nnRoute, TimeMileageListsTruck3)

def getSinglePackageStatusWithTime(userPackageInput, userTimeInput):
    packageDeliveryTime = time.fromisoformat(myHash.search(userPackageInput).DeliveryTime)
    truck1and3DepartTime = time(8, 0)
    truck2DepartTime = time(9, 15)

    if userPackageInput in packageTruck1_ids or userPackageInput in packageTruck3_ids:
        if userTimeInput < truck1and3DepartTime:
            Package.updateStatus(myHash.search(userPackageInput), "at hub")
        else:
            if packageDeliveryTime > userTimeInput:
                Package.updateStatus(myHash.search(userPackageInput), "en route")
            else:
                Package.updateStatus(myHash.search(userPackageInput), "delivered")
    else:
        if userTimeInput < truck2DepartTime:
            Package.updateStatus(myHash.search(userPackageInput), "at hub")
        else:
            if packageDeliveryTime > userTimeInput:
                Package.updateStatus(myHash.search(userPackageInput), "en route")
            else:
                Package.updateStatus(myHash.search(userPackageInput), "delivered")

    if myHash.search(userPackageInput).Status != "delivered":
        Package.updateDeliveryTime(myHash.search(userPackageInput), "N/A")

    print("----------------------------------------------")
    print("PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
    print(myHash.search(userPackageInput))

def getAllPackageStatusWithTime(userTimeInput):
    print("----------------------------------------------")
    print("PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
    truck1and3DepartTime = time(8, 0)
    truck2DepartTime = time(9, 15)

    for packageID in range(1, 41):
        packageDeliveryTime = time.fromisoformat(myHash.search(packageID).DeliveryTime)
        if packageID in packageTruck1_ids or packageID in packageTruck3_ids:
            if userTimeInput < truck1and3DepartTime:
                Package.updateStatus(myHash.search(packageID), "at hub")
            else:
                if packageDeliveryTime > userTimeInput:
                    Package.updateStatus(myHash.search(packageID), "en route")
                else:
                    Package.updateStatus(myHash.search(packageID), "delivered")
        else:
            if userTimeInput < truck2DepartTime:
                Package.updateStatus(myHash.search(packageID), "at hub")
            else:
                if packageDeliveryTime > userTimeInput:
                    Package.updateStatus(myHash.search(packageID), "en route")
                else:
                    Package.updateStatus(myHash.search(packageID), "delivered")

        if myHash.search(packageID).Status != "delivered":
            Package.updateDeliveryTime(myHash.search(packageID), "N/A")

        print(myHash.search(packageID))
# --------------------------------------- Menu Methods ---------------------------------------

def getTimeAndMileage(truckNNRoute):
    totalMileage = 0
    truckLocation = 0
    mileageList = []
    for i in truckNNRoute:
        totalMileage = totalMileage + getDistance(truckLocation, getAddressIDFromPackageID(i))
        mileageList.append(totalMileage)
        truckLocation = getAddressIDFromPackageID(i)

    if truckNNRoute == truck2nnRoute:
        startTime = (9 * 60) + 15
    else:
        startTime = 8 * 60
    lastTravelDistance = 0
    travelTimeMinutes = []
    deliveryTimeList = []
    for i in mileageList:
        travelTimeMinutes.append(round((i - lastTravelDistance) / 0.3))
        lastTravelDistance = i
    for i in travelTimeMinutes:
        startTime += i
        hours, minutes = divmod(startTime, 60)
        deliveryTimeList.append(f"{hours:02d}:{minutes:02d}")
    return mileageList, deliveryTimeList

TimeMileageListsTruck1 = getTimeAndMileage(truck1nnRoute)
TimeMileageListsTruck2 = getTimeAndMileage(truck2nnRoute)
TimeMileageListsTruck3 = getTimeAndMileage(truck3nnRoute)

def totalMileageCalculation():
    truck3ReturnTrip = getDistance(12, 0)
    totalMileage = TimeMileageListsTruck1[0][-1] + TimeMileageListsTruck2[0][-1] + truck3ReturnTrip + TimeMileageListsTruck3[0][-1]
    truck1Mileage = TimeMileageListsTruck1[0][-1]
    truck2Mileage = TimeMileageListsTruck2[0][-1]
    truck3Mileage = TimeMileageListsTruck3[0][-1] + truck3ReturnTrip
    return totalMileage, truck1Mileage, truck2Mileage, truck3Mileage

# Define the selectPackagesBetweenTime function
def selectPackagesBetweenTime(startTime, endTime):
    selected_packages = []
    for packageID in range(1, 41):
        packageDeliveryTime = time.fromisoformat(myHash.search(packageID).DeliveryTime)
        if startTime <= packageDeliveryTime <= endTime:
            selected_packages.append(myHash.search(packageID))
    return selected_packages

def addDeliveryTimesToPackages(truckNNRoute, TimeMileageList):
    timeNum = 0
    for package_id in truckNNRoute:
        Package.updateDeliveryTime(myHash.search(package_id), TimeMileageList[1][timeNum])
        timeNum = timeNum + 1

addDeliveryTimesToPackages(truck1nnRoute, TimeMileageListsTruck1)
addDeliveryTimesToPackages(truck2nnRoute, TimeMileageListsTruck2)
addDeliveryTimesToPackages(truck3nnRoute, TimeMileageListsTruck3)

def getSinglePackageStatusWithTime(userPackageInput, userTimeInput):
    packageDeliveryTime = time.fromisoformat(myHash.search(userPackageInput).DeliveryTime)
    truck1and3DepartTime = time(8, 0)  # time truck 1 and 3 will depart the hub
    truck2DepartTime = time(9, 15)  # time truck 2 will depart the hub


    # Update nearest neighbor logic for package 9
    if userPackageInput == 9 and userTimeInput >= time(10, 20):
        Package.updateAddress(myHash.search(9), "410 S State St")


    # Change the package status depending on which trucks it's associated with and the time the user passed in
    if userPackageInput in packageTruck1_ids or userPackageInput in packageTruck3_ids:
        if userTimeInput < truck1and3DepartTime:
            Package.updateStatus(myHash.search(userPackageInput), "at hub")
        else:
            if packageDeliveryTime > userTimeInput:
                Package.updateStatus(myHash.search(userPackageInput), "en route")
            else:
                Package.updateStatus(myHash.search(userPackageInput), "delivered")
    else:
        if userTimeInput < truck2DepartTime:
            Package.updateStatus(myHash.search(userPackageInput), "at hub")
        else:
            if packageDeliveryTime > userTimeInput:
                Package.updateStatus(myHash.search(userPackageInput), "en route")
            else:
                Package.updateStatus(myHash.search(userPackageInput), "delivered")


    # If the package does not have a delivered status, display the delivery time as N/A
    if myHash.search(userPackageInput).Status != "delivered":
        Package.updateDeliveryTime(myHash.search(userPackageInput), "N/A")


    print("----------------------------------------------")
    print("PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
    print(myHash.search(userPackageInput))  # print the package

def getAllPackageStatusWithTime(userTimeInput):
    print("----------------------------------------------")
    print("PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
    truck1and3DepartTime = time(8, 0)
    truck2DepartTime = time(9, 15)

    for packageID in range(1, 41):
        packageDeliveryTime = time.fromisoformat(myHash.search(packageID).DeliveryTime)
        if packageID in packageTruck1_ids or packageID in packageTruck3_ids:
            if userTimeInput < truck1and3DepartTime:
                Package.updateStatus(myHash.search(packageID), "at hub")
            else:
                if packageDeliveryTime > userTimeInput:
                    Package.updateStatus(myHash.search(packageID), "en route")
                else:
                    Package.updateStatus(myHash.search(packageID), "delivered")
        else:
            if userTimeInput < truck2DepartTime:
                Package.updateStatus(myHash.search(packageID), "at hub")
            else:
                if packageDeliveryTime > userTimeInput:
                    Package.updateStatus(myHash.search(packageID), "en route")
                else:
                    Package.updateStatus(myHash.search(packageID), "delivered")

        if myHash.search(packageID).Status != "delivered":
            Package.updateDeliveryTime(myHash.search(packageID), "N/A")

        print(myHash.search(packageID))
#--------------------------------------- Menu ---------------------------------------

def menu():
    print("----------------------------------------------")
    print("Hello & Welcome to the CLI terminal for WGU C950 Task 2 of Data Structures Data Algorithms")
    print("----------------------------------------------")
    print("Main Menu, please type an option 1, 2, 3, 4, or 5")
    print("----------------------------------------------")
    print("1. Print All Package Status and Total Mileage")
    print("2. Get a Single Package Status with a Time")
    print("3. Get All Package Status Within a Start & End Time")
    print("4. View All 3 Trucks Status and Mileage")
    print("5. Exit the Program")
    menuOptionSelect = input("Selection(1-5): ")
    if menuOptionSelect == "1":
        option1()
    elif menuOptionSelect == "2":
        option2()
    elif menuOptionSelect == "3":
        option3()
    elif menuOptionSelect == "4":
        option4()
    else:
        option5()

def option1():
    print("----------------------------------------------")
    print("Printing All Package Status and Total Mileage...")
    print("----------------------------------------------")
    getAllPackageStatusWithTime(time(12, 0))
    totalMileage = totalMileageCalculation()[0]
    print("----------------------------------------------")
    print(f"Total mileage traveled: {totalMileage} miles")
    print("----------------------------------------------")
    return_to_menu()

def option2():
    print("----------------------------------------------")
    try:
        userPackageInput = int(input("Enter Package ID: "))
        userTimeInput = input("Enter Time (HH:MM): ")
        if ':' not in userTimeInput:
            raise ValueError("Invalid time format. Please enter the time in HH:MM format.")
        userTime = time.fromisoformat(userTimeInput + ':00')
        getSinglePackageStatusWithTime(userPackageInput, userTime)
    except ValueError as e:
        print(str(e))
    print("----------------------------------------------")
    return_to_menu()

def option3():
    print("----------------------------------------------")
    try:
        userStartTimeInput = input("Enter Start Time (HH:MM): ")
        userEndTimeInput = input("Enter End Time (HH:MM): ")

        if ':' not in userStartTimeInput or ':' not in userEndTimeInput:
            raise ValueError("Invalid time format. Please enter the time in HH:MM format.")

        startTime = time.fromisoformat(userStartTimeInput + ':00')
        endTime = time.fromisoformat(userEndTimeInput + ':00')

        if startTime >= endTime:
            raise ValueError("End time must be later than start time.")

        selected_packages = selectPackagesBetweenTime(startTime, endTime)

        print("----------------------------------------------")
        print("Selected packages between", startTime.strftime('%H:%M'), "and", endTime.strftime('%H:%M') + ":")
        print("----------------------------------------------")
        print("PackageID, Address, City, State, Zip, Delivery Deadline, Mass KILO, PageSpecial Notes, Status, DeliveryTime")
        for package in selected_packages:
            print(package)
    except ValueError as e:
        print(str(e))
    print("----------------------------------------------")
    return_to_menu()
def option4():
    print("----------------------------------------------")
    print("Truck 1 travelled " + str(round(totalMileageCalculation()[1], 1)) + " miles.")
    print("Truck 2 travelled " + str(round(totalMileageCalculation()[2], 1)) + " miles.")
    print("Truck 3 travelled " + str(round(totalMileageCalculation()[3], 1)) + " miles.")
    print("The total distance travelled to deliver all the packages is " + str(round(totalMileageCalculation()[0], 1)) + " miles.")
    print("----------------------------------------------")
    return_to_menu()

def option5():
    print("Exiting the Program...")
    exit()

def return_to_menu():
    print("Do you want to return to the main menu? (Y/N)")
    choice = input().strip().upper()
    if choice == 'Y':
        menu()
    elif choice == 'N':
        option5()
    else:
        print("Invalid choice. Please enter Y or N.")
        return_to_menu()

menu()