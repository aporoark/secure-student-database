#Name: Aiden O'Roark
#Description: Create the student class that will define the student information
#and then send it to their record with the right format
#Used to store the function used to create students

import utils
import colorama
from colorama import Fore

#Initialize colorama
colorama.init(autoreset=True)

class Student:
    def __init__(self, user_email, number, first_name, last_name, age, gender, phone, grades):
        self.user_email = user_email
        self.number = number
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.phone = phone
        self.grades = grades
    #Function to save student objects in dictionary that can be sent to the JSON
    def dictionary(self):
        return {
            "user_email": self.user_email,
            "700_number": self.number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone,
            "grades": self.grades
        }

#Function to create a new student
def create_student(user_email=None, data=None, prompt_for_email=False):
    if prompt_for_email:
        #Prompt for a valid email
        user_email = utils.validate_email()

        #Make sure user is registered in the database
        user = data["users"].get(user_email)
        if not user:
            print(Fore.RED + "That email has not been registered as a user.")
            return None

        #Check each student in the students list to prevent a duplicate
        for s in data["students"]:
            if s["user_email"] == user_email:
                print(Fore.RED + "A student record already exists for this email.")
                return None

        #Make sure the 700 number is matched to the user
        number = utils.validate_700(data)
        if user["700_number"] != number:
            print(Fore.RED + "700 number doesn't match the one linked to this user.")
            return None
    else:
        number = utils.validate_700(data)

#Prompt for the rest of the user's info

    first = utils.validate_name("First")
    last = utils.validate_name("Last")
    age = utils.validate_age()
    gender = utils.validate_gender()
    phone = utils.validate_phone()
    grades = utils.enter_grades()
    return Student(user_email, number, first, last, age, gender, phone, grades)
