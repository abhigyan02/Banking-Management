def cp7(conn,cur,acc_no):
    cash_in_hand=int(input("Enter the cash in your hand:"))
    cur.execute(f'UPDATE cash_in_hand set cash_in_hand={cash_in_hand} where acc_no={acc_no}')