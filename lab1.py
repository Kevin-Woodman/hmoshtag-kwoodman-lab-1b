import numpy as np
import os


def main():
    studentArray = []
    with open("./students.txt") as studentFile:
        lines = studentFile.readlines()
        studentArray = [list(map(lambda string : string.replace("\n",""),line.split(","))) for line in lines]




if __name__ == "__main__":
    main()


