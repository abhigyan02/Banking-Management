from datetime import date
from tools import dataentering
import base64
def age(birthdate):
    if birthdate is None:
        return -1
    else:
        today = date.today()
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

class EmployeeEditor:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.emp_no = None
        self.birth_date = None
        self.hire_date = None
        __password = None
    def start_editing_process(self):
        print("---------Edit employee process----------\n")
        while True:
            print("input ~ to quit")
            emp_no = input("Enter emp_no of the employee to edit the details: ")
            if emp_no == "~":
                break
            if len(emp_no) <= 5:
                try:
                    self.emp_no = int(emp_no)
                    print("Checking...")
                except ValueError:
                    print("emp_no should be an integer!!")
                else:
                    self.load_employee_details()
                    break
            else:
                print("Maximum length is 5!")

    def load_employee_details(self):
        self.cur.execute("SELECT * FROM employees WHERE emp_no=%s", (self.emp_no,))
        results = self.cur.fetchall()
        if len(results) == 0:
            print("That employee number does not exist.")
        else:
            results1 = results[0]
            print("1. emp_no:", results1[0])
            print("2. birth_date:", results1[1])
            print("3. first_name:", results1[2])
            print("4. last_name:", results1[3])
            print("5. gender:", results1[4])
            print("6. hire_date:", results1[5])
            print("7. password")
            # print("8. protected_class")
            self.birth_date = results1[1]
            self.hire_date = results1[5]
            self.edit_employee_details()

    def edit_employee_details(self):
        print("0 to quit.")
        option = input("What would you like to change from the above:")

        if option == '0':
            return
        options = {
            '1': self.update_emp_no,
            '2': self.update_birth_date,
            '3': self.update_first_name,
            '4': self.update_last_name,
            '5': self.update_gender,
            '6': self.update_hire_date,
            '7': self.manage_password,
            # '8': self.update_protected_class,
        }
        options.get(option, lambda: print("Invalid option"))()

    def update_emp_no(self):
        en = dataentering.primary_key_no("emp_no")
        query = "UPDATE employees SET emp_no=%s WHERE emp_no=%s"
        query2 = "UPDATE empass SET emp_no=%s WHERE emp_no=%s"
        data = (en, self.emp_no)
        done = dataentering.tableupdate(self.conn, self.cur, query, data)
        if done:
            done = dataentering.tableupdate(self.conn, self.cur, query2, data)
            if done:
                print("Updated employee number...")

    def update_birth_date(self):
        self.birth_date = dataentering.birthdate("employee", 20, 60)
        if age(self.birth_date) - age(self.hire_date) >= 20:
            query = "UPDATE employees SET birth_date=%s WHERE emp_no=%s"
            data = (self.birth_date, self.emp_no)
            done = dataentering.tableupdate(self.conn, self.cur, query, data)
            if done:
                print("Updated birth date")
        else:
            print("Employee must be at least 20 years of age when hired!!")
            print(self.birth_date, ": birth_date")
            print(self.hire_date, ":hire date you entered")

    def update_first_name(self):
        first_name = dataentering.fname()
        query = "UPDATE employees SET first_name=%s WHERE emp_no=%s"
        data = (first_name, self.emp_no)
        done = dataentering.tableupdate(self.conn, self.cur, query, data)
        if done:
            print("Updated first name...")

    def update_last_name(self):
        last_name = dataentering.lname()
        query = "UPDATE employees SET last_name=%s WHERE emp_no=%s"
        data = (last_name, self.emp_no)
        done = dataentering.tableupdate(self.conn, self.cur, query, data)
        if done:
            print("Updated last name...")

    def update_gender(self):
        gender = dataentering.gender()
        query = "UPDATE employees SET gender=%s WHERE emp_no=%s"
        data = (gender, self.emp_no)
        done = dataentering.tableupdate(self.conn, self.cur, query, data)
        if done:
            print("Updated gender...")

    def update_hire_date(self):
        self.hire_date = dataentering.date2("employee", self.birth_date, "hire", 20, 60)
        query = "UPDATE employees SET hire_date=%s WHERE emp_no=%s"
        data = (self.hire_date, self.emp_no)
        done = dataentering.tableupdate(self.conn, self.cur, query, data)
        if done:
            print("Updated hire date...")

    def manage_password(self):
        print("1. Show the password")
        print("2. Change the password")
        ans = input("Enter your choice (1,2):")
        if ans == '1':
            self.cur.execute("SELECT pass FROM empass WHERE emp_no=%s", (self.emp_no,))
            result = self.cur.fetchall()
            decoded_pwd=base64.b64decode(result[0][0].encode('utf-8'))
            decoded_pwd=decoded_pwd.decode('utf-8')
            print(decoded_pwd, "is the password.")
        elif ans == '2':
            while True:
                __password = input("Enter employee login password (max 8 characters, min 4, integer only): ")
                encode_password=base64.b64encode(__password.encode('utf-8'))
                lp = len(__password)
                if lp > 8:
                    print("Max 8 characters only.")
                elif lp < 4:
                    print("Minimum 4 characters to be entered.")
                else:
                    query = "UPDATE empass SET pass=LPAD(%s,%s,'0') WHERE emp_no=%s"
                    lp=len(encode_password)
                    data = (encode_password, lp, self.emp_no)
                    done = dataentering.tableupdate(self.conn, self.cur, query, data)
                    if done:
                        print("Password changed successfully!!!")
                        break

    # def update_protected_class(self):
    #     protected_class = dataentering.protected_class()
    #     query = "UPDATE employees SET protected_class=%s WHERE emp_no=%s"
    #     data = (protected_class, self.emp_no)
    #     done = dataentering.tableupdate(self.conn, self.cur, query, data)
    #     if done:
    #         print("Updated protected class...")
