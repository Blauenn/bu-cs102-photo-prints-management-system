header_marker = "=" * 15

print(header_marker, "Photo Prints Management System", header_marker)
print("1. Customers")
print("2. Images")
print("3. Prints")
print("4. Deliveries")
print("5. Exit program")

menu_1 = int(input("\nSelect a menu (1-5): "))

while True:
    if (menu_1 == 5):
        break
    else:
        print("Hey!")
        break

print(header_marker, "Program exitted", header_marker)
