from constants import header_marker
from utils import clear_console

def manage_prints():
    while True:
        print(header_marker, "Manage prints", header_marker)
        print("1. View prints")
        print("2. Add print")
        print("3. Update print")
        print("4. Delete print")
        print("5. Return")

        menu = input("\nSelect a menu (1-5): ")
        print("\n")

        if menu == "5":
            clear_console(True)
            break
        else:
            print("Invalid menu!")
            continue
