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

LASTNAME, FIRSTNAME, GRADE, CLASSROOM, BUS, GPA, TLASTNAME, TFIRSTNAME = [i for i in range(0,8)]


def _searchAndPrint(filter, studentArray, comparisonIndex, outputIndices):
    for student in studentArray: 
        if(student[comparisonIndex] == filter): 
            for index in outputIndices:
                print(student[index], end=" ")
            print()    

def searchByTeacher(selection, studentArray):
    if(len(selection) != 2): 
        print("Invalid usage: ", selection)
        return

    _searchAndPrint(selection[1],studentArray, TLASTNAME, [LASTNAME,FIRSTNAME])

def searchByBus(selection, studentArray):
    if(len(selection) != 2): 
        print("Invalid usage: ", selection)
        return

    _searchAndPrint(selection[1],studentArray, BUS, [LASTNAME,FIRSTNAME])

def searchByStudent(selection, studentArray):
    if(len(selection) == 2):
        _searchAndPrint(selection[1], studentArray, LASTNAME, [LASTNAME,FIRSTNAME, GRADE,
                                                                CLASSROOM, TLASTNAME, TFIRSTNAME])
    elif (len(selection) == 3 and (selection[2] == "B" or selection[2] == "Bus")):
        _searchAndPrint(selection[1], studentArray, LASTNAME, [LASTNAME, FIRSTNAME, BUS])
    else: 
        print("Invalid usage: ", selection)

def average(selection, studentArray):
    if(len(selection) != 2): 
        print("Invalid usage: ", selection)
        return

    total, count = [0,0]
    for student in studentArray:
        if(student[GRADE] == selection[1]): 
            try:
                total += float(student[GPA])
            except ValueError: 
                 print(student[LASTNAME], student[GPA], "NAN, students.txt improperly formatted")
                 return
            count += 1

    if count == 0: return
    print(f"{selection[1]} %.2f"%(total/count))

def searchByGrade(selection, studentArray):
    if len(selection) == 2:  # Normal search by grade
        _searchAndPrint(selection[1], studentArray, GRADE, [LASTNAME, FIRSTNAME])
    
    elif len(selection) == 3:  # Search for highest or lowest GPA in a given grade
        grade = selection[1]
        grade_students = [student for student in studentArray if student[GRADE] == grade] # Gets all the students within a given grade

        if not grade_students:
            return

        if selection[2] == 'H' or selection[2] == "High": 
            max_gpa = max(float(student[GPA]) for student in grade_students)
            
            # Get all students with the maximum GPA
            highest_gpa_students = [student for student in grade_students if float(student[GPA]) == max_gpa]

            # Print all students with the highest GPA (addresses ties)
            for student in highest_gpa_students:
                print(f"{student[LASTNAME]} {student[FIRSTNAME]} {student[GPA]} {student[TLASTNAME]} {student[TFIRSTNAME]} {student[BUS]}")
        
        elif selection[2] == 'L' or selection[2] == "Low": 
            min_gpa = min(float(student[GPA]) for student in grade_students)
            
            # Get all students with the minimum GPA
            lowest_gpa_students = [student for student in grade_students if float(student[GPA]) == min_gpa]
            
            # Print all students with the lowest GPA (addresses ties)
            for student in lowest_gpa_students:
                print(f"{student[LASTNAME]} {student[FIRSTNAME]} {student[GPA]} {student[TLASTNAME]} {student[TFIRSTNAME]} {student[BUS]}")
        else:
            print("Invalid usage: must specify 'H'/'High' for highest or 'L'/'Low' for lowest.")
    else:
        print("Invalid usage: ", selection)

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
        selection = input().split()
        match selection[0]:
            case "Q" | "Quit":  exit(0)
            case "S:" | "Student:" : searchByStudent(selection, studentArray)
            case "T:" | "Teacher:" : searchByTeacher(selection, studentArray)
            case "B:" | "Bus:" : searchByBus(selection, studentArray)
            case "A:" | "Average:" : average(selection,studentArray)
            case "G:"  | "Grade:" : searchByGrade(selection,studentArray)
            case _: print(selection, "Invalid input")
        print("")
if __name__ == "__main__":
    main()


