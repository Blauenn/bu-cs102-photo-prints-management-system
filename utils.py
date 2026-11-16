import os

def clear_console(immediately: bool = False):
    if not immediately:
        input("\nPress any button to continue...")

    os.system("cls" if os.name == "nt" else "clear")
