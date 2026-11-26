import os

def clear_console(immediately: bool = False):
    if not immediately:
        input("\nPress any button to continue...")

    os.system("cls" if os.name == "nt" else "clear")

def truncate_string(string: str, max_length: int) -> str:
    if len(string) > max_length:
        return f"{string[:max_length - 3]}..."
    else:
        return string

def format_phone_number(phone_number: str) -> str:
    return f"{phone_number[:3]}-{phone_number[3:6]}-{phone_number[6:]}"
