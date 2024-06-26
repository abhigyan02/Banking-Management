from admin import hireemployee
from admin import fireemployee
from admin import editemployee
from admin import showemployee
from admin.editemployee import EmployeeEditor
from tools import connection
def ap(query, conn):
    print("\nWelcome Admin!!")

    while True:
        print("\n---------------------Admin Panel-----------------------")
        print("\n1.Hire Employee")
        print("2.Fire Employee")
        print("3.Change employee data")
        print("4.Show employee table")
        print("\nInput 0 to quit.")
        a = input("Enter choice:")
        match a:
            case '1':
                hireemployee.ap1(query, conn)
            case '2':
                fireemployee.ap2(query, conn)
            case '3':
                editor=editemployee.EmployeeEditor(conn,connection.cur)
                editor.start_editing_process()
            case '4':
                showemployee.ap4(conn)
            case '0':
                print("Quit Admin Panel.")
                break
            case _:
                print("Wrong input! (1, 2, 3, 4)")

# Add code to create a database connection and cursor, then call ap function
# import necessary modules and initialize database connection
