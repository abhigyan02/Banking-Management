from panels import adminpanel
from panels import employeepanel
from panels import clientpanel
import maskpass
def acctype(query,cur):
    while True:
        print("--------------Account Selector Menu--------------")
        print("1.Admin.")
        print("2.Employee.")
        print("3.Client.")
        print("Enter ~ to end process.")
        a=input("\nEnter your account type (Enter 1, 2 or 3):")
        
        match a:
            case '1':
                b = maskpass.askpass(prompt="\nEnter admin password:",mask='*')
                if b == "admin123":
                    adminpanel.ap(query, cur)
                else:
                    print("\nWrong password!\n")
            case '2':
                b = maskpass.askpass(prompt="\nEnter employee password:",mask='*')
                if b == "emp123":
                    employeepanel.ep(query, cur)
                else:
                    print("\nWrong password!\n")
            case '3':
                clientpanel.cp(query, cur)
            case '~':
                print("\nShutting down the program.")
                break
            case _:
                print("\nWrong input!")