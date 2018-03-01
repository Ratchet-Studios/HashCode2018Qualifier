import math


def distance(x0, x1, y0, y1):
    return math.fabs(x0 - x1) + math.fabs(y0 - y1)


class Ride(object):
    def __init__(self, a, b, x, y, s, f, id):
        """
        :param a: the row of the start intersection (0 ≤ a < R)
        :param b: the column of the start intersection (0 ≤ b < C )
        :param x: the row of the finish intersection (0 ≤ x < R)
        :param y: the column of the finish intersection (0 ≤ y < C )
        :param s: the earliest start (0 ≤ s < T)
        :param f: the latest finish (0 ≤ f ≤ T), (f ≥ s + |x − a| + |y − b|)
            ○ note that f can be equal to T – this makes the latest finish equal to the end of the simulation
        :return:
        """
        self.a = a
        self.b = b
        self.x = x
        self.y = y
        self.s = s
        self.f = f

        self.id = id

        self.distance = distance(a, x, b, y)
        self.s_latest = self.f - self.distance - 1  # latest time at which you can leave and still arrive in time


class Car(object):
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id



def read_file(filename):
    """
    :param filename:
    :var R: number of rows of the grid (1≤R≤10000)
    :var C: number of columns of the grid (1 ≤ C ≤ 10000)
    :var F: number of vehicles in the fleet (1 ≤ F ≤ 1000)
    :var N: number of rides (1≤N ≤10000)
    :var B: per-ride bonus for starting the ride on time (1 ≤ B ≤ 10000)
    :var T: number of steps in the simulation (1 ≤ T ≤ 109)
    :return: Nothing
    """

    f = open(filename)
    global R, C, F, N, B, T
    R, C, F, N, B, T = map(int, f.readline().strip().split())
    global rides
    rides = []  # sorted with earliest start times first
    for i in range(N):
        # ugly but it works
        arr = list(map(int, f.readline().strip().split()))
        rides.append(Ride(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], i))
    rides.sort(key=lambda ride: ride.s)  # sort rides with earliest start time first

    cars = []
    for i in range(F):
        cars.append(Car(0, 0, i))
    f.close()


def main():
    files = ["Problem/a_example.in",
             "Problem/b_should_be_easy.in",
             "Problem/c_no_hurry.in",
             "Problem/d_metropolis.in",
             "Problem/e_high_bonus.in"]
    read_file(files[0])
    
    create_graph()
    
    for i in range(0, F):
        print('Car ' + str(i))
        dijkstra_for_one_car()

    print('oi')
    # # For testing all the files
    # for file in files:
    #     read_file(file)
    
    

class Node(object):
    def __init__(self, ride, start_time, score):
        self.score = score
        self.ride = ride
        self.start_time = start_time
        self.children = [] #  All the places you can go from here!
        
        self.visited = False


def create_graph():
    global nodes
    nodes = {}  # nodes[(ride, start_time)] is the score that we gain from visiting this node
    # -1 means we mustn't do this ride
    
    # add root node
    blank_ride = Ride(0, 0, 0, 0, 0, 0, 0)
    
    ride_index = 0
    start = 0
    score = 0
    
    # while score == 0:
    #     start, score = ride_start_and_score(rides[ride_index], blank_ride, 0)
    #     ride_index += 1
    
    for ride_index, ride in enumerate(rides):
        start, score = ride_start_and_score(ride, blank_ride, 0)
        if score == 0:
            continue  # We don't care about dem nodes if they don't give us no points!
        
        if nodes.get((ride, start), 0) == 0:  # Don't replace the node if it already exists
            node = Node(ride, start, score)
            nodes[(ride, start)] = node
            connect_to_other_nodes_after_ride_index(node, ride_index)


def connect_to_other_nodes_after_ride_index(node, ride_index):
    for ride_index in range(ride_index + 1, len(rides)):
        start, score = ride_start_and_score(rides[ride_index], node.ride, node.start_time)

        child = nodes.get((rides[ride_index], start), 0)
        
        if child == 0:
            child = Node(rides[ride_index], start, score)
            nodes[(rides[ride_index], start)] = child
        
        node.children.append(child)
        connect_to_other_nodes_after_ride_index(child, ride_index)
        
    
    
    
    # delete all the useless rides
    # for i in range(ride_index - 1, -1, -1):
    #     del rides[i]
    
    
def dijkstra_for_one_car():
    
    score = 0
    
    current_node = 0
    max = 0
    
    for key, node in nodes.items():
        if not node.visited and node.score > max:
            current_node = node
            max = current_node.score

    score += current_node.score
    current_node.visited = True
    print(current_node.ride.id)
    
    max_child_node = 0
    max = 0
    
    for child in current_node.children:
        if not child.visited and child.score > max:
            max_child_node = child
            max = max_child_node.score
    
    if max_child_node == 0:
        return
    
    
    score += max_child_node.score
    max_child_node.visited = True
    
    current_node = max_child_node

    print(current_node.ride.id)
    
    
    
    
    
def ride_start_and_score(ride, previous_ride, previous_start_time):  # ask stu to explain it
    score = ride.distance
    
    distance_between_rides = distance(ride.a, previous_ride.x, ride.b, previous_ride.y)
    
    previous_end_time = previous_start_time + previous_ride.distance
    arrival_time_at_new_ride = previous_end_time + distance_between_rides
    
    start_time = max(ride.s, arrival_time_at_new_ride)
    if start_time > ride.s_latest:
        return start_time, 0  # we won't arrive on time so we won't get no points :(
    
    if start_time <= ride.s:
        score += B
    
    return start_time, score
    
    
def rewrite_line(nums):
    line = str(len(nums) - 2)
    for num in nums:
        line += ' ' + num
    return line
    


def is_valid_file(submission_array):
    """submission_array is of the form ['vehicle1 ride1 ride2... rideN',...,'vehicleN ride1... rideN']"""
    assigned_rides = []
    if len(submission_array) != F:
        return 0
    for i in range(F):
        if len(submission_array[i]) < 3:
            submission_array[i] = i + ' 0'
        else:
            nums = submission_array.split()
            for x in range(2, len(nums)):
                if x in assigned_rides:
                    submission_array[i] = i + ' ' + rewrite_line(nums)
                    break
                assigned_rides.append(x)

def write_output(data):
    """
    :param data: a list of space-deliminated arrays: ["{M} {R0} {R1} {R2} etc", "{M} {R0} {R1} {R2} etc", etc]
        ● M:
            number of rides assigned to the vehicle (0 ≤ M ≤ N)
        ● R0, R1, ..., RM-1:
            ride numbers assigned to the vehicle, in the order in which the vehicle will performthem (0≤Ri <N)
    :return: nothing
    """
    output_file = open("output.txt", "w+")
    output = ""
    for item in data:
        output += item + "\n"
    output_file.write(output)
    output_file.close()
    #test

if __name__ == '__main__':
    main()
