import csv
from os import truncate
from os.path import join

from constants import header_marker, system_csv_location, customers_csv_location
from utils import clear_console, format_phone_number, truncate_string

from data_system import update_system, update_system_from_csv

# Global list so functions can access it
system = []
customers = []

# Populate system data
def update_customers_from_csv():
    customers.clear()

    with open(customers_csv_location, "r", newline="", encoding="utf-8") as file:
        customers_csv = list(csv.reader(file))[1:]

    for row in customers_csv:
        customer_to_append = [int(row[0]), row[1], row[2]]
        customers.append(customer_to_append)

update_system_from_csv(system)
update_customers_from_csv()

def find_customer(customer_id: int) -> list[str | int] | None:
    # Look through all row in customers
    for customer in customers:
        if int(customer[0]) == customer_id:
            # If customer is found
            return customer

    # If customer is not found
    return None

def get_customer_name(customer_id: int) -> str | None:
    found_customer = find_customer(customer_id)

    if found_customer:
        return str(found_customer[1]) 

    return None

def get_customers_list() -> str:
    return_list = []
    for customer in customers:
        customer_string = f"({customer[0]}) {customer[1]}"
        return_list.append(customer_string)

    return f"{" | ".join(return_list)}\n" 

### CRUD FUNCTIONS ###

def add_customer(name: str, phone: str) -> str:
    # autoincrement value of customers
    customer_id = system[0][1]

    with open(customers_csv_location, "a", newline="", encoding="utf-8") as file:
        customers_csv = csv.writer(file)

        customers_csv.writerow([customer_id, name, phone])

    # Add the new customer to the global list
    customers.append([customer_id, name, phone])

    # Update the autoincrement value
    for row in system:
        if row[0] == "customers":
            customer_id = row[1]
            row[1] += 1
            break

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

def manage_customers() -> None:
    while True:
        try:
            print(header_marker, "👤 Manage customers", header_marker)
            print("1. 📋 View customers")
            print("2. 🟩 Add customer")
            print("3. 🟡 Update customer")
            print("4. 🗑️ Delete customer")
            print("5. ⏪ Return")

            menu = input("\nSelect a menu (1-5): ")
            print("\n")

            # VIEW CUSTOMERS
            if menu == "1":
                clear_console(True)
                print(header_marker, "📋 Customers list", header_marker)
                print(f"{'ID':<4}"
                      f"{'Name':<20}"
                      f"{'Phone':<10}"
                      )

                for customer in customers:
                    customer_name = customer[1]
                    customer_name = truncate_string(customer_name, 17)

                    print(f"{customer[0]:<4}"
                          f"{customer_name:<20}"
                          f"{format_phone_number(customer[2]):<10}"
                          )

                clear_console()

            # ADD CUSTOMER
            elif menu == "2":
                clear_console(True)
                print(header_marker, "🟩 Add customer", header_marker)

                # Validate name
                while True:
                    customer_name = input("Customer name: ").strip()

                    if customer_name:
                        break
                    else:
                        print("❌ Customer name cannot be empty.\n")
                
                # Validate phone
                while True:
                    customer_phone = input("Phone number: ").replace("-", "").strip()
                    
                    if len(customer_phone) == 10 and customer_phone.isdigit():
                        break
                    else:
                        print("❌ The phone number has be 10 digits in length.\n")
                        continue

                result = add_customer(customer_name, customer_phone)
                print(result)

                clear_console()

            # UPDATE CUSTOMER
            elif menu == "3":
                clear_console(True)
                print(header_marker, "🟡 Update customer", header_marker)
                print(f"\n{get_customers_list()}")

                # Validate ID
                while True:
                    customer_id = input("Select a customer to update (0 to cancel): ")

                    if customer_id == "0":
                        raise(KeyboardInterrupt)
                    
                    if customer_id.isdigit():
                        break
                    else:
                        print("❌ The ID must be a number.\n")
                        continue

                customer = find_customer(int(customer_id))

                if customer is None:
                    print("\n❌ Customer not found.")
                    clear_console()
                else:
                    old_name = str(customer[1]) 
                    old_phone = str(customer[2]) 

                    new_name = input(f"Update customer name [{old_name}]: ") or old_name

                    # Validate phone
                    while True:
                        new_phone = str(input(f"Update customer phone [{format_phone_number(old_phone)}]: ").replace("-", "").strip() or old_phone
) 
                        if len(new_phone) == 10 and new_phone.isdigit():
                            break
                        else:
                            print("The phone number has be 10 digits in length.\n")
                            continue

                    result = update_customer(int(customer_id), str(new_name), str(new_phone))
                    print(result)

                    clear_console()

            # DELETE CUSTOMER
            elif menu == "4":
                clear_console(True)
                print(header_marker, "🗑️ Delete customer", header_marker)
                print(f"\n{get_customers_list()}")

                # Validate ID
                while True:
                    customer_id = input("Select a customer to delete (0 to cancel): ")

                    if customer_id == "0":
                        raise(KeyboardInterrupt)

                    if customer_id.isdigit():
                        break
                    else:
                        print("❌ The ID must be a number.\n")
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
                print("❌ Invalid menu!")
                clear_console()
                continue

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            clear_console(True)
            continue
