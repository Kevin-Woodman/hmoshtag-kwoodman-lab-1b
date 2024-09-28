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


def _searchAndPrint(selection, studentArray, selectionLen, comparisonIndex, outputIndices):
    if(len(selection) != selectionLen): 
        print("Invalid usage")
        return

    for student in studentArray: 
        if(student[comparisonIndex] == selection[1]): 
            for index in outputIndices:
                print(student[index], end=" ")
            print()    

def searchByTeacher(selection, studentArray):
    _searchAndPrint(selection,studentArray, 2, 6, [0,1])

def searchByBus(selection, studentArray):
     _searchAndPrint(selection,studentArray, 2, 4, [0,1])

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
            case "B" | "Bus" : searchByBus(selection,studentArray)
            case _: print(selection, "Invalid input")
        print("")
if __name__ == "__main__":
    main()


