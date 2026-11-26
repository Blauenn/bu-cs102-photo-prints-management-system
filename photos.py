import csv
from datetime import date
from typing import Tuple

from constants import header_marker, system_csv_location, photos_csv_location
from utils import clear_console, truncate_string

from data_system import update_system, update_system_from_csv

# Global lists
system = []
photos = []

# Populate system data
def update_photos_from_csv() -> None:
    photos.clear()

    with open(photos_csv_location, "r", newline="", encoding="utf-8") as file:
        photos_csv = list(csv.reader(file))[1:]

    for row in photos_csv:
        photo_to_append = [
            int(row[0]),
            int(row[1]),
            int(row[2]),
            row[3],
            row[4],
            row[5]
        ]

        photos.append(photo_to_append)

update_system_from_csv(system)
update_photos_from_csv()

def find_photo(photo_id: int) -> list[int | str] | None:
    for photo in photos:
        if photo[0] == photo_id:
            return photo

    return None

def get_photos_list() -> str:
    return_list = []
    for photo in photos:
        if photo[4] != "":
            description = photo[4]
        else:
            description = "No description"

        photo_string = f"({photo[0]}) {description}"
        return_list.append(photo_string)

    return f"{" | ".join(return_list)}\n"

### CRUD FUNCTIONS ###

def add_photo(width: int, height: int, photo_url: str, description: str, added_date: str) -> str:
    # Get the next available photo ID
    photo_id = None

    for row in system:
        if row[0] == "photos":
            photo_id = row[1]
            break

    if photo_id is None:
        return "Photo autoincrement entry not found."

    # Write to CSV
    with open(photos_csv_location, "a", newline="", encoding="utf-8") as file:
        photos_csv = csv.writer(file)
        photos_csv.writerow([photo_id, width, height, photo_url, description, added_date])

    # Update global list
    photos.append([photo_id, width, height, photo_url, description, added_date])

    # Increment photo ID
    for row in system:
        if row[0] == "photos":
            row[1] += 1
            break

    update_system(system)

    return f"✅ Photo {photo_id} has been added."

def update_photo(photo_id: int, width: int, height: int, photo_url: str, added_date: str) -> str:
    photo = find_photo(photo_id)

    if photo is None:
        return f"❌ Photo {photo_id} was not found."

    photo[1] = width
    photo[2] = height
    photo[3] = photo_url
    photo[4] = added_date

    save_photos()

    return f"✅ Photo {photo_id} has been updated."

def save_photos() -> None:
    with open(photos_csv_location, "w", newline="", encoding="utf-8") as file:
        photos_csv = csv.writer(file)

        photos_csv.writerow(["photo_id", "width", "height", "photo_url", "added_date"])
        photos_csv.writerows(photos)

def delete_photo(photo_id: int) -> str:
    photo = find_photo(photo_id)

    if photo is None:
        return f"❌ Photo {photo_id} was not found."

    photos.remove(photo)

    save_photos()

    return f"✅ Photo {photo_id} has been deleted."

def manage_photos() -> None:
    while True:
        try:
            print(header_marker, "🏞️ Manage photos", header_marker)
            print("1. 📋 View photos")
            print("2. 🟩 Add photo")
            print("3. 🟡 Update photo")
            print("4. 🗑️ Delete photo")
            print("5. ⏪ Return")

            menu = input("\nSelect a menu (1-5): ")
            print("\n")

            # VIEW PHOTOS
            if menu == "1":
                clear_console(True)
                print(header_marker, "📋 Photos list", header_marker)
                print(
                    f"{'ID':<6}"
                    f"{'Description':<20}"
                    f"{'Width':<10}"
                    f"{'Height':<10}"
                    f"{'Date':<15}"
                    f"{'URL'}"
                )

                for photo in photos:
                    description = photo[4]
                    description = truncate_string(description, 17)

                    if not description.strip():
                        description = "-"

                    print(
                            f"{photo[0]:<6}"
                            f"{description:<20}"
                            f"{photo[1]:<10}"
                            f"{photo[2]:<10}"
                            f"{photo[5]:<15}"
                            f"{photo[3]}"
                        )

                clear_console()

            # ADD PHOTO
            elif menu == "2":
                clear_console(True)
                print(header_marker, "🟩 Add photo", header_marker)

                while True:
                    width = input("Photo width: ")

                    if width.isdigit() and int(width) > 0:
                        break
                    else:
                        print("❌ Width must be a positive number.\n")

                while True:
                    height = input("Photo height: ")

                    if height.isdigit() and int(height) > 0:
                        break
                    else:
                        print("❌ Height must be a positive number.\n")

                photo_url = input("Photo URL: ")
                photo_description = input("Photo description: ")

                todays_date = date.today().isoformat()
                added_date = input(f"Date added [{todays_date}]: ") or todays_date 

                result = add_photo(int(width), int(height), photo_url, photo_description, added_date)
                print(f"{result}")

                clear_console()

            # UPDATE PHOTO
            elif menu == "3":
                clear_console(True)
                print(header_marker, "🟡 Update photo", header_marker)
                print(f"\n{get_photos_list()}")

                while True:
                    photo_id = input("Select a photo to update (0 to cancel): ")

                    if photo_id == "0":
                        raise(KeyboardInterrupt)

                    if photo_id.isdigit():
                        break
                    else:
                        print("❌ The ID must be a number.\n")

                photo = find_photo(int(photo_id))

                if photo is None:
                    print("\n❌ Photo not found.")
                    clear_console()
                else:
                    old_width = photo[1]
                    old_height = photo[2]
                    old_url = photo[3]
                    old_date = photo[4]

                    while True:
                        new_width = input(f"Update width [{old_width}]: ") or str(old_width)

                        if new_width.isdigit() and int(new_width) > 0:
                            break
                        else:
                            print("❌ Width must be a positive number.\n")

                    while True:
                        new_height = input(f"Update height [{old_height}]: ") or str(old_height)

                        if new_height.isdigit() and int(new_height) > 0:
                            break
                        else:
                            print("❌ Height must be a positive number.\n")

                    new_url = input(f"Update URL [{old_url}]: ") or old_url
                    new_date = input(f"Update date [{old_date}]: ") or str(old_date)

                    result = update_photo(
                        int(photo_id),
                        int(new_width),
                        int(new_height),
                        str(new_url),
                        str(new_date) 
                    )

                    print(f"\n{result}")
                    clear_console()

            # DELETE PHOTO
            elif menu == "4":
                clear_console(True)
                print(header_marker, "🗑️ Delete photo", header_marker)
                print(get_photos_list())

                while True:
                    photo_id = input("Select a photo to delete (0 to cancel): ")

                    if photo_id == "0":
                        raise(KeyboardInterrupt)

                    if photo_id.isdigit():
                        break
                    else:
                        print("❌ The ID must be a number.\n")

                result = delete_photo(int(photo_id))
                print(f"\n{result}")

                clear_console()

            # RETURN
            elif menu == "5":
                clear_console(True)
                break

            # INVALID MENU
            else:
                print("❌ Invalid menu!")
                clear_console()

        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            clear_console(True)
            continue
