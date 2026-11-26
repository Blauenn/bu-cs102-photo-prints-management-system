import csv
from datetime import date

from constants import header_marker, system_csv_location, deliveries_csv_location
from utils import clear_console

from data_system import update_system, update_system_from_csv
from prints import prints, find_print

# Global lists
system = []
deliveries = []


def update_deliveries_from_csv() -> None:
    deliveries.clear()

    with open(deliveries_csv_location, "r", newline="", encoding="utf-8") as file:
        deliveries_csv = list(csv.reader(file))[1:]

    for row in deliveries_csv:
        delivery_to_append = [
            int(row[0]),
            int(row[1]),
            row[2],
            row[3]
        ]

        deliveries.append(delivery_to_append)


update_system_from_csv(system)
update_deliveries_from_csv()

def find_delivery(delivery_id: int) -> list[int | str] | None:
    for delivery in deliveries:
        if delivery[0] == delivery_id:
            return delivery

    return None


def save_deliveries() -> None:
    with open(deliveries_csv_location, "w", newline="", encoding="utf-8") as file:
        deliveries_csv = csv.writer(file)

        deliveries_csv.writerow([
            "delivery_id",
            "print_id",
            "date_created",
            "date_delivered"
        ])

        deliveries_csv.writerows(deliveries)

def add_delivery(print_id: int, date_created: str) -> str:
    if find_print(print_id) is None:
        return f"Print {print_id} was not found."

    for delivery in deliveries:
        if delivery[1] == print_id:
            return f"Print {print_id} already has a delivery."

    delivery_id = None

    for row in system:
        if row[0] == "deliveries":
            delivery_id = int(row[1])
            break

    if delivery_id is None:
        return "Delivery autoincrement entry not found."

    new_delivery = [
        delivery_id,
        print_id,
        date_created,
        ""
    ]

    with open(deliveries_csv_location, "a", newline="", encoding="utf-8") as file:
        deliveries_csv = csv.writer(file)
        deliveries_csv.writerow(new_delivery)

    deliveries.append(new_delivery)

    for row in system:
        if row[0] == "deliveries":
            row[1] = int(row[1]) + 1
            break

    update_system(system)

    return f"Delivery {delivery_id} has been created."

def update_delivery(
    delivery_id: int,
    print_id: int,
    date_created: str,
    date_delivered: str
) -> str:

    delivery = find_delivery(delivery_id)

    if delivery is None:
        return f"Delivery {delivery_id} was not found."

    if find_print(print_id) is None:
        return f"Print {print_id} was not found."

    for other_delivery in deliveries:
        if other_delivery[0] != delivery_id and other_delivery[1] == print_id:
            return f"Print {print_id} already has a delivery."

    delivery[1] = print_id
    delivery[2] = date_created
    delivery[3] = date_delivered

    save_deliveries()

    return f"Delivery {delivery_id} has been updated."

def delete_delivery(delivery_id: int) -> str:
    delivery = find_delivery(delivery_id)

    if delivery is None:
        return f"Delivery {delivery_id} was not found."

    deliveries.remove(delivery)
    save_deliveries()

    return f"Delivery {delivery_id} has been deleted."

def manage_deliveries() -> None:
    while True:
        print(header_marker, "🚚 Manage deliveries", header_marker)
        print("1. View deliveries")
        print("2. Add delivery")
        print("3. Update delivery")
        print("4. Delete delivery")
        print("5. Return")

        menu = input("\nSelect a menu (1-5): ")
        print("\n")

        # VIEW DELIVERIES
        if menu == "1":
            print(header_marker, "📋 Deliveries list", header_marker)
            print(
                f"{'ID':<6}{'Print':<8}{'Created':<15}"
                f"{'Delivered':<15}{'Status'}"
            )

            for delivery in deliveries:
                status = "Delivered" if delivery[3] else "Pending"

                print(
                    f"{delivery[0]:<6}{delivery[1]:<8}"
                    f"{delivery[2]:<15}{delivery[3]:<15}"
                    f"{status}"
                )

            clear_console()

        # ADD DELIVERY
        elif menu == "2":
            print(header_marker, "🟩 Add delivery", header_marker)

            while True:
                print_id = input("Print ID: ")

                if print_id.isdigit() and find_print(int(print_id)) is not None:
                    break
                else:
                    print("Print not found. Enter an existing print ID.")

            date_created = input("Date created (YYYY-MM-DD): ") or date.today().isoformat()

            result = add_delivery(int(print_id), date_created)

            print(result)
            clear_console()

        # UPDATE DELIVERY
        elif menu == "3":
            print(header_marker, "🟡 Update delivery", header_marker)

            while True:
                delivery_id = input("Select a delivery to update: ")

                if delivery_id.isdigit():
                    break
                else:
                    print("The ID must be a number.")

            delivery = find_delivery(int(delivery_id))

            if delivery is None:
                print("\n❌ Delivery not found.")
                clear_console()

            else:
                old_print_id = delivery[1]
                old_date_created = delivery[2]
                old_date_delivered = delivery[3]

                while True:
                    new_print_id = input(
                        f"Update print ID [{old_print_id}]: "
                    ) or str(old_print_id)

                    if new_print_id.isdigit() and find_print(int(new_print_id)) is not None:
                        break
                    else:
                        print("Print not found. Enter an existing print ID.")

                new_date_created = input(
                    f"Update creation date [{old_date_created}]: "
                ) or str(old_date_created)

                new_date_delivered = input(
                    f"Update delivery date [{old_date_delivered or 'Not delivered'}] (0 to clear): "
                )
                
                if new_date_delivered == "0":
                    new_date_delivered = ""
                elif new_date_delivered == "":
                    new_date_delivered = str(old_date_delivered)

                result = update_delivery(
                    int(delivery_id),
                    int(new_print_id),
                    new_date_created,
                    new_date_delivered
                )

                print(result)
                clear_console()

        # DELETE DELIVERY
        elif menu == "4":
            print(header_marker, "🗑️ Delete delivery", header_marker)

            while True:
                delivery_id = input("Select a delivery to delete: ")

                if delivery_id.isdigit():
                    break
                else:
                    print("The ID must be a number.")

            result = delete_delivery(int(delivery_id))

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
