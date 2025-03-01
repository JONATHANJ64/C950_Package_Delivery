class Package: # package class
    # Space-Time Complexities are O(1)
    def __init__(self, PackageID, Address, City, State, Zip, DeliveryDeadline, Mass, Notes, Status, DeliveryTime):
        self.PackageID = PackageID # a unique identifier for the package
        self.Address = Address # the street address where the package is to be delivered
        self.City = City # the city where the package is to be delivered
        self.State = State # the state where the package is to be delivered
        self.Zip = Zip # the zip code where the package is to be delivered
        self.DeliveryDeadline = DeliveryDeadline # the time by which the package must be delivered
        self.Mass = Mass # the weight of the package
        self.Notes = Notes # any additional notes about the package
        self.Status = Status # the current status of the package
        self.DeliveryTime = DeliveryTime # the time when the package was delivered

    # Space-Time Complexities is O(1)
    # updates the status

    def updateStatus(self, newStatus):
        self.Status = newStatus

    # Space-Time Complexities is O(1)
    # updates the delivery

    def updateDeliveryTime(self, newDeliveryTime):
        self.DeliveryTime = newDeliveryTime

    # Space-Time Complexities are O(1)
    # updates the address

    def updateAddress(self, newAddress):
        self.Address = newAddress

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (
            self.PackageID, self.Address, self.City, self.State, self.Zip, self.DeliveryDeadline, self.Mass, self.Notes, self.Status, self.DeliveryTime)
