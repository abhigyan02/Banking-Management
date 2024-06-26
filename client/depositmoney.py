from tools import dataentering
def cp2(conn,cur,acc_type,acc_no):
    cash_in_hand=dataentering.handcash(conn,cur,acc_no)
    
    deposit_amt=dataentering.amounts("deposit",cash_in_hand,acc_type)
    deposit_amt=deposit_amt[0]
    match bool(deposit_amt):
        case True:
            query2="update {} set balance = balance+%s where acc_no = %s".format(acc_type)
            data2=(deposit_amt,acc_no)
            done2=dataentering.tableupdate(conn,cur,query2,data2)
            match done2:
                case True:
                    query3="update cash_in_hand set cash_in_hand = cash_in_hand-%s where acc_no = %s"
                    data3=(deposit_amt,acc_no)
                    done3=dataentering.tableupdate(conn,cur,query3,data3)
                    match done3:
                        case True:
                            print("Deposit of {} currency successful".format(deposit_amt))
                            print()
                        case False:
                            query2="update {} set balance = balance-%s where acc_no = %s".format(acc_type)
                            data2=(deposit_amt,acc_no)
                            done2=dataentering.tableupdate(conn,cur,query2,data2)
                            if done2:
                                print("Unable to subtract amount from cash_in_hand\n")
                case False:
                    print("Error while trying to add amount to balance.\n")
        case False:
            pass