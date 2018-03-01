"""
    var R: number of rows of the grid (1≤R≤10000)
    var C: number of columns of the grid (1 ≤ C ≤ 10000)
    var F: number of vehicles in the fleet (1 ≤ F ≤ 1000)
    var N: number of rides (1≤N ≤10000)
    var B: per-ride bonus for starting the ride on time (1 ≤ B ≤ 10000)
    var T: number of steps in the simulation (1 ≤ T ≤ 10^9)
"""

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

        self.distance = distance(a, x, b, y)
        # latest time at which you can leave and still arrive in time (You'll lose the bonus by starting then)
        self.s_latest = self.f - self.distance - 1


class Car(object):
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.rides = []
        self.availability = [True for _ in range(T)]

    def is_free_at(self, timestep):
        """
        checks if the car is free at timestep
        :param timestep: an int used as an index in self.availability
        :return:
        """
        return self.availability[timestep]

    def is_free_for(self, ride):
        """
        Checks if the car can complete a ride, and if it will get the bonus
        :param ride: a Ride object
        :return: bool, bool: [can_make_ride, can_get_bonus]
        """
        dist_traveled = 0
        # for every timestep in which you can complete the ride, try to go for a continuous ride.distance amount
        for i in range(ride.s, ride.f):
            if self.is_free_at(i):
                dist_traveled += 1
            else:
                dist_traveled = 0
            if dist_traveled == ride.distance:
                return True, i == ride.s + ride.distance
        return False, False

    def book_earliest_ride(self, ride):
        """
        Changes self.availability to reflect the booking of the earliest possible slot for :param ride:
        :return: Nothing
        """
        if ride not in self.rides:
            dist_traveled = 0
            start = ride.s
            if self.is_free_for(ride)[0]:
                for i in range(ride.s, ride.f):
                    if self.is_free_at(i):
                        dist_traveled += 1
                    else:
                        dist_traveled = 0
                        start = i
                    if dist_traveled == ride.distance:
                        for j in range(start, start + ride.distance):
                            self.availability[j] = False
                            self.rides.append(ride)


def just_do_it():
    curr_time = 0
    for ride in rides:
        cars_with_bonus = []
        for car in [car for car in cars if car.is_free_for(ride)[0]]:  # all the cars that are free for that ride
            # if can also get the bonus
            if curr_time + distance(car.x, ride.a, car.y, ride.b) < ride.s:
                cars_with_bonus.append(car)
        # todo nothing will happen if there isn't a car that can get the ride with the bonus
        for car in cars_with_bonus:
            # todo if we have time, expand this to prefer assigning a ride to a car from a group of 5 cars over one from a group of 2 cars
            if car.x in [car.x for car in cars_with_bonus] \
                    and car.y in [car.y for car in cars_with_bonus]:
                car.book_earliest_ride(ride)
                break
        cars_with_bonus[0]


def read_file(filename):
    """
    :param filename:
    :var R: number of rows of the grid (1≤R≤10000)
    :var C: number of columns of the grid (1 ≤ C ≤ 10000)
    :var F: number of vehicles in the fleet (1 ≤ F ≤ 1000)
    :var N: number of rides (1≤N ≤10000)
    :var B: per-ride bonus for starting the ride on time (1 ≤ B ≤ 10000)
    :var T: number of steps in the simulation (1 ≤ T ≤ 10^9)
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


def main():
    files = ["Problem/a_example.in",
             "Problem/b_should_be_easy.in",
             "Problem/c_no_hurry.in",
             "Problem/d_metropolis.in",
             "Problem/e_high_bonus.in"]
    read_file(files[0])

    # # For testing all the files
    # for file in files:
    #     read_file(file)



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


if __name__ == '__main__':
    main()
