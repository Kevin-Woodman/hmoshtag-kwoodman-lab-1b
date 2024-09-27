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

def main():
    studentArray = []
    with open("./students.txt") as studentFile:
        lines = studentFile.readlines()
        studentArray = [list(map(lambda string : string.replace("\n",""),line.split(","))) for line in lines]


    print(infoString)
    while(True):
        selection = input().split(" ")
        match selection[0]:
            case "Q" | "Quit":  exit(0)
            case "S" | "Student" : pass
            case _: print(selection, "Invalid input")

if __name__ == "__main__":
    main()


