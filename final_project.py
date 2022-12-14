import datetime
import os


# Get the current time
time = datetime.datetime.now()

# Print a greeting based on the time of day
if time.hour < 12:
    print("Good morning and welcome to Alpha Bank! How may we assist you today?")
elif time.hour < 18:
    print("Good afternoon and welcome to Alpha Bank! How may we assist you today?")
else:
    print("Good evening and welcome to Alpha Bank! How may we assist you today?")


def create_account():
    # Prompt the user to enter a username and password
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    # Create a new user account with balance 0
    user_account = {"username": username, "password": password, "balance": 0}

    # Save the user account to the accounts.txt file
    with open("accounts.txt", "a") as file:
        file.write(f"{username},{password},{user_account['balance']}\n")


def login():
    # Prompt the user to enter a username and password
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    # Check if the username and password are correct
    with open("accounts.txt", "r") as file:
        for line in file:
            user, passwd, balance = line.strip().split(",", maxsplit=2)
            if user == username and passwd == password:
                # If the user exists, return their account information
                return {"username": user, "password": passwd, "balance": int(balance)}

    # If the username and password are not correct, print an error message
    # and prompt the user to create an account or try again
    print("The username and password do not match any existing accounts.")
    print("Please choose one of the following options:")
    print("1. Try again")
    print("2. Create a new account")

    # Prompt the user to select an option
    option = input("Enter your choice: ")

    # If the user chose to try again, prompt them to log in again
    if option == "1":
        print("Please log in into your existing account.")
        return login()
    # If the user chose to create a new account, create a new account for them
    elif option == "2":
        print("Please create your new account.")
        create_account()

    # Prompt the user to log in again
    print("Login into your new account.")
    return login()


def check_balance(user_account):
    # Read the user's account information from the accounts.txt file
    with open("accounts.txt", "r") as file:
        for line in file:
            if not line.strip():
                # Skip empty lines
                continue
            user, passwd, balance = line.strip().split(",", maxsplit=2)
            if user == user_account["username"] and passwd == user_account["password"]:
                # If the user exists, return their account information
                user_account = {"username": user, "password": passwd, "balance": int(balance)}

    # Print the user's current balance
    print(f"Your balance is {user_account['balance']}€.")


def deposit(account):
    # Prompt the user to enter an amount to deposit
    amount = input("Enter the amount you want to deposit: ")

    # If the user did not enter a number, print an error message and return
    try:
        amount = int(amount)
    except ValueError:
        print("Please enter a valid number.")
        return

    # Add the amount to the user's balance
    account["balance"] += amount

    # Save the updated balance to the accounts.txt file
    with open("accounts.txt", "r") as file:
        lines = file.readlines()
    with open("accounts.txt", "w") as file:
        for line in lines:
            if line.startswith(account["username"]):
                file.write(f"{account['username']},{account['password']},{account['balance']}\n")
            else:
                file.write(line)

    # Print a confirmation message
    print(f"Your deposit of {amount}€ was successful.")


def withdraw(user_account):
    # Prompt the user to enter an amount to withdraw
    amount = input("Enter the amount you want to withdraw: ")

    # If the user did not enter a number, print an error message and return
    try:
        amount = int(amount)
    except ValueError:
        print("Please enter a valid number.")
        return

    # Check if the user has sufficient funds
    if user_account["balance"] < amount:
        print("Insufficient funds.")
        return

    # Subtract the amount from the user's balance
    user_account["balance"] -= amount

    # Save the updated balance to the accounts.txt file
    with open("accounts.txt", "r") as file:
        lines = file.readlines()
    with open("accounts.txt", "w") as file:
        for line in lines:
            if line.startswith(user_account["username"]):
                file.write(f"{user_account['username']},{user_account['password']},{user_account['balance']}\n")
            else:
                file.write(line)

    # Print a confirmation message
    print(f"Your withdrawal of {amount}€ was successful.")


def transfer(user_account):
    # Prompt the user to enter the username of the recipient
    recipient = input("Enter the username of the recipient: ")

    # Check if the recipient exists in the accounts.txt file
    with open("accounts.txt", "r") as file:
        for line in file:
            user, passwd, balance = line.strip().split(",", maxsplit=2)
            if user == recipient:
                # If the recipient exists, transfer the money
                break
        else:
            # If the recipient does not exist, print an error message
            # and return the user to the main menu
            print(f"User '{recipient}' does not exist.")
            return

    # Prompt the user to enter the amount to transfer
    amount = input("Enter the amount you want to transfer: ")

    # If the user did not enter a number print an error message and return
    try:
        amount = int(amount)
    except ValueError:
        print("Please enter a valid number.")
        return

    # Check if the user has enough money to make the transfer
    if user_account["balance"] < amount:
        print("You do not have sufficient funds to make this transfer.")
        return

    # Read the recipient's account information from the accounts.txt file
    with open("accounts.txt", "r") as file:
        for line in file:
            if not line.strip():
                # Skip empty lines
                continue
            user, passwd, balance = line.strip().split(",", maxsplit=2)
            if user == recipient:
                # If the recipient exists, transfer the money to their account
                recipient_account = {"username": user, "password": passwd, "balance": int(balance)}
                recipient_account["balance"] += amount
                user_account["balance"] -= amount

    # Save the updated balances to the accounts.txt file
    with open("accounts.txt", "r") as file:
        lines = file.readlines()
    with open("accounts.txt", "w") as file:
        for line in lines:
            if line.startswith(user_account["username"]):
                file.write(f"{user_account['username']},{user_account['password']},{user_account['balance']}\n")
            elif line.startswith(recipient_account["username"]):
                file.write(
                    f"{recipient_account['username']},{recipient_account['password']},{recipient_account['balance']}\n")
            else:
                file.write(line)

    # Print a message to let the user know that the transfer was successful
    print("The transfer was successful.")


def exit():
    # Quit the program
    print("Thank you for using Alpha bank. Hope to see you soon!")
    quit()


# Check if the accounts.txt file exists
if not os.path.exists("accounts.txt"):
    # If the file doesn't exist, create it
    with open("accounts.txt", "w") as file:
        pass

# Prompt the user to choose an option
while True:
    option = input("1. Create an account\n"
                   "2. Log in\n"
                   "3. Exit\n"
                   "Enter your choice: ")
    if option == "1":
        # If the user chooses to create an user account call the create account function
        create_account()
        print("Please login into your new account.")
    elif option == "2":
        # If the user chooses to log in, call the login function
        account = login()
        if account:
            # If the user successfully logs in show the login menu
            while True:
                option = input(
                    "1. Check your balance\n"
                    "2. Deposit money\n"
                    "3. Withdraw money\n"
                    "4. Transfer money\n"
                    "5. Log out\n")
                if option == "1":
                    # If the user chooses to check their balance, call the check balance function
                    check_balance(account)
                elif option == "2":
                    # If the user chooses to deposit money, call the deposit function
                    deposit(account)
                elif option == "3":
                    # If the user chooses to withdraw money, call the withdraw function
                    withdraw(account)
                elif option == "4":
                    # If the user chooses to transfer money, call the transfer function
                    transfer(account)
                elif option == "5":
                    # If the user chooses to log out, break out of the loop
                    break
    elif option == "3":
        # If the user chooses to exit, call the exit function
        exit()
