#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 18:15:34 2023

@author: mukeshavudaiappan
"""

import csv
import random
from faker import Faker
import sqlite3

fake = Faker()

# Function to generate random ordinal data


def generate_ordinal_data():
    roles = ["Manager", "Developer", "Analyst", "Designer", "HR"]
    return random.choice(roles)

# Function to generate random ratio data


def generate_ratio_data():
    return round(random.uniform(30000, 100000), 2)

# Function to generate random nominal data


def generate_nominal_data():
    departments = ["IT", "Finance", "HR"]
    return random.choice(departments)

# Function to generate random interval data


def generate_interval_data():
    return round(random.uniform(20, 40), 2)


# Generate Employees data
employees_data = []
for employee_id in range(1, 1001):
    employee_name = fake.name()
    role = generate_ordinal_data()
    salary = generate_ratio_data()
    hiredate = fake.date_this_decade()
    dept_no = random.randint(1, 3)
    # Create a custom email
    email = f"{employee_name.replace(' ', '.').lower()}@uh.com"

    employee = {
        "employee_id": employee_id,
        "employee_name": employee_name,
        "role": role,
        "hiredate": hiredate,
        "salary": salary,
        "dept_no": dept_no,
        "email": email,
    }
    employees_data.append(employee)

# Generate Departments data with unique department names
departments_data = []
unique_department_names = set()
for dept_no in range(1, 4):
    if dept_no == 3:
        department_name = "HR"
    else:
        while True:
            department_name = generate_nominal_data()
            if department_name not in unique_department_names:
                unique_department_names.add(department_name)
                break

    department = {
        "dept_no": dept_no,
        "department_name": department_name,
    }
    departments_data.append(department)

# Generate SalaryGrades data
roles = ["Manager", "Developer", "Analyst", "Designer", "HR"]
salary_grades_data = []
for role in roles:
    low_salary = generate_ratio_data()
    high_salary = low_salary + 15000

    salary_grade = {
        "role": role,
        "low_salary": low_salary,
        "high_salary": high_salary,
    }
    salary_grades_data.append(salary_grade)

# Define CSV file names
employees_csv_file = "employees_data.csv"
departments_csv_file = "departments_data.csv"
salary_grades_csv_file = "salary_grades_data.csv"

# Write data to CSV files
with open(employees_csv_file, mode="w", newline="") as file:
    fieldnames = ["employee_id", "employee_name",
                  "role", "hiredate", "salary", "dept_no", "email"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(employees_data)

with open(departments_csv_file, mode="w", newline="") as file:
    fieldnames = ["dept_no", "department_name"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(departments_data)

with open(salary_grades_csv_file, mode="w", newline="") as file:
    fieldnames = ["role", "low_salary", "high_salary"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(salary_grades_data)

# Function to create a SQLite database and import data from a CSV file

def create_database(csv_file, table_name, database_name):
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Create a table based on the CSV file structure
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)
        columns = ', '.join(header)
        cursor.execute(f'CREATE TABLE {table_name} ({columns})')

        # Insert data into the table
        cursor.executemany(
            f'INSERT INTO {table_name} VALUES ({", ".join(["?"] * len(header))})', 
            reader)

    # Commit changes and close connection
    conn.commit()
    conn.close()


# List of CSV files, corresponding table names, and database names

csv_files = ['employees_data.csv',
             'departments_data.csv', 'salary_grades_data.csv']
table_names = ['employees', 'departments', 'salary_grades']
database_name = 'Company_database.db'

# Create a database for each CSV file

for csv_file, table_name in zip(csv_files, table_names):
    create_database(csv_file, table_name, database_name)

