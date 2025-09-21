#Name: Aiden O'Roark
#700: 700763212
#Description: Utility file to create functions for the json database, password validation, also
#hashes passwords for storage

#Imports and initializing colorama
import json
import os
import re
import hashlib
import csv
import colorama
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

#Create the json file
database_file = "database.json"

#Function to load json information into python
def load_data():
    if not os.path.exists(database_file):
        return {"users": {}, "students": []}
    with open(database_file, "r") as f:
        return json.load(f)

#Function to save data to json file
def save_data(data):
    with open(database_file, "w") as f:
        json.dump(data, f, indent=2)

#Function to send student data to a csv file
def student_csv(data, filename="student_report.csv"):
    students = data.get("students", [])
    if not students:
        print(Fore.RED + "No student data to export")
        return
    #Fieldnames makes it so the column header is the students keys (e.g. user_email, 700_number...)
    fieldnames = list(students[0].keys())
    try:
        with open(filename, mode="w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for student in students:
                writer.writerow(student)
        print(f"Student data exported successfully to {filename}")
    except Exception as e:
        print(f"Failed to export data to csv file: {e}")

#Function to hash passwords with sha256 encoding
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

#Function to check if the python hashed password is the same as
#the hashed password in the json database
def verify_password(plain, hashed):
    return hash_password(plain) == hashed

#Function to use regex to validate emails with gmail, yahoo, and ucmo domains
def validate_email():
    pattern = r"^[\w\.-]+@(?:gmail|yahoo|ucmo)\.(?:com|edu)$"
    while True:
        email = input("Enter email: ").strip()
        if re.match(pattern, email):
            return email
        print(Fore.RED + "Invalid email. Only @gmail, @yahoo, and @ucmo allowed.")

#Function to use regex to validate passwords that begin with certain special characters
#Is 6-12 characters long, contains atleast one uppercase letter, at least one lowercase letter
#and atleast one digit
def validate_password():
    special_char = r"^[!@#$%^&*]"
    while True:
        pwd = input("Enter password: ").strip()
        if (
            #Checks if password begins with special character
            re.match(special_char, pwd) and
            #Validates password length
            6 <= len(pwd) <= 12 and
            #Checks for uppercase, lowercase, and digit
            any(c.isupper() for c in pwd) and
            any(c.islower() for c in pwd) and
            any(c.isdigit() for c in pwd)
        ):
            return pwd
        print(Fore.RED + "Invalid password." + " Password must start with a special char (!@#$%^&*), "
              "at least 6-12 chars long, must have 1 digit, 1 uppercase, 1 lowercase.")

#Use regex to validate 700 number and also make sure it's unique to each student
def validate_700(data):
    pattern = r"^700\d{6}$"
    while True:
        number = input("Enter 700 number: ").strip()

        if not re.match(pattern, number):
            print("Invalid 700 number format. Must start with 700 and be 9 digits")
            continue

        #Check if the 700 number is already taken
        is_unique = True
        for student in data["students"]:
            if student["700_number"] == number:
                is_unique = False
                print(Fore.RED + "Error: 700 number already exists. Please enter a unique number.")
                break

        if is_unique:
            return number

    #Get rid of the explicit return statement
    return None


def validate_name(which):
    #Regex pattern to check for a name that starts with a capital, and
    #has at least 2 letters
    pattern = r"^[A-Z][a-z]{1,}$"
    while True:
        name = input(f"Enter {which} Name: ").strip()
        if re.match(pattern, name):
            return name
        print("Name must start with an uppercase and have at least " + Back.YELLOW +
              Fore.BLACK + "2 letters. No special characters")

#Make sure age is between 16 and 100
def validate_age():
    while True:
        try:
            age = int(input("Enter age: ").strip())
            if 16 <= age <= 100:
                return age
            else:
                print("Age must be between 16 and 100.")
        except ValueError:
            print(Fore.RED + "Invalid input. Enter a number.")

#Make sure phone number is a valid input and also shows the correct format for reference
def validate_phone():
    #Regex to validate a phone number
    pattern = r"^\d{3}-\d{3}-\d{4}$"
    while True:
        phone = input("Enter phone number " + Back.YELLOW + Fore.BLACK + "(xxx-xxx-xxxx):" + Style.RESET_ALL +
                      " ").strip()
        if re.match(pattern,phone):
            return phone
        print("Invalid phone number format")

#Make sure any gender inputs aren't super long
def validate_gender():
    while True:
        gender = input("Enter gender: ").strip()
        if len(gender) <= 10:
            return gender
        print("Gender must be 10 characters or fewer.")

#Function to allow admin's to enter grades for students
def enter_grades():
    grades = []
    print("Enter grades (type 'done' to finish): ")
    while True:
        grade = input("Grade: ").strip()
        if grade.lower() == "done":
            break
        try:
            grades.append(int(grade))
        except ValueError:
            print(Fore.RED + "Enter a valid number.")
    return grades

#Function to be used in student report cards to calculate average grade
def average_grade(grades):
    if not grades:
        return "Average Grade: N/A"
    return round(sum(grades) / len(grades), 2)

#Student report card main function to assign letter grades
def letter_grade(avg):
    if avg >= 90:
        return Fore.LIGHTGREEN_EX + 'A'
    elif avg >= 80:
        return Fore.GREEN + 'B'
    elif avg >= 70:
        return Fore.LIGHTYELLOW_EX + 'C'
    elif avg >= 60:
        return Fore.YELLOW + 'D'
    else:
        return Fore.RED + 'F'

#Function to print a report card
#This display function will be in the utils file so that it
#can be called by both the user and admin classes
def report_card(student):
    print(Fore.CYAN + "\n===== Report Card =====")
    print(f"Name: {student['first_name']} {student['last_name']}")
    print(f"700 Number: {student['700_number']}")
    print(f"Grades: {student['grades']}")

    #Assign new variable names to util functions
    avg = average_grade(student['grades'])
    letter = letter_grade(avg)
    print(f"Average: {avg}")
    print(f"Letter Grade: {letter}")
    print(Fore.CYAN + "========================\n")