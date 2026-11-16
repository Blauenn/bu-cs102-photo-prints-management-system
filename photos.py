from constants import header_marker
from utils import clear_console

def manage_photos():
    while True:
        print(header_marker, "Manage photos", header_marker)
        print("1. View photos")
        print("2. Add photo")
        print("3. Update photo")
        print("4. Delete photo")
        print("5. Return")

        menu = input("\nSelect a menu (1-5): ")
        print("\n")

        if menu == "5":
            clear_console(True)
            break
        else:
            print("Invalid menu!")
            continue
