import csv
from datetime import date

from constants import header_marker, system_csv_location, prints_csv_location
from photos import find_photo, get_photos_list
from utils import clear_console
from data_system import update_system, update_system_from_csv

from customers import customers, find_customer, get_customer_name, get_customers_list

# Global lists
system = []
prints = []

def update_prints_from_csv() -> None:
    prints.clear()

    with open(prints_csv_location, "r", newline="", encoding="utf-8") as file:
        prints_csv = list(csv.reader(file))[1:]

    for row in prints_csv:
        print_to_append = [
            int(row[0]),  # prints_id
            int(row[1]),  # photo_id
            int(row[2]),  # customer_id
            row[3],       # paper_size
            row[4],       # paper_type
            int(row[5]),  # amount
            row[6]        # print_date
        ]

        prints.append(print_to_append)


update_system_from_csv(system)
update_prints_from_csv()

def find_print(prints_id: int) -> list[int | str] | None:
    for print_record in prints:
        if print_record[0] == prints_id:
            return print_record

    return None

def get_prints_list() -> str:
    return_list = []
    for print_record in prints:
        found_photo = find_photo(print_record[1])

        if found_photo:
            description = str(found_photo[4]).strip()

            if not description:
                description = "Photo"
            
            photo_string = description 
        else:
            photo_string = "Photo not found."

        prints_string = f"({print_record[0]}) {photo_string} from {get_customer_name(print_record[2])}"
        return_list.append(prints_string)

    return f"{", ".join(return_list)}\n" 

def save_prints() -> None:
    with open(prints_csv_location, "w", newline="", encoding="utf-8") as file:
        prints_csv = csv.writer(file)

        prints_csv.writerow([
            "prints_id",
            "photo_id",
            "customer_id",
            "paper_size",
            "paper_type",
            "amount",
            "print_date"
        ])

        prints_csv.writerows(prints)

def add_print(
    photo_id: int,
    customer_id: int,
    paper_size: str,
    paper_type: str,
    amount: int,
    print_date: str
) -> str:

    if find_photo(photo_id) is None:
        return f"Photo {photo_id} was not found."

    if find_customer(customer_id) is None:
        return f"Customer {customer_id} was not found."

    prints_id = None

    for row in system:
        if row[0] == "prints":
            prints_id = int(row[1])
            break

    if prints_id is None:
        return "Print autoincrement entry not found."

    new_print = [
        prints_id,
        photo_id,
        customer_id,
        paper_size,
        paper_type,
        amount,
        print_date
    ]

    with open(prints_csv_location, "a", newline="", encoding="utf-8") as file:
        prints_csv = csv.writer(file)
        prints_csv.writerow(new_print)

    prints.append(new_print)

    for row in system:
        if row[0] == "prints":
            row[1] = int(row[1]) + 1
            break

    update_system(system)

    return f"Print {prints_id} has been added."

def update_print(
    prints_id: int,
    photo_id: int,
    customer_id: int,
    paper_size: str,
    paper_type: str,
    amount: int,
    print_date: str
) -> str:

    print_record = find_print(prints_id)

    if print_record is None:
        return f"Print {prints_id} was not found."

    if find_photo(photo_id) is None:
        return f"Photo {photo_id} was not found."

    if find_customer(customer_id) is None:
        return f"Customer {customer_id} was not found."

    print_record[1] = photo_id
    print_record[2] = customer_id
    print_record[3] = paper_size
    print_record[4] = paper_type
    print_record[5] = amount
    print_record[6] = print_date

    save_prints()

    return f"Print {prints_id} has been updated."

def delete_print(prints_id: int) -> str:
    print_record = find_print(prints_id)

    if print_record is None:
        return f"Print {prints_id} was not found."

    prints.remove(print_record)
    save_prints()

    return f"Print {prints_id} has been deleted."

def manage_prints() -> None:
    while True:
        try:
            print(header_marker, "🖨️ Manage prints", header_marker)
            print("1. View prints")
            print("2. Add print")
            print("3. Update print")
            print("4. Delete print")
            print("5. Return")

            menu = input("\nSelect a menu (1-5): ")
            print("\n")

            # VIEW PRINTS
            if menu == "1":
                clear_console(True)
                print(header_marker, "📋 Prints list", header_marker)
                print(
                    f"{'ID':<6}"
                    f"{'Photo':<20}"
                    f"{'Customer':<20}"
                    f"{'Size':<8}"
                    f"{'Paper':<10}"
                    f"{'Amount':<9}"
                    f"{'Date'}"
                )

                for print_record in prints:
                    found_photo = find_photo(print_record[1])
                    if found_photo:
                        photo_description = str(found_photo[4]) 
                        
                        if not photo_description.strip():
                            photo_description = "Photo"
                    else:
                        photo_description = "DELETED PHOTO"

                    if len(photo_description) > 17:
                       photo_description = photo_description[:14] + "..." 

                    customer_name = get_customer_name(print_record[2])
                    if customer_name:
                        customer_name = str(customer_name.strip())
                    else:
                        customer_name = "DELETED CUSTOMER"

                    if len(customer_name) > 17:
                       customer_name = customer_name[:14] + "..." 

                    print(
                        f"{print_record[0]:<6}"
                        f"{photo_description:<20}"
                        f"{customer_name:<20}"
                        f"{print_record[3]:<8}"
                        f"{print_record[4]:<10}"
                        f"{print_record[5]:<9}"
                        f"{print_record[6]}"
                    )

                clear_console()

            # ADD PRINT
            elif menu == "2":
                clear_console(True)
                print(header_marker, "🟩 Add print", header_marker)

                # Validate photo ID
                while True:
                    print("\nPhoto ID:")
                    print(get_photos_list())
                    photo_id = input("Photo ID: ")

                    if photo_id.isdigit() and find_photo(int(photo_id)) is not None:
                        break
                    else:
                        print("Photo not found. Please enter an existing photo ID.\n")

                # Validate customer ID
                while True:
                    print("\nCustomer ID:")
                    print(get_customers_list())
                    customer_id = input("Customer ID: ")

                    if customer_id.isdigit() and find_customer(int(customer_id)) is not None:
                        break
                    else:
                        print("Customer not found. Please enter an existing customer ID.\n")

                # Validate paper size
                while True:
                    paper_size = input("Paper size (A3/A4/4x6/2x3): ").upper()

                    if paper_size in ["A3", "A4", "4X6", "2X3"]:
                        break
                    else:
                        print("Invalid paper size.\n")

                # Validate paper type
                while True:
                    paper_type = input("Paper type (Matte/Satin): ").capitalize()

                    if paper_type in ["Matte", "Satin"]:
                        break
                    else:
                        print("Invalid paper type.\n")

                # Validate amount
                while True:
                    amount = input("Amount: ")

                    if amount.isdigit() and int(amount) > 0:
                        break
                    else:
                        print("Amount must be a positive number.\n")

                todays_date = date.today().isoformat()
                print_date = input(f"Print date [{todays_date}]: ") or todays_date 

                result = add_print(
                    int(photo_id),
                    int(customer_id),
                    paper_size,
                    paper_type,
                    int(amount),
                    print_date
                )

                print(result)
                clear_console()

            # UPDATE PRINT
            elif menu == "3":
                clear_console(True)
                print(header_marker, "🟡 Update print", header_marker)
                print(f"\n{print_prints_list()}")

                while True:
                    prints_id = input("Select a print to update (0 to cancel): ")
                    
                    if prints_id == "0":
                        raise(KeyboardInterrupt)

                    if prints_id.isdigit():
                        break
                    else:
                        print("The ID must be a number.\n")

                print_record = find_print(int(prints_id))

                if print_record is None:
                    print("\n❌ Print not found.")
                    clear_console()

                else:
                    old_photo_id = print_record[1]
                    old_customer_id = print_record[2]
                    old_paper_size = print_record[3]
                    old_paper_type = print_record[4]
                    old_amount = print_record[5]
                    old_date = print_record[6]

                    # Validate photo ID
                    while True:
                        new_photo_id = input(f"Update photo ID [{old_photo_id}]: ") or str(old_photo_id)

                        if new_photo_id.isdigit() and find_photo(int(new_photo_id)) is not None:
                            break
                        else:
                            print("Photo not found. Please enter an existing photo ID.\n")

                    # Validate customer ID
                    while True:
                        new_customer_id = input(f"Update customer ID [{old_customer_id}]: ") or str(old_customer_id)

                        if new_customer_id.isdigit() and find_customer(int(new_customer_id)) is not None:
                            break
                        else:
                            print("Customer not found. Please enter an existing customer ID.\n")

                    # Validate paper size
                    while True:
                        new_paper_size = input(f"Update paper size [{old_paper_size}]: ").upper() or old_paper_size

                        if new_paper_size in ["A3", "A4", "4X6", "2X3"]:
                            break
                        else:
                            print("Invalid paper size.\n")

                    # Validate paper type
                    while True:
                        new_paper_type = input(f"Update paper type [{old_paper_type}]: ").capitalize() or old_paper_type

                        if new_paper_type in ["Matte", "Satin"]:
                            break
                        else:
                            print("Invalid paper type.\n")

                    # Validate amount
                    while True:
                        new_amount = input(f"Update amount [{old_amount}]: ") or str(old_amount)

                        if new_amount.isdigit() and int(new_amount) > 0:
                            break
                        else:
                            print("Amount must be a positive number.\n")

                    new_date = input(f"Update print date [{old_date}]: ") or str(old_date)

                    result = update_print(
                        int(prints_id),
                        int(new_photo_id),
                        int(new_customer_id),
                        new_paper_size,
                        new_paper_type,
                        int(new_amount),
                        new_date
                    )

                    print(result)
                    clear_console()

            # DELETE PRINT
            elif menu == "4":
                clear_console(True)
                print(header_marker, "🗑️ Delete print", header_marker)
                print(f"\n{print_prints_list()}")

                while True:
                    prints_id = input("Select a print to delete (0 to cancel): ")

                    if prints_id == "0":
                        raise(KeyboardInterrupt)

                    if prints_id.isdigit():
                        break
                    else:
                        print("The ID must be a number.\n")

                result = delete_print(int(prints_id))

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
        
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            clear_console(True)
            continue
