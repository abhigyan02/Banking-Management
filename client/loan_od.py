from tools import dataentering
def cp5(cur,acc_type,acc_no):
    loan_or_od=None
    if acc_type=="current":
        loan_or_od="overdraft"
    else:
        loan_or_od="loan"
    cur.execute("select {} from {} where acc_no={}".format(loan_or_od,acc_type,acc_no))
    a=cur.fetchall()
    if a[0][0]=="NO" and acc_type=="savings":
        loan_amt,loan_type=loan_process()
        time_period=12
        intrest=8
        total_loan=loan_amt+(loan_amt*0.08)
        amt_per_month=total_loan/time_period
        cur.execute(f"update savings SET loan='YES' where acc_no={acc_no}")
        cur.execute(f"INSERT INTO loan VALUES ({acc_no},'{loan_type}',{loan_amt},{time_period},{intrest},{amt_per_month},{total_loan})")      
    elif a[0][0]=="NO" and acc_type=="current":
        overdraft=int(input("enter overdraft amount you want to take:"))
        cur.execute(f"update current SET overdraft='YES' where acc_no={acc_no}") 
        cur.execute(f"INSERT INTO overdraft VALUES ({acc_no},{overdraft},{overdraft+(overdraft*0.08)})") 
    elif a[0][0]=="YES" and acc_type=="current":
        cur.execute("select {}_amt from {} where acc_no={}".format(loan_or_od,loan_or_od,acc_no))
        od=cur.fetchall()
        od=od[0][0]
        print(f"Your remaining od amount is {od}")
    else:
        print("You already have a loan pending to repay...")
        cur.execute("select {}_amt,{}_type from {} where acc_no={}".format(loan_or_od,loan_or_od,loan_or_od,acc_no))
        loan=cur.fetchall()
        loan_type=loan[0][1]
        if loan_type=='PL':loan_type='Personal Loan'
        if loan_type=='HL':loan_type='Health Loan'
        if loan_type=='EL':loan_type='Education Loan'
        if loan_type=='TL':loan_type='Term Loan'
        else:loan_type='Business Loan'
        loan_amt=loan[0][0]
        print("Your remaining od amount is {} of loan type {}".format(loan_amt,loan_type))


def loan_process():
    while True:
        loan_amt=input("Enter loan amount: ")
        try:
            loan_amt=int(loan_amt)
        except ValueError:
            print("Loan amount should be an integer")
        else:
            print("Done OK")
            break

    while True:
        print()
        print("1.Personal Loan")
        print("2.Home Loan")
        print("3.Education Loan")
        print("4.Term Loan")
        print("5.Business Loan")
        print(" Input ~ to quit\n")
        loan_type=input("Enter choice: ")
        if loan_type=="1":
            loan_type='PL'
            break
        elif loan_type=="2":
            loan_type='HL'
            break
        elif loan_type=="3":
            loan_type='EL'
            break
        elif loan_type=="4":
            loan_type='TL'
            break
        elif loan_type=="5":
            loan_type='BL'
            break
        elif loan_type=="~":
            break
        else:
            print("Wrong Input!!")
    
    if loan_type!="~":
        return loan_amt,loan_type
        #TODO: Add a method to store requests in dat file or csv file...
