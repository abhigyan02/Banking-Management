from initialization import setup
from initialization import check
from panels import accounttype
from tools import connection
while True:
    print("1.Continue")
    print("2.Quit")
    a=input("Enter your choice(1,2): ")
    match a:
            case "1":
                if not check.check():
                    query, cur = connection.cc()
                    accounttype.acctype(query, cur)
                    break
                else:
                    setup.setup()
            case "2":
                print("Shutting down the program")
                break
            case _:
                print("Wrong input.")
            