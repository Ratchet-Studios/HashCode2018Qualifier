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
    rides = []
    for i in range(N):
        # ugly but it works
        arr = list(map(int, f.readline().strip().split()))
        rides.append(Ride(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5], i))


def main():
    files = ["a_example.in",
             "b_should_be_easy.in",
             "c_no_hurry.in",
             "d_metropolis.in",
             "e_high_bonus.in"]
    read_file(files[0])


    # # For testing all the files
    # for file in files:
    #     read_file(file)


def is_valid_file(submission_array):
    """submission_array is of the form [[fi"""
    if len(submission_array) != num_rides:
        return 0


if __name__ == '__main__':
    main()
