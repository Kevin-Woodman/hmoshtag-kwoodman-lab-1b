import numpy as np
import os

infoString = """ Usage: 
    S[tudent]: <lastname> [B[us]] 
    T[eacher]: <lastname> 
    B[us]: <number> 
    G[rade]: <number> [H[igh]|L[ow]]
    A[verage]: <number>
    I[nfo]
    Q[uit]"""


def searchByTeacher(selection, studentArray):
    if(len(selection) != 2): 
        print("Invalid usage")
        return

    for student in studentArray: 
        if(student[6] == selection[1]): print(student[0],student[1])
    

def main():
    studentArray = []

    if(not os.path.isfile("./students.txt")): 
        print("students.txt not found")
        exit(0)

    with open("./students.txt") as studentFile:
        lines = studentFile.readlines()
        studentArray = [list(map(lambda string : string.replace("\n",""),line.split(","))) for line in lines]


    print(infoString)
    while(True):
        selection = input().split(" ")
        print("-----")
        match selection[0]:
            case "Q" | "Quit":  exit(0)
            case "S" | "Student" : pass
            case "T" | "Teacher" : searchByTeacher(selection,studentArray)
            case _: print(selection, "Invalid input")
        print("")
if __name__ == "__main__":
    main()


