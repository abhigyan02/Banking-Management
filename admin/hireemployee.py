import mysql.connector
from tools import dataentering
import base64
def ap1(query,cur):
    print("-------------Hire Employee Process-------------")

#Employee number
    emp_no=dataentering.primary_key_no("emp_no")
#Employee Birth date
    birth_date=dataentering.birthdate("employee",20,60)
#Employee name
    first_name,last_name=dataentering.fname(),dataentering.lname()
#Employee Gender
    gender=dataentering.gender()
#Employee hire date
    hire_date=dataentering.date2("Employee",birth_date,"hire",20,60)


    print("=========== Final Data ===========")
    print(emp_no,birth_date,first_name,last_name,gender,hire_date)
    add_employee=("INSERT INTO employees "
    "(emp_no,birth_date,first_name,last_name,gender,hire_date) "
    "VALUES (%s,%s,%s,%s,%s,%s)")
    data_employee=(emp_no,birth_date,first_name,last_name,gender,hire_date)
    try:
        cur.execute(add_employee, data_employee)
        query.commit()
    except mysql.connector.Error as err:
        print(err.msg)
        print("-----------Value addition was unsuccessful!!!!-------------")
    else:
        print("Values added successfully!!")
        while True:
            password=input("Enter employee login password(max 8 characters, min 4, inteeger only): ")
            encode_password=base64.b64encode(password.encode('utf-8'))
            lp=len(password)
            if lp>8:
                print("Max 8 characters only.")
            elif lp<4:
                print("Minimum 4 characters to be entered.")
            else:
                try:
                    lp=len(encode_password)
                    cur.execute("INSERT INTO empass (emp_no,pass) VALUES('{}','{}')".format(emp_no,encode_password.decode('utf-8')))
                    query.commit()
                except mysql.connector.Error as err:
                    print(err.msg)
                    print("-----------Password addition was unsuccessful!!!!-------------")
                else:
                    print("Password added successfully!!!")
                    break
