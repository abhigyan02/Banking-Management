from datetime import date
from tools import dataentering
import base64
acc_no=None
first_name=None
last_name=None
gender=None
birth_date=None
acc_creation_date=None
mobile_no=None
email_id=None
password = None

def age(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age

class EditAccount:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
        self.acc_no = None
        self.first_name = None
        self.last_name = None
        self.gender = None
        self.birth_date = None
        self.acc_creation_date = None
        self.mobile_no = None
        self.email_id = None
        self._password = None

    def ep2(self):
        while True:
            print("\ninput ~ to quit")
            acc_no = input("Enter acc_no (max 5 int) to edit details: ")
            if acc_no == "~":
                break
            elif len(acc_no) <= 5:
                try:
                    acc_no = int(acc_no)
                    print("Done OK")
                except ValueError:
                    print("acc_no should be an integer!!")
                    continue
            else:
                print("Maximum length is 5!")
                continue

            self.cur.execute("SELECT * FROM clients WHERE acc_no={}".format(acc_no))
            results = self.cur.fetchall()
            print(results)
            if len(results) == 0:
                print("That account number does not exist.")
            else:
                results1 = results[0]
                self.acc_no = acc_no
                self.first_name = results1[2]
                self.last_name = results1[3]
                self.gender = results1[4]
                self.birth_date = results1[5]
                self.acc_creation_date = results1[6]
                self.mobile_no = results1[7]
                self.email_id = results1[8]
                self._password = results1[9]

                print("1. first_name            = ", self.first_name)
                print("2. last_name             = ", self.last_name)
                print("3. gender                = ", self.gender)
                print("4. birth_date            = ", self.birth_date)
                print("5. account_creation_date = ", self.acc_creation_date)
                print("6. mobile_no             = ", self.mobile_no)
                print("7. email_id              = ", self.email_id)
                print("8. password")
                print("0 to quit")
                self.ep2f2()

    def ep2f2(self):
        choice = input("What would you like to change from here: ")

        match choice:
            case "1":
                self.first_name = dataentering.fname()
                query = "UPDATE clients SET first_name=%s WHERE acc_no=%s"
                data = (self.first_name, self.acc_no)
                done = dataentering.tableupdate(self.conn, self.cur, query, data)
                if done:
                    print("Updated first name")

            case "2":
                self.last_name = dataentering.lname()
                query = "UPDATE clients SET last_name=%s WHERE acc_no=%s"
                data = (self.last_name, self.acc_no)
                done = dataentering.tableupdate(self.conn, self.cur, query, data)
                if done:
                    print("Updated last name")

            case "3":
                self.gender = dataentering.gender()
                query = "UPDATE clients SET gender=%s WHERE acc_no=%s"
                data = (self.gender, self.acc_no)
                done = dataentering.tableupdate(self.conn, self.cur, query, data)
                if done:
                    print("Updated gender")

            case "4":
                self.birth_date = dataentering.birthdate("Client", 10, 100)
                if age(self.birth_date) - age(self.acc_creation_date) >= 10:
                    query = "UPDATE clients SET birth_date=%s WHERE acc_no=%s"
                    data = (self.birth_date, self.acc_no)
                    done = dataentering.tableupdate(self.conn, self.cur, query, data)
                    if done:
                        print("Updated birth date")
                else:
                    print("The client should be at least 10 years of age.")
                    print("Birth date:", self.birth_date)
                    print("Account Creation Date:", self.acc_creation_date)

            case "5":
                self.acc_creation_date = dataentering.date2("client", self.birth_date, "account_creation", 10, 100)
                query = "UPDATE clients SET acc_creation_date=%s WHERE acc_no=%s"
                data = (self.acc_creation_date, self.acc_no)
                done = dataentering.tableupdate(self.conn, self.cur, query, data)
                if done:
                    print("Updated account creation date")

            case "6":
                self.mobile_no, lmn = dataentering.mobileno()
                query = "UPDATE clients SET mobile_no=LPAD(%s,%s,'0') WHERE acc_no=%s"
                data = (self.mobile_no, lmn, self.acc_no)
                done = dataentering.tableupdate(self.conn, self.cur, query, data)
                if done:
                    print("Updated mobile number")

            case "7":
                self.email_id = dataentering.email()
                query = "UPDATE clients SET email=%s WHERE acc_no=%s"
                data = (self.email_id, self.acc_no)
                done = dataentering.tableupdate(self.conn, self.cur, query, data)
                if done:
                    print("Updated email id")

            case "8":
                while True:
                    print("1. Show Password")
                    print("2. Change Password")
                    print("0 to quit")
                    choice = input("Enter choice: ")
                    match choice:
                        case "1":
                            print("\nThe password will be printed on the next line")
                            decoded_pwd=base64.b64decode(self._password)
                            decoded_pwd=decoded_pwd.decode('utf-8')
                            print(decoded_pwd)
                            
                            print()
                        case "2":
                            self._password, lp = dataentering.clientpassword()
                            # self._password=base64.b64encode(__password.encode('utf-8'))
                            query = "UPDATE clients SET pass=%s WHERE acc_no=%s"
                            data = (self._password, self.acc_no)
                            done = dataentering.tableupdate(self.conn, self.cur, query, data)
                            if done:
                                print("Updated password")
                        case "0":
                            break
                        case _:
                            print("Wrong input!!")

            case "0":
                pass

            case _:
                print("Wrong input!!")

