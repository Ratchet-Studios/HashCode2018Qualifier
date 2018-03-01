def read_file(filename):
    f = open(filename)
    several_variables = map(int, f.readline().strip().split())
    several_more_variables = map(int, f.readline().strip().split())

def main():
    files = ["example.in", "easy.in", "medium.in", "hard.in", ]
    read_file(files[0])


    # # For testing all the files
    # for file in files:
    #     read_file(file)


if __name__ == '__main__':
    main()


"""
BRK: This is the Boyd Branch
"""