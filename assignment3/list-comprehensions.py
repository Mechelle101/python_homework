
import csv

# Task 3: List comprehension practice
# reading employees.csv into a list of lists
with open('../csv/employees.csv', newline='') as file: 
    reader = csv.reader(file)
    rows = list(reader)

# build a list of full names using list comprehension
# row[0] = header so skip by slicing rows[1:]
names = [row[0] + " " + row[1] for row in rows[1:]]
print(names)

# lastly filter names that contain e
names_with_e = [name for name in names if "e" in name.lower()]
print(names_with_e)
