import csv
import traceback
import os
import custom_module
from datetime import datetime

# Task 2
def read_employees():
    # key:value pairs of employee ID and employee name
    data = {}
    # will hold the data read from the CSV file
    rows = []

    try:
        with open('../csv/employees.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            # using enumerate to detect the first row
            for index, row in enumerate(reader):
                if index == 0:
                    data["fields"] = row  # first row is a header row
                else:
                    rows.append(row)

        # after looping the rows list is attached to data dictionary
        data["rows"] = rows
        # return the complete dictionary
        return data

    except Exception as e:
        # print the exception that occurred, and the stack trace
        print("An exception occurred.", type(e).__name__)

        # detailed traceback information
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")

employees = read_employees()
print(employees)

# Task 3
def column_index(column_name):
    # look in employees["fields"] the header row
    # return the index of the column name
    return employees["fields"].index(column_name)

employee_id_column = column_index("employee_id")
print(f"Employee ID column index: {employee_id_column}")

# Task 4
# getting the row number as parameter
def first_name(row_number):
    # this gets you the column index for first_name
    column = column_index("first_name")

    # get the row from employees["rows"]
    row = employees["rows"][row_number]

    # return the value from that column
    return row[column]

print(f"First name in row 0: {first_name(0)}")

# Task 5
def employee_find(employee_id):

    def employee_match(row):
        # returns true if there is a match
        return int(row[employee_id_column]) == employee_id

    # filter() calls employee_match once for each row
    matches = list(filter(employee_match, employees["rows"]))

    # return rows with matching employee id
    return matches

print(f"Employee with ID 3: {employee_find(3)}")

# Task 6
def employee_find_2(employee_id):
    matches = list(filter(lambda row: int(row[employee_id_column]) == employee_id, employees["rows"]))
    return matches

print(f"Employee with ID 4: {employee_find_2(4)}")

# Task 7
# sort employees['rows'] by last_name using sort() 
# and a lambda function
# returns the sorted list
def sort_by_last_name():

    # determine the column index for 'last_name'
    col = column_index("last_name")

    # sorting the rows in place
    employees["rows"].sort(key=lambda row: row[col])

    # return the sorted list
    return employees["rows"]

sort_by_last_name()
print(f"Employees sorted by last name: {employees['rows']}")
print(employees)

# Task 8
# return a dictionary from employees['raws']
# mapping field names to values, skip id...
def employee_dict(row):
    emp_dict = {}

    # Input - get the column header
    fields = employees['fields']

    # Process - loop through each column
    for i in range(1, len(fields)):
        key = fields[i]
        value = row[i]
        emp_dict[key] = value

    # Output - return the dictionary
    return emp_dict

print(f"Employee dictionary for row 0: {employee_dict(employees['rows'][0])}")

# Task 9
def all_employees_dict():
    result = {}

    # Process - map each row to a dictionary
    for row in employees['rows']:
        # key, string
        emp_id = row[employee_id_column]
        # value, dict from 8
        emp_info = employee_dict(row)

        result[emp_id] = emp_info

    # Output - return the list of dictionaries
    return result

all_employees = all_employees_dict()
print(f"All employee dictionaries: {all_employees}")

# task 10
def get_this_value():
    return os.getenv("THISVALUE")

# Task 11
# wrapper function that sets the secret in custom_module
# to the provided new_secret value
def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)


set_that_secret("my new secret")
print("Custom_module.secret is now:", custom_module.secret)

# Task 12
def read_minutes():
    minute1 = {}
    minute2 = {}

    try:
        # reading minutes1.csv
        with open('../csv/minutes1.csv', 'r') as file1:
            reader = csv.reader(file1)
            rows = []
            for index, row in enumerate(reader):
                if index == 0:
                    minute1["fields"] = row
                else:
                    rows.append(tuple(row)) # convert to tuple
            minute1["rows"] = rows

        # reading minutes2.csv
        with open('../csv/minutes2.csv', 'r') as file2:
            reader = csv.reader(file2)
            rows = []
            for index, row in enumerate(reader):
                if index == 0:
                    minute2["fields"] = row
                else:
                    rows.append(tuple(row)) # convert to tuple
            minute2["rows"] = rows

        return minute1, minute2
    
    except Exception as e:
        print("Error reading minutes files:", type(e).__name__)
        raise e
    
minutes1, minutes2 = read_minutes()
print("Minutes 1:", minutes1)
print("Minutes 2:", minutes2)

# Task 13
# create a set of all unique minutes from minutes1 and minutes2
# each row is a tuple (name, date)
def create_minutes_set():
    # convert the rows lists (tuples) into sets
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])

    # Union: all unique rows from both sets
    combined = set1.union(set2)

    return combined

# global variable used by later tasks
minutes_set = create_minutes_set()
print("Minutes Set: ", minutes_set)

# Task 14
# convert the minutes_set (the tuples)
# into a list of tuples
def create_minutes_list():
    # Processing: convert the set to a list
    minutes_list = list(minutes_set)

    # Processing: applying the map to transform each element
    converted = list( 
        map( 
            lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")),
            minutes_list
        )
    )

    # Output: return the list of tuples
    return converted

# global variable used by later tasks
minutes_list = create_minutes_list()
print("Minutes List:", minutes_list)

# Task 15
def write_sorted_list():
    # Input: sort minutes list in asc order by datetime
    minutes_list.sort(key=lambda x: x[1])

    # Processing: converting datetime back to a string
    converted = list(
        map(
            lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")),
            minutes_list
        )
    )

    # Processing: write to the csv file minutes.csv
    with open("minutes.csv", "w", newline='') as file:
        writer =csv.writer(file)
        # write the header row from minuter1["fields"]
        writer.writerow(minutes1["fields"])
        # data row from the converted list
        for row in converted:
            writer.writerow(row)

    # Output: return the converted list
    return converted

# now calling the function and store the results
sorted_minutes = write_sorted_list()
print("Sorted Minutes:", sorted_minutes)
