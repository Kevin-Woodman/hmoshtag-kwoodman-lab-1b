import numpy as np
import os

infoString = """ Usage: 
    S[tudent]: <lastname> [B[us]] 
    T[eacher]: <lastname> 
    B[us]: <number> 
    G[rade]: <number> [H[igh] | L[ow] | T[eachers]]
    A[verage]: <number>
    I[nfo]
    E[nrollment]
    C[lassroom]: <number> [T[eachers]] [S[tudents]]
    GPA: Grade 
    GPA: Teacher 
    GPA: Bus
    Q[uit]\n"""

LASTNAME, FIRSTNAME, GRADE, CLASSROOM, BUS, GPA = [i for i in range(0,6)]
TLASTNAME, TFIRSTNAME, TCLASSROOM = [i for i in range(0,3)]

def _searchAndPrint(filter, studentArray, teacherArray, comparisonIndex, outputIndices, teacher : bool = False):
    for student in studentArray: 
        if(student[comparisonIndex] == filter): 
            for index in outputIndices:
                print(student[index], end=" ")
            if(teacher): _printTeachersByClass(teacherArray, student[CLASSROOM])
            print()    


def _printTeachersByClass(teacherArray, classroom):
    print(" [", end = "")
    for teacher in teacherArray: 
        
        if(teacher[TCLASSROOM] == classroom): 
                print(teacher[TLASTNAME], teacher[TFIRSTNAME], end=", ")
    print("\b\b]", end = "")

def searchByTeacher(selection, studentArray, teacherArray):
    if(len(selection) != 2): 
        print("Invalid usage: ", selection)
        return

    for teacher in teacherArray:
        if(teacher[TLASTNAME] == selection[1]):
             _searchAndPrint(teacher[TCLASSROOM], studentArray, teacherArray, CLASSROOM, [LASTNAME,FIRSTNAME])

def searchByBus(selection, studentArray, teacherArray):
    if(len(selection) != 2): 
        print("Invalid usage: ", selection)
        return

    _searchAndPrint(selection[1],studentArray, teacherArray, BUS, [LASTNAME,FIRSTNAME], False)

def searchByStudent(selection, studentArray, teacherArray):
    if(len(selection) == 2):
        _searchAndPrint(selection[1], studentArray, teacherArray, LASTNAME, [LASTNAME,FIRSTNAME, GRADE, CLASSROOM], True)
    elif (len(selection) == 3 and (selection[2] == "B" or selection[2] == "Bus")):
        _searchAndPrint(selection[1], studentArray,  teacherArray, LASTNAME, [LASTNAME, FIRSTNAME, BUS], False)
    else: 
        print("Invalid usage: ", selection)

def average(selection, studentArray, teacherArray):
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

def searchByGrade(selection, studentArray, teacherArray):
    if len(selection) == 2:  # Normal search by grade
        _searchAndPrint(selection[1], studentArray, teacherArray, GRADE, [LASTNAME, FIRSTNAME], False)
    
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
                print(f"{student[LASTNAME]} {student[FIRSTNAME]} {student[GPA]}", end = "")
                _printTeachersByClass(teacherArray,student[CLASSROOM])
                print(f" {student[BUS]}")
        
        elif selection[2] == 'L' or selection[2] == "Low": 
            min_gpa = min(float(student[GPA]) for student in grade_students)
            
            # Get all students with the minimum GPA
            lowest_gpa_students = [student for student in grade_students if float(student[GPA]) == min_gpa]
            
            # Print all students with the lowest GPA (addresses ties)
            for student in lowest_gpa_students:
                print(f"{student[LASTNAME]} {student[FIRSTNAME]} {student[GPA]}", end = "")
                _printTeachersByClass(teacherArray,student[CLASSROOM])
                print(f" {student[BUS]}")
        elif selection[2] == 'T' or selection[2] == "Teachers":
            teachersByGrade(selection,studentArray, teacherArray)
        else:
            print("Invalid usage: must specify 'H'/'High' for highest or 'L'/'Low' for lowest.")
    else:
        print("Invalid usage: ", selection)

def displayGradeCount(studentArray, teacherArray):
    # loop though the array, use a dict to keep track of students in each grade 

    grade_count = {}

    for student in studentArray:
        grade = student[GRADE]
        if grade in grade_count:
            grade_count[grade] += 1 
        else:
            grade_count[grade] = 1

    for grade in sorted(grade_count.keys()):
        print(f"{grade}: {grade_count[grade]}")

def displayClassroomCount(studentArray, teacherArray):
    class_count = {}

    for student in studentArray:
        classRoom = student[CLASSROOM]
        if classRoom in class_count:
            class_count[classRoom] += 1 
        else:
            class_count[classRoom] = 1

    for classRoom, count in sorted(class_count.items()):
        print(f"{classRoom}: {count}")

def teachersByGrade(selection, studentArray, teacherArray):
    gradeClassrooms = []
    for student in studentArray:
        if(student[GRADE] == selection[1] and student[CLASSROOM] not in gradeClassrooms):
            gradeClassrooms.append(student[CLASSROOM])
            _printTeachersByClass(teacherArray, student[CLASSROOM])
            print()
    
def searchByClassNumber(selection, studentArray, teacherArray):
    if len(selection) < 2:
        print("Invalid usage: must specify a classroom number and 'S' (students) or 'T' (teachers).")
        return

    classroom = selection[1]

    if len(selection) == 3 and (selection[2] == "S" or selection[2] == "Students"):  # list students assigned to the classroom
        students_in_class = [student for student in studentArray if student[CLASSROOM] == classroom]

        for student in students_in_class:
            print(f"{student[LASTNAME]} {student[FIRSTNAME]} ")
    elif len(selection) == 3 and (selection[2] == "T" or selection[2] == "Teachers"):  # list teachers assigned to the classroom
        teachers_in_class = [teacher for teacher in teacherArray if teacher[TCLASSROOM] == classroom]

        for teacher in teachers_in_class:
            print(f"{teacher[TLASTNAME]} {teacher[TFIRSTNAME]}")
    else:
        print("Invalid usage: must specify 'S'/'Students' or 'T'/'Teachers'.")

def gpaByGrade(studentArray):
    grade_gpa = {}
    
    for student in studentArray:
        grade = student[GRADE]
        gpa = float(student[GPA])
        
        if grade not in grade_gpa: # organize the gpas by grade level
            grade_gpa[grade] = []
        grade_gpa[grade].append(gpa)
    
    for grade in sorted(grade_gpa.keys()):
        gpas = grade_gpa[grade]
        avg_gpa = sum(gpas) / len(gpas)
        median_gpa = np.median(gpas)
        print(f"{grade}: Average GPA = {avg_gpa:.2f}, Median GPA = {median_gpa:.2f}")

def gpaByTeacher(studentArray, teacherArray):
    teacher_gpa = {}
    
    for student in studentArray:
        classroom = student[CLASSROOM]
        gpa = float(student[GPA])
        
        for teacher in teacherArray: # organize gpas by teacher
            if teacher[TCLASSROOM] == classroom:
                teacher_name = f"{teacher[TLASTNAME]} {teacher[TFIRSTNAME]}"
                if teacher_name not in teacher_gpa:
                    teacher_gpa[teacher_name] = []
                teacher_gpa[teacher_name].append(gpa)
    
    for teacher, gpas in teacher_gpa.items():
        avg_gpa = sum(gpas) / len(gpas)
        median_gpa = np.median(gpas)
        print(f"{teacher}: Average GPA = {avg_gpa:.2f}, Median GPA = {median_gpa:.2f}")

def gpaByBus(studentArray):
    bus_gpa = {}
    
    for student in studentArray:
        bus = student[BUS]
        gpa = float(student[GPA])
        
        if bus not in bus_gpa: # organize gpas by bus
            bus_gpa[bus] = []
        bus_gpa[bus].append(gpa)
    
    for bus in sorted(bus_gpa.keys()):
        gpas = bus_gpa[bus]
        avg_gpa = sum(gpas) / len(gpas)
        median_gpa = np.median(gpas)
        print(f"{bus}: Average GPA = {avg_gpa:.2f}, Median GPA = {median_gpa:.2f}")

def main():
    studentArray = []
    teacherArray = []

    for fileName in ["list","teachers"]:
        if(not os.path.isfile(f"./{fileName}.txt")): 
            print(f"{fileName}.txt not found")
            exit(0)

    with open("./teachers.txt") as teacherFile:
        lines = teacherFile.readlines()
        for line in lines:
            teacher = list(map(lambda string : string.replace("\n",""),line.split(",")))

            if(len(teacher) != 3):
                print("Malformatted teacher file")
                exit(0)

            teacherArray.append(teacher)

    with open("./list.txt") as studentFile:
        lines = studentFile.readlines()
        for line in lines:
            student = list(map(lambda string : string.replace("\n",""),line.split(",")))

            if(len(student) != 6):
                print("Malformatted student file")
                exit(0)

            studentArray.append(student)

    print(infoString)
    while(True):
        selection = input("Enter your command~ ").split()
        match selection[0]:
            case "Q" | "Quit":  exit(0)
            case "S:" | "Student:" : searchByStudent(selection, studentArray, teacherArray)
            case "T:" | "Teacher:" : searchByTeacher(selection, studentArray, teacherArray)
            case "B:" | "Bus:" : searchByBus(selection, studentArray, teacherArray)
            case "A:" | "Average:" : average(selection,studentArray, teacherArray)
            case "G:" | "Grade:" : searchByGrade(selection,studentArray, teacherArray)
            case "I" | "Info" : displayGradeCount(studentArray, teacherArray)
            case "E" | "Enrollment" : displayClassroomCount(studentArray, teacherArray)
            case "C:" | "Classroom:" : searchByClassNumber(selection, studentArray, teacherArray)
            case "GPA:" if selection[1] == "Grade" : gpaByGrade(studentArray)
            case "GPA:" if selection[1] == "Teacher" : gpaByTeacher(studentArray, teacherArray)
            case "GPA:" if selection[1] == "Bus" : gpaByBus(studentArray)
            case _: print(selection, "Invalid input")
        print("")
if __name__ == "__main__":
    main()


