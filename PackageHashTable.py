# Milan Macura #000989289

from datetime import time, datetime, timedelta

from Graph import Graph
from Package import Package
from Truck import Truck
from Vertex import Vertex


class PackageHashTable:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.hash_table = []
        for i in range(capacity):
            self.hash_table.append([])

    # Add a value to the hashtable
    def add(self, value):
        bucket = self.package_hash(value.package_id)
        self.hash_table[bucket].append(value)

    # Remove value from the hashtable
    def remove(self, value):
        bucket = self.package_hash(value.package_id)
        if value in self.hash_table[bucket]:
            self.hash_table[bucket].remove(value)

    # Search for a hash value and return it
    def search(self, value):
        bucket = self.package_hash(value.package_id)
        bucket_list = self.hash_table[bucket]
        # if the value is found in the bucket list
        if value in bucket_list:
            index = bucket_list.index(value)
            return bucket_list[index]
        else:
            return None

    # Returns the package data of the searched hash value by id
    def search_id(self, value):
        bucket = self.package_hash(value)
        bucket_list = self.hash_table[bucket]
        for i in range(0, len(bucket_list)):
            if bucket_list[i].package_id == value:
                return bucket_list[i]
        return False

    # Removes everything in the hash table
    def clear(self):
        self.hash_table.clear()
        self.__init__()

    def package_hash(self, value):
        return value % 10

    # Big O Notation for this code block:  O(n)
    # Returns the total of packages in the hash table
    def count(self):
        c = 0
        for i in range(0, len(self.hash_table)):
            c += len(self.hash_table[i])
        return c

    # Big O Notation for this code block:  O(n^2)
    # Returns the number of delivered packages in the hash table
    def count_delivered(self):
        c = 0
        for i in range(0, len(self.hash_table)):
            for j in range(0, len(self.hash_table[i])):
                if self.hash_table[i][j].delivered == "Delivered":
                    c += 1
        return c

# Big O Notation for this code block:  O(n^3)
# Converts the csv files into usable data and adds it to the hash table
def init_packages(package_master):
    ph_table.clear()
    for i in range(1, len(list(package_master)) + 1):
        p = package_master[str(i)]
        if p[4] == 'EOD':
            p = list(package_master[str(i)])
            ph_table.add(Package(i, p[0], p[1], p[2], p[3], p[4], p[5], p[6]))
        else:
            t_str = p[4].split(":")
            if t_str[1].__contains__("AM"):
                h = int(t_str[0])
            else:
                h = int(t_str[0]) + 12
            m = int(t_str[1][0:2])
            del_time = datetime(2020, 1, 1, h, m, 0)
            ph_table.add(Package(i, p[0], p[1], p[2], p[3], del_time.strftime("%X"), p[5], p[6]))


# Big O Notation for this code block:  O(n^3)
# Populate the hub
def pop_hub(time):
    for i in range(1, ph_table.count() + 1):
        if ph_table.search_id(i):
            pack = ph_table.search_id(i)
            if "Delivered" not in pack.delivered and pack not in packs_at_hub:
                if ":" not in pack.notes:
                    packs_at_hub.append(pack)
                else:
                    to_str = pack.notes.split(':')
                    h = int(to_str[0][-2:])
                    m = int(to_str[1][0:2])
                    if "pm" in to_str[1][0:].lower():
                        h += 12
                    t = datetime(2020, 1, 1, h, m)
                    if time_is_before(t, time):
                        packs_at_hub.append(pack)

# Big O notation for this block of code O(1)
# Checks if the arrival time is before or after the current time
def time_is_before(arrival_time, current_time):
    h = current_time.hour - arrival_time.hour
    m = (current_time.minute - arrival_time.minute) / 60
    s = (current_time.second - arrival_time.second) / 360
    # if the arrival time is after the current time
    if (h + m + s) < 0:
        return False
    else:  # arrival time is before the current time
        return True

# Open the distance and the package file
distances_file = open("WGUPS Distance Table.csv", "rt")
packages_file = open("WGUPS Package File.csv", "rt")

# Create a pointer method for the graph
graph_distance = Graph()

# Create a pointer for the package hash table
ph_table = PackageHashTable()

# Initialize variables
package_master = {}
pm = []
vertex_array = []
global_time = datetime(2020, 1, 1, 8, 0, 0)

# Create 2 trucks to move the packages
truck1 = Truck('truck 1', 'HUB')
truck2 = Truck('truck 2', 'HUB')

# Big O Notation for this code block:  O(n)
# fill the vertex array
for line in distances_file:
    distance_array = line.split(",")
    key = Vertex(distance_array[1])
    distance_array.pop(0)
    distance_array.pop(0)
    vertex_array.append((key, distance_array))
    graph_distance.adjacency_list[key] = distance_array

# Big O Notation for this code block: O(N^2
# for int i in the length of vertext array
for i in range(0, len(vertex_array)):
    # create edge list
    edge_list = list((vertex_array[i])[1:len(vertex_array)][0])
    # for loop with the length of edge list
    for j in range(0, len(edge_list)):
        if edge_list[j] == "" or edge_list[j] == "/n" or edge_list[j] == "\n":
            break
        else:
            x = list(vertex_array[i])[0]
            y = list(vertex_array[j])[0]
            z = edge_list[j]
            # add undirected edge to the graph
            graph_distance.add_undirected_edge(list(vertex_array[i])[0], list(vertex_array[j])[0], float(edge_list[j]))

# Big O Notation for this code block:  O(n)
for line in packages_file:
    package = line.split(",")
    package_master[package[0]] = package[1:len(package)]
    pm.append((int(package[0]), package[1:len(package)]))

menu = -1

# Initialize the packages
init_packages(package_master)
# Output amount it packages in the hash table
print("Total Packages To Deliver: %s" % ph_table.count())


# PSEUDOCODE FOR THE WGUPS DELIVERY PROGRAM
# Open the distance file and the package file
# Convert data from the package file into hashtable and distance file into vertex array
# Create 2 trucks
# Fill trucks with packages from hub
# Find closest location between current location to destination
# Deliver package when reaching destination
# Set package to delivered so it will be ignored by the algorithm
# Repeat until all packages are delivered
# Ask user to input time to show packages for that time period


# Big O Notation for this code block: O(N^7)
while int(menu) < 0:

    menu = '3'
    if menu == '1':

        menu = -1
    elif menu == '2':
        pass
    elif menu == '3':
        # Variable for packages at hub
        packs_at_hub = []
        # While not all the packages are not delivered
        while ph_table.count_delivered() < ph_table.count():
            # Populate the hub
            pop_hub(global_time)
            # Fill truck 1 and 2 with the packages from the hub
            truck1.fill(packs_at_hub)
            truck2.fill(packs_at_hub)

            # Check if truck 1's time is before truck 2's time
            if time_is_before(truck1.current_time, truck2.current_time):
                # store truck 2's current time into global time
                global_time = truck2.current_time
            else:
                # store truck 1's current time into global time
                global_time = truck1.current_time

            # Print the output counts
            print("Delivered Count: %s" % ph_table.count_delivered())
            print("Table Count: %s" % ph_table.count())

            for i in range(1, ph_table.count() + 1):
                if ph_table.search_id(i).delivery_time is not None:
                    print(str(ph_table.search_id(i).package_id) + " Deadline: " + ph_table.search_id(
                        i).deadline + " Delivery Time: " + ph_table.search_id(i).delivery_time.strftime("%X"))

            print("Truck 1 distance: " + str(truck1.daily_distance) + " Truck 2 distance: " + str(truck2.daily_distance))
            print("Total distance: " + str(truck1.daily_distance + truck2.daily_distance))

        print("\nEnter beginning of time window to check: ")
        # User input to check from start time
        h1 = input("Enter hours [1-12]: ")
        m1 = input("Enter minutes [0-59]: ")
        noon1 = input("Enter AM or PM: ").upper()

        print("\nEnter end of time window to check: ")
        # User input to check to finish time
        h2 = input("Enter hours [1-12]: ")
        m2 = input("Enter minutes [0-59]: ")
        noon2 = input("Enter AM or PM: ").upper()
        pass
    elif menu == '4':
        break
    else:
        menu = -1
