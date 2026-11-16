import csv

from constants import header_marker, system_csv_location, customers_csv_location
from utils import clear_console

customers = []

def manage_customers():
    while True:
        print(header_marker, "Manage customers", header_marker)
        print("1. View customers")
        print("2. Add customer")
        print("3. Update customer")
        print("4. Delete customer")
        print("5. Return")

        menu = input("\nSelect a menu (1-5): ")
        print("\n")
    
        if menu == "1":
            global customers

            customers = []

            print(header_marker, "Customers list", header_marker)
            print(f"{'ID':<4}{'Name':<20}{'Phone':<10}")
            
            with open(customers_csv_location, "r", newline="", encoding="utf-8") as file:
                customers_csv = csv.reader(file)
                next(customers_csv, None) # Skip header 

                for customer in customers_csv:
                    customers.append(customer)

                for row in customers:
                    print(f"{row[0]:<4}{row[1]:<20}{row[2]:10}")
                print(f"End of list - {len(customers)} customer(s)\n")

            clear_console()

        elif menu == "2":
            print(header_marker, "Add customer", header_marker)
            customer_name = input("Customer name: ")
            
            while True:
                customer_phone = input("Phone number: ")
                
                if len(customer_phone) == 10:
                    break
                else:
                    print("The phone number has be 10 digits in length.")
                    continue

            print(f"Customer name: {customer_name}")
            print(f"Customer phone: {customer_phone}")

            clear_console()

        elif menu == "3":
            print(header_marker, "Update customer", header_marker)

            customer_id = input("Select a customer to update: ")

            # Find customer

            old_name = "CUSTOMER NAME"
            old_phone = "1234567890"

            new_name = input(f"Update customer name [{old_name}]: ") or old_name

            while True:
                new_phone = input(f"Update customer phone [{old_phone}]: ") or old_phone

                if len(new_phone) != 10:
                    print("The phone number has be 10 digits in length.")
                    continue
                else:
                    break

            # UPDATE customers SET name = {new_name}, phone = {new_phone} WHERE customer_id = {customer_id}
            print(f"\nCustomer {customer_id} - {old_name} has been updated")

            clear_console()

        elif menu == "4":
            print(header_marker, "Delete customer", header_marker)

            customer_id = input("Select a customer to delete: ")

            # Find customer

            # If found, set customer_name as the name...
            # and then delete.
            customer_name = "CUSTOMER_NAME"

            # DELETE from customers WHERE customer_id = {customer_id}

            print(f"Customer {customer_id} - {customer_name} has been deleted")

            clear_console()

        elif menu == "5":
            clear_console(True)

            break
        else:
            print("Invalid menu!")
            continue
