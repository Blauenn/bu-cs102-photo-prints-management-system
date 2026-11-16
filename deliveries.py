from constants import header_marker
from utils import clear_console

def manage_deliveries():
    while True:
        print(header_marker, "Manage deliveries", header_marker)
        print("1. View deliveries")
        print("2. Add delivery")
        print("3. Update delivery")
        print("4. Delete delivery")
        print("5. Return")

        menu = input("\nSelect a menu (1-5): ")
        print("\n")

        if menu == "5":
            clear_console(True)
            break
        else:
            print("Invalid menu!")
            continue

