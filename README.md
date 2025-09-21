# Secure Student Database System - Python Project

## Overview

This project is a secure, modular Python-based student database system. It demonstrates good programming practices, object-oriented design, and data security. The system allows both **students** and **admins** to interact with student records safely and efficiently.

## Key Features

* **Modular Design:** Each functionality is separated into modules for step-by-step execution and easier maintenance.
* **Object-Oriented Programming:**

  * `User` base class with inheritance in the `Admin` class.
  * Encapsulation of user data and methods.
* **Data Security:**

  * Student passwords are hashed using **SHA-256** before storage.
  * Input validation with **regular expressions (regex)** to ensure correct formats.
* **Data Storage:**

  * Student records are stored in **JSON** files for structured and persistent storage.
  * Students can export their data to **CSV** for reporting or analysis.
* **Enhanced Console Interface:**

  * Colored text and prompts using **Colorama** for better readability.

## Technologies Used

* Python 3.10.1
* JSON for data storage
* CSV for data export
* Regex for input validation
* SHA-256 hashing for password security
* Colorama for terminal styling

## File Structure

```
Secure_Student_Database/
├── main.py                # Main program
├── modules/               # Modular Python files
│   ├── admin.py           # Admin class and methods
│   ├── student.py         # Student class and methods
│   └── utils.py           # Helper functions (validation, hashing, etc.)
├── data/                  # JSON storage files
│   └── students.json
├── exports/               # Folder for exported CSVs
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/Secure_Student_Database.git
```

2. Navigate to the project folder:

```bash
cd Secure_Student_Database
```

3. Install dependencies:

```bash
pip install colorama
```

## Usage

1. Run the main program:

```bash
python main.py
```

2. Follow on-screen prompts to:

   * Log in as a student or admin
   * View, edit, or export student records
   * Add or remove student entries (admin only)
3. Student data is automatically saved to JSON; CSV export is optional.

## Security Features

* **SHA-256 Password Hashing:** Protects student login credentials.
* **Regex Validation:** Ensures emails, phone numbers, and other inputs follow the correct format.
* **Role-Based Access:** Admins can manage all data, students can only view/export their own data.

## Author

Aiden O'Roark

## License

This project is for educational purposes.
