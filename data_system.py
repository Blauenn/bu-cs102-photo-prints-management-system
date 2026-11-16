import csv

from constants import system_csv_location

# Populate data from CSV
def update_system_from_csv(system: list[list[str | int]]):
    system.clear()

    with open(system_csv_location, "r", newline="", encoding="utf-8") as file:
        system_csv = list(csv.reader(file))[1:]

    for row in system_csv:
        system_row = [row[0], int(row[1])]
        system.append(system_row)

def update_system(system: list[list[str | int]]):
    with open(system_csv_location, "w", newline="", encoding="utf-8") as file:
        system_csv = csv.writer(file)

        system_csv.writerow(["file", "autoincrement"])
        system_csv.writerows(system)
