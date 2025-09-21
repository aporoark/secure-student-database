#Name: Aiden O'Roark
#700: 700763212
#Description: Create the main function that will run the main loop and create all the menu's
#and prompt the user for inputs that will be saved by utilizing the other python files.

#Import user classes and functions from the util file
from utils import load_data, save_data, student_csv
from user import User, Admin
import colorama
from colorama import Fore

#Initialize colorama
colorama.init(autoreset=True)

#Define the main function
def main():

    #Define the load_data() function as data for simplicity
    data = load_data()

    #Create the main loop that starts the process of registering and logging in
    #and runs until the user chooses to exit
    while True:

        #Print the starting screen for the program and prompt the user for their choice
        print(Fore.CYAN + "\n==== Secure Student Management System ====")
        print(Fore.LIGHTGREEN_EX + "1. Register")
        print(Fore.BLUE + "2. Login")
        print(Fore.RED + "3. Exit")
        choice = input("Enter your choice: ").strip()

        #Use if statements to provide the outcome corresponding to the user's choice
        #Register the user and save their data
        if choice == "1":
            user = User()
            user.register(data)
            save_data(data)
        elif choice == "2":
            user = User()
            if user.login(data):
                #Check if the user has admin status
                if user.role == "admin":
                    admin = Admin(user.email, user.username, user.password, user.role)
                    admin_menu(admin, data)
                else:
                    user_menu(user,data)
                save_data(data)
        elif choice == "3":
            print(Fore.LIGHTMAGENTA_EX + "Goodbye!")
            break
        else:
            print(Fore.YELLOW + "Invalid choice. Try again.")

#Create a menu for normal user's and allows them to view their data
#if they are a student
def user_menu(user, data):
    while True:
        print(Fore.CYAN + "\n--- User Menu ---")
        print("1. View my student data")
        print("2. Logout")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            user.view_user_data(data)
            print(Fore.MAGENTA + "Press enter to return to User menu")
            input()
        elif choice == "2":
            break
        else:
            print(Fore.RED + "Invalid choice.")

#Create a separate menu for admin that allows them
#to add students, edit student information, delete students, and even send data to a csv file
def admin_menu(admin, data):
    while True:
        print(Fore.CYAN + "\n--- Admin Menu ---")
        print("1. View all students")
        print("2. Add student")
        print("3. Edit student")
        print("4. Delete student")
        print("5. Export data to CSV")
        print("6. Logout")
        choice = input("Choice: ").strip()

        #After any choice where data can be manipulated is chosen and ran,
        #the data is then saved
        if choice == "1":
            admin.view_students(data)
            input(Fore.GREEN + "Press enter to return to Admin menu")
        elif choice == "2":
            admin.add_student(data)
            save_data(data)
            print(Fore.GREEN + "Changes saved successfully.")
            print(Fore.MAGENTA + "Press enter to return to Admin menu")
            input()
        elif choice == "3":
            admin.edit_student(data)
            save_data(data)
            print(Fore.GREEN + "Changes saved successfully.")
            print(Fore.MAGENTA + "Press enter to return to Admin menu")
            input()
        elif choice == "4":
            admin.delete_student(data)
            save_data(data)
            print(Fore.GREEN + "Changes saved successfully.")
            print(Fore.MAGENTA + "Press enter to return to Admin menu")
            input()
        elif choice == "5":
            student_csv(data)
        elif choice == "6":
            break
        else:
            print(Fore.RED + "Invalid choice.")

#Call the main function
main()