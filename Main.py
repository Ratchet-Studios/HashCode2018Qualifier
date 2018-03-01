def read_file(filename):
    f = open(filename)
    # take the first line, strip extra whitespace, convert to an array by spaces, convert each element to an int
    var1, var2, var3, etc = map(int, f.readline().strip().split())
    var4, var5, var6, etc = map(int, f.readline().strip().split())


def main():
    files = ["example.in", "easy.in", "medium.in", "hard.in", ]
    read_file(files[0])


    # # For testing all the files
    # for file in files:
    #     read_file(file)


if __name__ == '__main__':
    main()
