
import pandas as pd
import json

# Task 1: creating dataframe
task1_dict = {
  'Name': ['Alice', 'Bob', 'Charlie'], 
  'Age': [25, 30, 35], 
  'City': ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(task1_dict)

print("Task 1 DataFrame:")
print(task1_data_frame)

# Task 1.2: adding a new column
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]

print("\nTask 1.2 DataFrame with Salary:")
print(task1_with_salary)

# Task 1.3: incrementing age by 1
task1_older = task1_with_salary.copy()
task1_older['Age'] = task1_older['Age'] + 1

print("\nTask 1.3 DataFrame with Incremented Age:")
print(task1_older)

# Task 1.4: writing DataFrame to CSV (no index)
task1_older.to_csv('employees.csv', index=False)

print("\nTask 1.4: DataFrame written to employees.csv")

# Task 2: Loading Data from CSV and JSON
task2_employees = pd.read_csv('employees.csv')

print("\nTask 2 DataFrame from CSV:")
print(task2_employees)

# Task 2.2: Loading Data from JSON
additional_employees = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
]

with open("additional_employees.json", "w") as f:
  json.dump(additional_employees, f)
  
json_employees  = pd.read_json("additional_employees.json")

print("\nTask 2.2 DataFrame from JSON:")
print(json_employees)

# Task 2.3: Concatenating DataFrames
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)

print("\nTask 2.3 Concatenated DataFrame:")
print(more_employees)

# Task 3: Data Inspection: Head, Tail, and Info
first_three = more_employees.head(3)

print("\nTask 3.1 First Three Rows:")
print(first_three)

# Task 3.2: Last Two Rows
last_two = more_employees.tail(2)

print("\nTask 3.2 Last Two Rows:")
print(last_two)

# Task 3.3: Shape of DataFrame
employee_shape = more_employees.shape

print("\nTask 3.3 Shape of DataFrame: rows/columns")
print(employee_shape)

# Task 3.4: Info()
print("\nTask 3.4 DataFrame Info:")
more_employees.info()

# Task 4: Data Cleaning
dirty_data = pd.read_csv('dirty_data.csv')

print("\nTask 4.1 Dirty Data")
print(dirty_data)

# making a copy for cleaning
cleaned_data = dirty_data.copy()

print("\nTask 4.1 clean data copy")
print(cleaned_data)

# Task 4.2: Remove Duplicates
clean_data = cleaned_data.drop_duplicates()

print("\nTask 4.2 Data after removing duplicates:")
print(clean_data)

# Task 4.3: Handle Missing Values and and Convert Age to numeric
clean_data['Age'] = pd.to_numeric(clean_data["Age"], errors= "coerce")

print("\nTask 4.3 - clean data (age converted to numeric):")
print(clean_data)

# Task 4.4: Clean Salary Column
clean_data["Salary"] = clean_data["Salary"].replace(['unknown', 'n/a'], pd.NA)
clean_data["Salary"] = pd.to_numeric(clean_data["Salary"], errors= "coerce")

print("\nTask 4.4 - clean data (salary cleaned and converted to numeric")
print(clean_data)

# Task 4.5: Fill Missing Values in Age and Salary
age_mean = clean_data["Age"].mean()
salary_median = clean_data["Salary"].median()

clean_data["Age"] = clean_data["Age"].fillna(age_mean)
clean_data["Salary"] = clean_data["Salary"].fillna(salary_median)

print("\nTask 4.5 - clean data (missing age and salary filled):")
print(clean_data)
      
# Task 4.6: Convert Hire Date to datetime
clean_data["Hire Date"] = pd.to_datetime(clean_data["Hire Date"], errors="coerce")

print("\nTask 4.6 - clean data (hire date converted to datetime):")
print(clean_data)

# Task 4.7: Strip Whitespace and Standardize Department Names
clean_data["Name"] = clean_data["Name"].str.strip().str.upper()
clean_data["Department"] = clean_data["Department"].str.strip().str.upper()

print("\nTask 4.7 - clean data (name and department standardized):")
print(clean_data)


