import math
import copy


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
    
    def __str__(self):
        return 'ride from [' + str(self.a) + ', ' + str(self.b) + '] to [' + str(self.x) + ', ' + str(
            self.y) + '], earliest start ' + str(self.s) + ', latest finish ' + str(self.f)


class Car(object):
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.rides = []
    
    def to_output(self):
        line = str(len(self.rides))
        for ride in self.rides:
            line += ' ' + str(ride.id)
        return line


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
    rides = []
    for i in range(N):
        # ugly but it works
        arr = list(map(int, f.readline().strip().split()))
        rides.append(Ride(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], i))
    rides.sort(key=lambda ride: ride.distance, reverse=True)  # sort rides with earliest start time first
    
    global cars
    cars = []
    for i in range(F):
        cars.append(Car(0, 0, i))
    f.close()


def luc_alg():
    rides_remaining = copy.deepcopy(rides)
    cnt = 0
    output = []
    for ride in rides:
        cars[cnt].rides.append(ride)
        cnt += 1
        if (cnt == len(cars)):
            cnt = 0
    
    for car in cars:
        output.append(car.to_output())
    write_output(output)


def main():
    files = ["Problem/a_example.in",
             "Problem/b_should_be_easy.in",
             "Problem/c_no_hurry.in",
             "Problem/d_metropolis.in",
             "Problem/e_high_bonus.in"]
    read_file(files[4])
    
    for ride in rides:
        print(ride)
    
    luc_alg()
    
    # # For testing all the files
    # for file in files:
    #     read_file(file)


# def rewrite_line(nums, num_to_remove):
#     line = ''
#     nums.remove(num_to_remove)
#     for num in nums:
#         line += ' ' + num
#     return line
#
#
# def is_valid_file(submission_array):
#     """submission_array is of the form ['vehicle1 ride1 ride2... rideN',...,'vehicleN ride1... rideN']"""
#     assigned_rides = []
#     if len(submission_array) != F:
#         return False
#     for i in range(F):
#         nums = submission_array[i].split()
#         for x in range(1, len(nums)):
#             if nums[x] in assigned_rides:
#                 submission_array[i] = str(i+1) + ' ' + rewrite_line(nums, nums[x])
#                 continue
#             assigned_rides.append(nums[x])
#     return submission_array

def write_output(data):
    """
    :param data: a list of space-deliminated arrays: ["{M} {R0} {R1} {R2} etc", "{M} {R0} {R1} {R2} etc", etc]
        ● M:
            number of rides assigned to the vehicle (0 ≤ M ≤ N)
        ● R0, R1, ..., RM-1:
            ride numbers assigned to the vehicle, in the order in which the vehicle will performthem (0≤Ri <N)
    :return: nothing
    """
    output_file = open("output4.txt", "w+")
    output = ""
    for item in data:
        output += item + "\n"
    output_file.write(output)
    output_file.close()
    # test


if __name__ == '__main__':
    main()
