# Milan Macura #000989289

from datetime import time, datetime, timedelta


class Truck:
    def __init__(self, name, location, speed=18, current_time=datetime(2020, 1, 1, 8, 0, 0), capacity=16):
        # Name of the truck
        self.name = name
        # List of packages in the truck
        self.package_list = {}
        self.current_time = current_time
        # Average speed of the truck (18 mph)
        self.speed = speed
        # Location of the truck
        self.location = location
        # How much the truck can hold
        self.capacity = capacity
        self.daily_distance = 0

    #  Adds a package to the truck
    def add_package(self, package):
        if len(self.package_list.items()) <= self.capacity:
            self.package_list[package.package_id] = package
        else:
            print("Truck has reached it's Max Load")
            return False

    # Set the package to deliver
    def deliver_package(self, package, distance):
        self.update_time(distance)
        self.location = package.address
        self.daily_distance += distance
        package.delivered = "Delivered"
        package.delivery_time = self.current_time

    # Update's the current time of the truck
    def update_time(self, distance):
        self.current_time = self.current_time + timedelta(hours=distance / self.speed)

    # Update the location of the truck
    def update_loc(self, location):
        self.location = location

    def get_closest(self, p):
        # import graph_distance
        from PackageHashTable import graph_distance

        closest = graph_distance.get_distance(self.location, p.address)
        for x in list(self.package_list.values()):
            next_loc = graph_distance.get_distance(self.location, x.address)
            if closest > next_loc > 0 and closest > 0:
                closest = next_loc
        return closest

    # This is a queue system for delivering packages. Packages with specific deadlines are high priority
    # Big O Notation for this code block:  O(n^3)
    def out_for_delivery(self):
        # import graph distance
        from PackageHashTable import graph_distance

        # store package list values into packages
        packages = list(self.package_list.values())
        # delivery_queue list
        delivery_queue = []
        # end of deadline que
        eod_queue = []

        # while there are packages in the package list
        while len(packages) > 0:

            # for each package in packages
            for p in packages:
                # if the package is delivered
                if p.delivered == "Delivered":
                    break
                # set it as the earliest package
                earliest = p
                # for loop for the length of packages
                for i in range(0, len(packages)):
                    # if the deadline of the package is not "End of Deadline"
                    if 'EOD' not in earliest.deadline and 'EOD' not in packages[i].deadline:
                        t1 = earliest.deadline.split(":")
                        t2 = packages[i].deadline.split(":")
                        # if pm is found in the notes of the package
                        if "pm" in earliest.notes.lower():
                            h1 = int(t1[0]) + 12
                        else:
                            h1 = int(t1[0])
                            # if pm is found in the notes of the package
                        if "pm" in packages[i].notes.lower():
                            h2 = int(t2[0]) + 12
                        else:
                            h2 = int(t2[0])

                        from PackageHashTable import time_is_before
                        # if date 2 is before date 1
                        if time_is_before(datetime(2020, 1, 1, h2, int(t2[1])), datetime(2020, 1, 1, h1, int(t1[1]))):
                            earliest = packages[i]
                # if there are no more packages in the delivery queue
                if len(delivery_queue) == 0 or delivery_queue[0].deadline == earliest.deadline:
                    # if end of delivery is not found in the earliest packages's deadline
                    if 'EOD' not in earliest.deadline:
                        # add the earliest package to the delivery queue
                        delivery_queue.append(earliest)
                    else:
                        # add earliest package to the end of delivery queue
                        eod_queue.append(earliest)
                # remove the earliest package
                packages.remove(earliest)
            # while the length of the delivery queue is greater than 1
            while len(delivery_queue) > 0:
                # for each package in the delivery queue
                for d in delivery_queue:
                    # if the packages is delivered
                    if d.delivered == "Delivered":
                        break
                    # set closest to package
                    closest = d
                    # for loop using the length of delivery queue
                    for i in range(0, len(delivery_queue)):
                        d1 = float(graph_distance.get_distance(self.location, delivery_queue[i].address))
                        d2 = float(graph_distance.get_distance(self.location, d.address))
                        if d1 < d2:
                            closest = delivery_queue[i]
                    distance = graph_distance.get_distance(self.location, closest.address)
                    # deliver the package
                    self.deliver_package(closest, distance)
                    # remove the closest package from the queue
                    delivery_queue.remove(closest)
            # while the end of day queue is not empty
            while len(eod_queue) > 0:
                # for each package in the end of delivery queue
                for d in eod_queue:
                    # if it's delivered
                    if d.delivered == "Delivered":
                        break
                    # set closest to the package
                    closest = d
                    # for loop for the length of end of delivery loop
                    for i in range(0, len(eod_queue)):
                        # compare distance between two addresses
                        d1 = float(graph_distance.get_distance(self.location, eod_queue[i].address))
                        d2 = float(graph_distance.get_distance(self.location, d.address))
                        # if distance 1 is closer than distance 2
                        if d1 < d2:
                            closest = eod_queue[i]
                    distance = graph_distance.get_distance(self.location, closest.address)
                    # deliver the package
                    self.deliver_package(closest, distance)
                    # remove the closest from the queue after delivering
                    eod_queue.remove(closest)
        self.package_list.clear()

    # Big O Notation for this code block:  O(n^5)
    # Fills the truck with the packages at hub
    def fill(self, packs_at_hub):
        # for each package at the hub
        for p in packs_at_hub:
            # if the package list of items is less than 6
            if len(self.package_list.items()) < 6:
                # if their deadline is not end of delivery, then add it
                if 'EOD' not in p.deadline:
                    self.add_package(p)
            # if the length of package items are less than the capacity of the truck
            if len(self.package_list.items()) < self.capacity:
                # if the length of a package note is < or = to 2 or if it's name is in th e notes, or theres a :
                if len(p.notes) <= 2 or self.name in p.notes or ":" in p.notes:
                    # if End of delivery is in the deadline
                    if 'EOD' in p.deadline:
                        self.add_package(p)
            else:
                break
        # for each package in the package list values
        for p in self.package_list.values():
            # remove the package
            packs_at_hub.remove(p)
        self.out_for_delivery()
