from constants import header_marker
from utils import clear_console

from customers import manage_customers
from photos import manage_photos
from prints import manage_prints
from deliveries import manage_deliveries

while True:
    print(header_marker, "Photo Prints Management System", header_marker)
    print("1. Customers")
    print("2. Photos")
    print("3. Prints")
    print("4. Deliveries")
    print("5. Exit program")

    menu = input("\nSelect a menu (1-5): ")

    # Valid menu
    if menu == "1":
        clear_console(True)
        manage_customers()
    elif menu == "2":
        clear_console(True)
        manage_photos()
    elif menu == "3":
        clear_console(True)
        manage_prints()
    elif menu == "4":
        clear_console(True)
        manage_deliveries()
    elif menu == "5":
        break
    else:
        print("Invalid input!")
        clear_console()
        continue

print("\n")
print(header_marker, "Program exited", header_marker)
