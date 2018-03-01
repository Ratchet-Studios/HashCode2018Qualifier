Rows, Columns, num_vehicles, num_rides, ride_bonus, num_steps = 0,0,0,0,0,0
def read_file(filename):
    f = open(filename)
    # take the first line, strip extra whitespace, convert to an array by spaces, convert each element to an int
    global Rows, Columns, num_vehicles, num_rides, ride_bonus, num_steps = map(int, f.readline().strip().split())
    var4, var5, var6, etc = map(int, f.readline().strip().split())


def main():
    files = ["example.in", "easy.in", "medium.in", "hard.in", ]
    read_file(files[0])


    # # For testing all the files
    # for file in files:
    #     read_file(file)




def is_valid_file(submission_array):
    if len(submission_array) != num_rides:
        return 0

if __name__ == '__main__':
    main()
