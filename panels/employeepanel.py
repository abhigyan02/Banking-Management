from employee import createaccount
from employee import editaccount
from employee.editaccount import EditAccount
from employee import deleteaccount
from employee import showaccounts
import maskpass
import base64
def ep(conn,cur):
    print("\nWelcome employee!!")
    print("Please log in with your creds (emp_id and password):")
    print("---------------------Employee Panel--------------------")
    print("1.Employee login.")
    print("2.Quit.")
    ch = input("Enter your choice:")
    logged_in= bool(False)
    match ch:
        case "1":
            print("------------login panel-------------")
            logged_in = bool(True)
        case "2":
            pass
        case _:
            print("Wrong input!!!(1 or 2 only)")
    if logged_in:
        while True:
            emp_no=input("Enter emp_no (max 5 int): ")
            if len(emp_no) <= 5:
                try:
                    emp_no=int(emp_no)
                    print("Done OK")
                except ValueError:
                    print("emp_no should be an integer!!")
                else:
                    break
            else:
                print("Maximum length is 5!")

        cur.execute("select * from empass where emp_no = {}".format(emp_no))
        record=cur.fetchall()
        if record == []:
            print("This emp_no doesn't exist!!!")
        else:
            while True:
                password=record[0][1]
                print("\nInput ~ to quit.")
                a=maskpass.askpass(prompt="Enter your password to continue:",mask='*')
                print()
                decoded_password=base64.b64decode(password.encode('utf-8'))
                decoded_password=decoded_password.decode('utf-8')
                if a==decoded_password:
                    choice=menu(emp_no,cur)
                    match choice:
                        case "1":
                            createaccount.ep1(conn,cur)
                        case "2":
                            edit_account = EditAccount(conn, cur)
                            edit_account.ep2()
                        case "3":
                            deleteaccount.ep3(conn,cur)
                        case "4":
                            showaccounts.ep4(cur)
                        case "0":
                            break
                        case _:
                            print("Wrong input!")
                elif a == "~" : break
                else:
                    print("Wrong password!!")
                    break
                
def menu(x,cur):
    cur.execute("select first_name,last_name from employees where emp_no = {}".format(x))
    record=cur.fetchone()
    print("---------------Welcome {} {} ----------------".format(record[0],record[1]))
    print("1.Create client account")
    print("2.Change client details")
    print("3.Close client account")
    print("4.Show client table")
    print("Enter 0 to quit.")
    choice=input("Enter your choice: ")
    return choice