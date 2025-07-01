from colorama import Fore
import re

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:        
            if "wrong argument" in str(e):
                return f"{Fore.RED}One of the arguments is wrong.{Fore.RESET} Use '{Fore.GREEN}help{Fore.RESET}' for additional info."
            elif "name or phone" in str(e):
                return f"{Fore.RED}Name or phone was not provided.{Fore.RESET} Use '{Fore.GREEN}help{Fore.RESET}' for additional info."
            elif "already in contacts" in str(e):
                return f"{Fore.RED}Contact already exists.{Fore.RESET} Use '{Fore.GREEN}help{Fore.RESET}' for additional info."
            elif "no contacts" in str(e):
                return f"{Fore.RED}Contact list is empty.{Fore.RESET}"
            
        except KeyError:
            return f"{Fore.RED}Given username was not found in the contact list.{Fore.RESET}"
        except IndexError:
            return f"{Fore.RED}Too few arguments were given.{Fore.RESET} Use '{Fore.GREEN}help{Fore.RESET}' for additional info."
    return inner

def parse_input(user_input: str) -> tuple[str, list[str]]:
    cmd, *args = user_input.split(" ", 2)    
    return cmd, args

@input_error
def add_contact(args: list[str], contacts: dict[str, str]) -> str:
    if len(args) < 2:
        raise IndexError
    
    username = "".join(re.findall(r"[a-zA-Z]", args[0]))
    phone = "".join(re.findall(r"[+\d]", args[1]))

    if not (username.isalpha() or (phone.startswith("+") and phone[1:].isdigit()) or phone.isdigit()):
        raise ValueError("wrong argument")
    elif not username or not phone:
        raise ValueError("name or phone not given")
    elif username in contacts:
        raise ValueError("username already in contacts")
    else:
        contacts.update({username: phone})
        return f"{Fore.GREEN}Contact added.{Fore.RESET}"

@input_error
def change_contact(args: list[str], contacts: dict[str, str]) -> str:
    if len(args) < 2:
        raise IndexError
    
    username = args[0]
    phone = args[1].replace(" ", "")

    if not username or not phone:
        raise ValueError("name or phone not given")
    elif username[1:].isdigit() or phone.isalpha():
        raise ValueError("wrong argument")
    elif username not in contacts:
        raise KeyError
    else:
        contacts.update({username: phone})
        return f"{Fore.GREEN}Contact updated.{Fore.RESET}"

@input_error
def show_phone(args: list[str], contacts: dict[str, str]) -> str:
    if len(args) < 1:
        raise IndexError
    
    username = args[0]

    if username not in contacts:
        raise KeyError
    else:
        return f"{Fore.GREEN}{contacts.get(username)}{Fore.RESET}"

@input_error
def show_all(contacts: dict[str, str]) -> str:
    if contacts:
        heading_message = f"{Fore.YELLOW}Your contact list:{Fore.RESET}"
        contacts_list = [f"\n - {key}: {contacts.get(key)}" for key in contacts.keys()]
        final_list = [heading_message] + contacts_list
        return "".join(final_list)
    else:
        raise ValueError("no contacts")

#Task 4
def main():
    contact_dict = {} # username: phone_number
    print(f"{Fore.YELLOW}Welcome to the assistant bot!{Fore.RESET}")

    while True:
        user_input = input("Enter a command: ").strip().casefold()
        if len(user_input) < 1:
            print(f"{Fore.RED}Too few arguments were given.{Fore.RESET} Use '{Fore.GREEN}help{Fore.RESET}' for additional info.")
            continue
        
        command, args = parse_input(user_input)

        match command:
            case "hello":
                print(f"{Fore.YELLOW}How can I help you?{Fore.RESET}")
            case "add":
                print(add_contact(args, contacts=contact_dict))
            case "change":
                print(change_contact(args, contacts=contact_dict))
            case "phone":
                print(show_phone(args, contacts=contact_dict))
            case "all":
                print(show_all(contacts=contact_dict))
            case "close" | "exit":
                print(f"{Fore.YELLOW}Goodbye!{Fore.RESET}")
                break
            case "help":
                print(f"""
The following commands are available:
    * {Fore.GREEN + 'add [username] [phone_number]':<45}{Fore.RESET} - add a contact to the contact list
    * {Fore.GREEN + 'change [username] [new_phone_number]':<45}{Fore.RESET} - change an already existing contact
    * {Fore.GREEN + 'phone [username]':<45}{Fore.RESET} - get to know a phone number by the owner's username
    * {Fore.GREEN + 'all':<45}{Fore.RESET} - get all contacts from the contact list
    * {Fore.GREEN + 'exit':<45}{Fore.RESET} - close the program
    * {Fore.GREEN + 'close':<45}{Fore.RESET} - close the program""")
            case _:
                print(f"{Fore.RED}Unknown command was given.{Fore.RESET} Use '{Fore.GREEN}help{Fore.RESET}' for additional info.")


if __name__ == "__main__":
    main()