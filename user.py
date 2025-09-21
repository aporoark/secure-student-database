#Name: Aiden O'Roark
#700: 700763212
#Description: File to hold all functions that will be utilized by the user and admins

#Import functions from the utils file and the student class
from student import create_student
import utils
import colorama
from colorama import Fore

#Initialize colorama
colorama.init(autoreset=True)

#Create the user class that will create all the basic starting functions
#to create an account for students and allow them to create an account
class User:
    #Initialize values
    def __init__(self, email=None, username=None, password=None, number=None, role="user"):
        self.email = email
        self.username = username
        self.password = password
        self.role = role
        self.number = number

    #Register users and holds the data in memory so it can be saved to the json later in correct format
    def register(self, data):
        print(Fore.CYAN + "\n--- Register ---")
        self.email = utils.validate_email()
        self.username = input("Enter username: ").strip()
        self.password = utils.validate_password()
        self.number = utils.validate_700(data)
        #Hash the password
        hashed_password = utils.hash_password(self.password)

        #Prompt user for admin status
        wants_admin = input("Registering as admin? (yes/no): ").strip().lower()

        role = "user"

        #Grant users with the correct password the admin role
        if wants_admin == "yes":
            secret = input("Enter the secret admin password: ").strip()
            if secret == "password!1":  #You can change this to any admin code you want
                role = "admin"
                print(Fore.GREEN + "Admin access granted.")
            else:
                print(Fore.RED + "Incorrect secret password. Registering as normal user.")

        #Store data in memory and make format correct for when it's dumped into the json file
        data["users"][self.email] = {
            "username": self.username,
            "password": hashed_password,
            "role": role,
            "700_number": self.number
        }
        print(Fore.GREEN + f"User {self.username} registered successfully")

    #Function to allow registered user's to log in
    #Doesn't allow too many failed attempts
    def login(self, data):
        print(Fore.CYAN + "\n--- Login ---")
        attempts = 0
        while attempts < 3:
            email = input("Email: ").strip()
            password = input("Password: ").strip()
            #Checks for the user's email to verify they are registered
            user = data["users"].get(email)
            if user and utils.verify_password(password, user["password"]):
                print(f"Welcome, {user['username']}!")
                self.email = email
                self.username = user["username"]
                self.password = user["password"]
                self.role = user["role"]
                return True

            else:
                print(Fore.YELLOW + "Invalid email or password.")
                attempts += 1
        print(Fore.RED + "Too many failed attempts. Returning to main menu.")
        return False

    #Function to allow students to view their grades
    def view_user_data(self, data):
        #Checks to make sure the self.email is in the student database
        for student in data["students"]:
            if student.get("user_email") == self.email:
                print(Fore.CYAN + f"\n--- Report Card for {student['first_name']} {student['last_name']} ---")
                utils.report_card(student)
                return
        print(Fore.YELLOW + "No student record found.")

class Admin(User):
    def __init__(self, email, username, password, number):
        #Inherit the values from the user class
        super().__init__(email, username, password, number, role="admin")

    def add_student(self, data):
        print(Fore.CYAN + f"\n--- {self.username} is adding a student ---")

        new_student = create_student(prompt_for_email=True, data=data)
        if new_student is None:
            print(Fore.YELLOW + "Student creation cancelled. Returning to Admin menu.")
            return

        data["students"].append(new_student.dictionary())
        print(Fore.GREEN + "Student added successfully.")

    def view_students(self, data):
        print(Fore.CYAN + f"\n--- {self.username}'s View of All Students ---")
        if not data["students"]:
            print(Fore.YELLOW + "No students found.")
            return

        for student in data["students"]:
            utils.report_card(student)

    def edit_student(self, data):
        print(Fore.CYAN + f"\n--- {self.username} is editing student data ---")

        student_id_to_edit = input("Enter the 700 number of the student to edit: ").strip()
        found_student = None

        for student in data["students"]:
            if student["700_number"] == student_id_to_edit:
                found_student = student
                break

        if not found_student:
            print(Fore.YELLOW + "Student not found.")
            return

        print(f"\nCurrent data for {found_student['first_name']} {found_student['last_name']}:")
        print(f"700 Number: {found_student['700_number']}")
        print(f"First Name: {found_student['first_name']}")
        print(f"Last Name: {found_student['last_name']}")
        print(f"Age: {found_student['age']}")
        print(f"Gender: {found_student['gender']}")
        print(f"Phone: {found_student['phone']}")
        print(f"Grades: {found_student['grades']}")
        print(f"User Email: {found_student['user_email']}")

        print(Fore.GREEN + "Press enter to continue to the Edit Student Sub-Menu...")
        input()

        while True:
            print(Fore.CYAN + "\n--- Edit Student Sub-Menu ---")
            print(Fore.BLUE + "Which field would you like to edit?")
            print("1. First Name")
            print("2. Last Name")
            print("3. Age")
            print("4. Gender")
            print("5. Phone Number")
            print("6. Grades")
            print(Fore.MAGENTA + "7. Done Editing")
            edit_choice = input(Fore.MAGENTA + "Enter your choice: ").strip()

            if edit_choice == "1":
                found_student["first_name"] = utils.validate_name("First")
                print(Fore.GREEN + "First name updated.")
            elif edit_choice == "2":
                found_student["last_name"] = utils.validate_name("Last")
                print(Fore.GREEN + "Last name updated.")
            elif edit_choice == "3":
                found_student["age"] = utils.validate_age()
                print(Fore.GREEN + "Age updated.")
            elif edit_choice == "4":
                found_student["gender"] = input("Enter new gender: ").strip()
                print(Fore.GREEN + "Gender updated.")
            elif edit_choice == "5":
                found_student["phone"] = utils.validate_phone()
                print(Fore.GREEN + "Phone number updated.")
            elif edit_choice == "6":
                found_student["grades"] = utils.enter_grades()
                print(Fore.GREEN + "Grades updated.")
            elif edit_choice == "7":
                print(Fore.YELLOW + "Exiting edit mode.")
                return
            else:
                print(Fore.YELLOW + "Invalid choice. Please select a valid option.")

    def delete_student(self, data):
        print(Fore.CYAN + f"\n--- {self.username} is deleting a student ---")
        student_id = input("Enter the 700 number of the student to delete: ").strip()

        for student in data["students"]:
            if student["700_number"] == student_id:
                data["students"].remove(student)
                print(Fore.RED + f"Student {student['first_name']} {student['last_name']} deleted.")
                return

        print(Fore.YELLOW + "Student not found.")



