import csv

from constants import header_marker, system_csv_location, customers_csv_location
from utils import clear_console

from data_system import update_system, update_system_from_csv

# Global list so functions can access it
system = []
customers = []

# Populate system data
def update_customers_from_csv():
    with open(customers_csv_location, "r", newline="", encoding="utf-8") as file:
        customers_csv = list(csv.reader(file))[1:]

    for row in customers_csv:
        customers.append(row)

update_system_from_csv(system)
update_customers_from_csv()

def find_customer(customer_id: int) -> list[str] | None:
    # Look through all row in customers
    for customer in customers:
        if int(customer[0]) == customer_id:
            # If customer is found
            return customer

    # If customer is not found
    return None

def add_customer(name: str, phone: str) -> str:
    # autoincrement value of customers
    customer_id = system[0][1]

    with open(customers_csv_location, "a", newline="", encoding="utf-8") as file:
        customers_csv = csv.writer(file)

        customers_csv.writerow([customer_id, name, phone])

    # Add the new customer to the global list
    customers.append([customer_id, name, phone])

    # Update the autoincrement value
    system[0][1] = customer_id + 1
    update_system(system)

    return(f"\n✅ Customer {customer_id} - {name} has been added.")

def update_customer(customer_id: int, name: str, phone: str) -> str:
    # Update the value of a customer based on customer_id
    for customer in customers:
        if int(customer[0]) == customer_id:
            customer[1] = name
            customer[2] = phone

            # Replace everything in the CSV
            with open(customers_csv_location, "w", newline="", encoding="utf-8") as file:
                customers_csv = csv.writer(file)

                customers_csv.writerow(["customer_id", "name", "phone"])
                customers_csv.writerows(customers)

            return f"\n✅ Customer {customer_id} - {name} has been updated."

    return f"\n❌ Customer {customer_id} was not found."

def delete_customer(customer_id: int) -> str:
    # Remove a customer based on customer_id
    for customer in customers:
        if int(customer[0]) == customer_id:
            customer_name = customer[1]

            customers.remove(customer)

            # Replace the entire CSV
            with open(customers_csv_location, "w", newline="", encoding="utf-8") as file:
                customers_csv = csv.writer(file)

                customers_csv.writerow(["customer_id", "name", "phone"])
                customers_csv.writerows(customers)

            return f"\n✅ Customer {customer_id} - {customer_name} has been deleted."

    return f"\n❌ Customer {customer_id} was not found."

def manage_customers():
    while True:
        print(header_marker, "👤 Manage customers", header_marker)
        print("1. View customers")
        print("2. Add customer")
        print("3. Update customer")
        print("4. Delete customer")
        print("5. Return")

        menu = input("\nSelect a menu (1-5): ")
        print("\n")

        # VIEW CUSTOMERS
        if menu == "1":
            print(header_marker, "📋 Customers list", header_marker)
            print(f"{'ID':<4}{'Name':<20}{'Phone':<10}")

            for customer in customers:
                print(f"{customer[0]:<4}{customer[1]:<20}{customer[2]:<10}")

            clear_console()

        # ADD CUSTOMER
        elif menu == "2":
            print(header_marker, "🟩 Add customer", header_marker)
            customer_name = input("Customer name: ")
            
            # Validate phone
            while True:
                customer_phone = input("Phone number: ")
                
                if len(customer_phone) == 10 and customer_phone.isdigit():
                    break
                else:
                    print("The phone number has be 10 digits in length.")
                    continue

            result = add_customer(customer_name, customer_phone)
            print(result)

            clear_console()

        # UPDATE CUSTOMER
        elif menu == "3":
            print(header_marker, "🟡 Update customer", header_marker)

            # Validate ID
            while True:
                customer_id = input("Select a customer to update: ")
                
                if customer_id.isdigit():
                    break
                else:
                    print("The ID must be a number.")
                    continue

            customer = find_customer(int(customer_id))

            if customer is None:
                print("\n❌ Customer not found.")
                clear_console()
            else:
                old_name = customer[1]
                old_phone = customer[2]

                new_name = input(f"Update customer name [{old_name}]: ") or old_name

                # Validate phone
                while True:
                    new_phone = input(f"Update customer phone [{old_phone}]: ") or old_phone

                    if len(new_phone) == 10 and new_phone.isdigit():
                        break
                    else:
                        print("The phone number has be 10 digits in length.")
                        continue

                result = update_customer(int(customer_id), new_name, new_phone)
                print(result)

                clear_console()

        # DELETE CUSTOMER
        elif menu == "4":
            print(header_marker, "🗑️ Delete customer", header_marker)

            # Validate ID
            while True:
                customer_id = input("Select a customer to delete: ")

                if customer_id.isdigit():
                    break
                else:
                    print("The ID must be a number.")
                    continue

            result = delete_customer(int(customer_id))
            print(result)

            clear_console()

        # RETURN
        elif menu == "5":
            clear_console(True)
            break

        # INVALID MENU
        else:
            print("Invalid menu!")
            clear_console()
            continue
