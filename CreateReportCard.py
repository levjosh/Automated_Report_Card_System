import sys
import csv
import json

# Adjust the total average and round
def calculateTotalAverage(output):
    for i in range(len(output["students"])):
        totalAverage = 0
        for j in range(len(output["students"][i]["courses"])):
            totalAverage += output["students"][i]["courses"][j]["courseAverage"]
            output["students"][i]["courses"][j]["courseAverage"] = round(output["students"][i]["courses"][j]["courseAverage"], 2)
        totalAverage /= len(output["students"][i]["courses"])
        totalAverage = round(totalAverage, 2)
        output["students"][i]["totalAverage"] = totalAverage


# Add courses and student info to JSON file
def courseAnalysis(path_to_marks, courses_dict, tests_dict, students_course_ids, student_element, student_course_element, output):
    with open(path_to_marks, 'r', newline='') as marks_csv_file:
        marks_csv = csv.reader(marks_csv_file)
        next(marks_csv)

        
        for row in marks_csv:
            course_id = tests_dict[int(row[0])][0]
            student_id = int(row[1])
            if course_id not in students_course_ids[student_id]:
                students_course_ids[student_id].append(course_id)
                student_course_element[student_id][course_id] = len(student_course_element[student_id])
                output["students"][student_element[student_id]]["courses"].append({
                    "id": course_id, "name": courses_dict[course_id][0], "teacher": courses_dict[course_id][1], "courseAverage": 0
                })
            output["students"][student_element[student_id]]["courses"][student_course_element[student_id][course_id]]["courseAverage"] += round(tests_dict[int(row[0])][1] * int(row[2])/100.0, 2)


# Change courses and tests csv file into dictionaries to read from for later
def makeDictOfCoursesAndTests(path_to_courses, path_to_tests, courses_dict, tests_dict):
    with open(path_to_courses, 'r', newline='') as courses_csv_file:
        courses_csv = csv.reader(courses_csv_file)
        next(courses_csv)

        for row in courses_csv:
            courses_dict[int(row[0])] = (row[1], row[2])

    with open(path_to_tests, 'r', newline='') as tests_csv_file:
        tests_csv = csv.reader(tests_csv_file)
        next(tests_csv)

        for row in tests_csv:
            tests_dict[int(row[0])] = (int(row[1]), int(row[2]))

# Create empty students for JSON file
def parseStudents(path_to_students, students_course_ids, student_element, student_course_element, output):
    with open(path_to_students, 'r', newline='') as students_csv_file:
        students_csv = csv.reader(students_csv_file)
        next(students_csv)

        for i, row in enumerate(students_csv):
            students_course_ids[int(row[0])] = []
            output["students"].append({"id": row[0], "name": row[1], "totalAverage": 0, "courses": []})
            student_element[int(row[0])] = i
            student_course_element[int(row[0])] = {}

# Remove the leading and trailing whitespaces and empty rows
def removeEmptySpaces(all_paths):
    for path in all_paths:
        lines = list()
        with open(path, 'r', newline='') as readFile:
            reader = csv.reader(readFile)
            for row in reader:
                if len(row) != 0:
                    lines.append([i.strip() for i in row])
            # print(lines)
        with open(path, 'w', newline='') as writeFile:
            writer = csv.writer(writeFile)
            writer.writerows(lines)
        # with open(path, 'r', newline='') as readFile:
        #     reader = csv.reader(readFile)
        #     for rows in reader:
        #         print(rows)


# Take the output dictionary and convert it to json output file
def convertDictToJSON(output, output_path):
    with open(output_path + 'output.json', 'w') as file:
        json.dump(output, file, indent=4)


# Set path to files here
path_to_courses = "Example2/courses.csv"
path_to_students = "Example2/students.csv"
path_to_tests = "Example2/tests.csv"
path_to_marks = "Example2/marks.csv"
output_path = "Example2/"
all_paths = [path_to_courses, path_to_students, path_to_tests, path_to_marks]


output = {"students": []}
courses_dict = {}
tests_dict = {}
student_element = {}
students_course_ids = {}
student_course_element = {}

removeEmptySpaces(all_paths)
parseStudents(path_to_students, students_course_ids, student_element, student_course_element, output)
makeDictOfCoursesAndTests(path_to_courses, path_to_tests, courses_dict, tests_dict)
# print(output["students"]["courses"])
# print(courses_dict)
# print(tests_dict)
# print(students_course_ids)

courseAnalysis(path_to_marks, courses_dict, tests_dict, students_course_ids, student_element, student_course_element, output)
# print(students_course_ids)
calculateTotalAverage(output)
convertDictToJSON(output, output_path)