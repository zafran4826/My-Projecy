import json
from abc import ABC, abstractmethod
import os

path = "Zafran/Products.json"
data = []

if os.path.exists(path):
    with open(path, "r") as f:
        data = json.load(f)

def save():
    with open(path, "w") as f:
        json.dump(data, f, indent = 4)


class Person(ABC):

    @abstractmethod
    def Register(self):
        pass

    @abstractmethod
    def Add_Product_To_Cart(self):
        pass

    @abstractmethod
    def Remove_Product_From_Cart(self):
        pass

    @abstractmethod
    def Show_Cart(self):
        pass

    @abstractmethod
    def Show_Orders(self):
        pass

    @staticmethod
    def email_check(email):
        if "@" in email and ".com" in email:
            return True
        else:
            return False

class Customer(Person):

    def Register(self):
        name = input("Enter Your Name :- ").title()
        email = input("Enter Your Email :- ")
        id_no = input("Enter Your ID Number :- ")
        cart = []

        for i in data:
            if i["id_no"] == id_no:
                print("Customer Already Exist..")
                return

        if not Person.email_check(email):
            print("Invalid Email..")
            return
        
        data.append({
            "name" : name,
            "email" : email,
            "id_no" : id_no,
            "cart" : []
                    })
        save()

    def Add_Product_To_Cart(self):
        id_no = input("Enter Your ID Number :-")
        product = input("Enter Product Name :- ").title()

        for i in data:
            if i["id_no"] == id_no:
                i["cart"].append(product)
                save()
                print("Product Added Successfully..")
            else:
                print("ID Number Not Matched..")
            break
        
    def Remove_Product_From_Cart(self):
        id_no = input("Enter Your ID Number :-")
        product = input("Enter Product Name :- ").title()

        for i in data:
            if i["id_no"] == id_no:
                if product in i["cart"]:
                    i["cart"].remove(product)
                    save()
                    print("Product Remove Successfully..")
                else:
                    print("Product Not in cart..")
                break
        else:
            print("ID Number Not Mathched..")

    def Show_Cart(self):
        id_no = input("Enter Your ID Number :-")

        for i in data:
            if i["id_no"] == id_no:
                print(f"Name : {i['name']}")
                print(f"Cart : {i['cart']}")
                break
        else:
            print("ID Number Not Matched..")

    def Show_Orders(self):
        for i in data:
            print(f"* Name  : {i['name']}")
            print(f"* Email : {i['email']}")
            print(f"* ID No : {i['id_no']}")
            print(f"* Cart  : {i['cart']}")
            print()

cust = Customer()
while True:
    print("Press 1 to add customer.")
    print("Press 2 to add product to cart.")
    print("Press 3 to remove product from cart.")
    print("Press 4 to show cart.")
    print("Press 5 to show orders.")
    print("Press 6 to exit.")

    try:
        choice = int(input("Enter your choice :- "))
    except ValueError:
        print("Only Numbers Allow..")
    else:
        print()
        if choice == 1:
            cust.Register()
        elif choice == 2:
            cust.Add_Product_To_Cart()
        elif choice == 3:
            cust.Remove_Product_From_Cart()
        elif choice == 4:
            cust.Show_Cart()
        elif choice == 5:
            cust.Show_Orders()
        elif choice == 6:
            print("Thanks to use our servise..")
            exit()
        else:
            print("Only (1-6) Numbers Are Allowed..")


