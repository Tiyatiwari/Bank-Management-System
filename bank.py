import json
import random
import string
from pathlib import Path
from datetime import datetime




class Bank:

    dataBase = "data.json"
    data = []

    # Load existing data
    try:
        if Path(dataBase).exists():
            with open(dataBase, "r") as fs:
                data = json.load(fs)
        else:
            data = []

    except Exception as err:
        print(f"Error : {err}")

    # Save data
    @classmethod
    def __update(cls):

        with open(cls.dataBase, "w") as fs:
            json.dump(cls.data, fs, indent=4)

    # Generate account number
    @classmethod
    def __accountGenerate(cls):

        while True:

            alpha = random.choices(string.ascii_uppercase, k=3)
            num = random.choices(string.digits, k=3)
            spchar = random.choices("@#!*&", k=1)

            acc = alpha + num + spchar

            random.shuffle(acc)

            accountNo = "".join(acc)

            exists = any(
                user["accountNo"] == accountNo
                for user in cls.data
            )

            if not exists:
                return accountNo

    # Find user helper
    @classmethod
    def findUser(cls, accountNo, pin):

        for user in cls.data:

            if (
                user["accountNo"] == accountNo
                and user["pin"] == pin
            ):
                return user

        return None
    def login(self, accountNo, pin):

        user = Bank.findUser(accountNo, pin)

        if not user:
            return False, "invalid account number or pin"
        return True, user

    # Create account
    def createAccount(self, name, age, email, pin):

        if age < 18:
            return False, "Age must be 18+"

        if len(str(pin)) != 4:
            return False, "PIN must be 4 digits"

        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo": self.__accountGenerate(),
            "balance": 0,
            "transactions": []
        }

        Bank.data.append(info)

        Bank.__update()

        return True, info

    # Deposit money
    def depositMoney(self, accountNo, pin, amount):

        user = Bank.findUser(accountNo, pin)

        if not user:
            return False, "User not found"

        if amount <= 0:
            return False, "Amount must be positive"

        if amount > 10000:
            return False, "Deposit limit is 10000"

        user["balance"] += amount

        user["transactions"].append(
            {
                "type": "Deposit",
                "amount": amount,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

        Bank.__update()

        return True, f"{amount} deposited successfully"

    # Withdraw money
    def withdrawMoney(self, accountNo, pin, amount):

        user = Bank.findUser(accountNo, pin)

        if not user:
            return False, "User not found"

        if amount <= 0:
            return False, "Amount must be positive"

        if user["balance"] < amount:
            return False, "Insufficient balance"

        user["balance"] -= amount

        user["transactions"].append(
            {
                "type": "Withdraw",
                "amount": amount,
                "time": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

        Bank.__update()

        return True, f"{amount} withdrawn successfully"

    # Show details
    def showDetails(self, accountNo, pin):

        user = Bank.findUser(accountNo, pin)

        if not user:
            return False, "User not found"

        return True, user

    # Update details
    def updateDetails(
        self,
        accountNo,
        pin,
        name=None,
        email=None,
        newPin=None
    ):

        user = Bank.findUser(accountNo, pin)

        if not user:
            return False, "User not found"

        if name:
            user["name"] = name

        if email:
            user["email"] = email

        if newPin:

            if len(str(newPin)) != 4:
                return False, "PIN must be 4 digits"

            user["pin"] = str(newPin)

        Bank.__update()

        return True, "Details updated"

    # Delete account
    def deleteAccount(self, accountNo, pin):

        user = Bank.findUser(accountNo, pin)

        if not user:
            return False, "User not found"

        Bank.data.remove(user)

        Bank.__update()

        return True, "Account deleted"

    # Transaction history
    def transactionHistory(self, accountNo, pin):

        user = Bank.findUser(accountNo, pin)

        if not user:
            return False, "User not found"

        return True, user["transactions"]