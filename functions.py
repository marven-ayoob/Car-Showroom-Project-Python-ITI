from time import sleep
from branches import Branch
import yaml


def generate_constants(config_path: str, output_path: str = "constants.py"):
    """Reads a YAML config file and writes the extracted constants to constants.py."""

    with open(config_path, "r") as file:
        config = yaml.safe_load(file)

    constants = {
        "_DB_HOST": config.get("_DB_HOST", ""),
        "_DB_USER": config.get("_DB_USER", ""),
        "_DB_PASSWORD": config.get("_DB_PASSWORD", ""),
        "_DB_NAME": config.get("_DB_NAME", ""),
        "_FIRST_BRANCH": config.get("_FIRST_BRANCH", ""),
    }

    with open(output_path, "w") as file:
        for key, value in constants.items():
            file.write(f'{key} = "{value}"\n')

def welcome_message():
    """Prints a welcome message."""
    print("===================================")
    print("Welcome to the Car Showroom System ")
    print("===================================")

def create_branch(branch_input=None):
    if branch_input is None:
        branch_input = input("Enter new branch name: ")  # Get user input
    temp_obj = Branch(branch_input)  # Create Branch object
    return branch_input, temp_obj  # Return both values

def main_menu():
    while True:
        choice = int(input("1️⃣ Log in\n2️⃣ Exit\nChoice: "))
        if choice==1:
            break
        elif choice==2:
            exit(0)
        else:
            print("\nIncorrect choice, please try again!\n")


def main_login(branch_obj):
    while True:
        main_menu()
        print("Please input the following to login:\n")
        username=input("Username: ")
        password=input("Password: ")

        result = branch_obj.check_user(username, password)
        # print(f"RESULT IN FUNCTIONS FILE: {result} length: {len(result)}")
        username=result[0]
        priv=result[1]

        if username!='none':
            while True:
                choice, _ = display_menu(username, priv)
                branch = result[2]

                if priv == "admin":
                    match choice:
                        case "1": #creates user
                            print("Please input the following info: \n")
                            first_name=input("first name: ")
                            last_name = input("last name: ")
                            username = input("username: ")
                            password = input("password: ")
                            privilege = input("privilege: ")
                            branch = input("branch: ")

                            branch_obj.new_user_exists(first_name, last_name, username, password, privilege, branch)
                        case "2": #deletes car
                            branch_obj.purchase_car(branch, "delete")
                        case "3": #add car
                            branch = input("Enter branch: ")
                            brand = input("Enter car brand: ")
                            model = input("Enter car model: ")
                            car_type = input("Enter car type: ")
                            color = input("Enter car color: ")
                            price = float(input("Enter car price: "))
                            branch_obj.add_car(branch, brand, model, car_type, color, price)
                        case "4": #view all cars in all branches
                            branch_obj.list_all_branch_cars()

                        case "5":
                            create_branch()
                        case "6": #sign out
                            print(f"Signing out.. Goodbye {username}!\n")
                            sleep(3)
                            break
                        case _:
                            print("Invalid choice. Please try again.")

                elif priv == "manager":
                    match choice:
                        case "1": #sell car
                            branch_obj.purchase_car(branch, "purchase")

                        case "2": #search car
                            branch_obj.search_car_model(branch)

                        case "3": #view all cars in all branches
                            branch_obj.list_all_branch_cars()

                        case "4":#sales
                            branch_obj.get_branch_sales(branch)

                        case "5":#sign out
                            print(f"Signing out.. Goodbye {username}!\n")
                            sleep(3)
                            break

                        case _:
                            print("Invalid choice. Please try again.")

                elif priv == "agent":
                    match choice:
                        case "1": #sell car
                            branch_obj.purchase_car(branch, "purchase")

                        case "2": #search car
                            branch_obj.search_car_model(branch)

                        case "3":#sign out
                            print(f"Signing out.. Goodbye {username}!\n")
                            sleep(3)
                            break

                        case _:
                            print("Invalid choice. Please try again.")

        else:
            print("Wrong username or password, please try again!")


def display_menu(username, priv):  # """Displays menu options based on user role."""

    if priv == "admin":
        print("\nAdmin Menu:")
        print("1️⃣ Create User")
        print("2️⃣ Delete Car")
        print("3️⃣ Add Car")
        print("4️⃣ Search Car")
        print("5️⃣ Create Branch")
        print("6️⃣ Log Out")
    elif priv == "manager":
        print("\nManager Menu:")
        print("1️⃣ Sell Car")
        print("2️⃣ Find Car")
        print("3️⃣ Check All Branches")
        print("4️⃣ Sales")
        print("5️⃣ Log Out")
    elif priv == "agent":
        print("\nAgent Menu:")
        print("1️⃣ Sell Car")
        print("2️⃣ Find Car")
        print("3️⃣ Log Out")

    choice= (input("Please input choice: "))
    return (choice, priv)