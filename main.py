header_marker = "=" * 15

while True:
    print(header_marker, "Photo Prints Management System", header_marker)
    print("1. Customers")
    print("2. Photos")
    print("3. Prints")
    print("4. Deliveries")
    print("5. Exit program")
    
    try:
        menu = int(input("\nSelect a menu (1-5): "))
    except ValueError:
        print("Please enter a number.")
        continue

    # Valid menu
    if not 1 <= menu <= 5:
        print("Please select a number between 1 and 5.")
        continue

    if menu == 1:
        print(header_marker, "Manage customers", header_marker)
    elif menu == 2:
        print(header_marker, "Manage photos", header_marker)
    elif menu == 3:
        print(header_marker, "Manage prints", header_marker)
    elif menu == 4:
        print(header_marker, "Manage deliveries", header_marker)
    elif menu == 5:
        break

print(header_marker, "Program exited", header_marker)
