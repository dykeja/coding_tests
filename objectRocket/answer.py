#

import os
import sys
import argparse
import copy

DEBUG=True


class Item:
    """
    Class to encapsulate the different items that we can sell
    """
    def __init__(self, code, name, price):
        self.code = code
        self.name = name
        self.price = price
        self.disprice = 0
        self.discount = None

ITEMS = {}
ITEMS["ch1"] = Item("CH1", "Chai", 3.11)
ITEMS["ap1"] = Item("AP1", "Apples", 6.00)
ITEMS["cf1"] = Item("CF1", "Coffee", 11.23)
ITEMS["mk1"] = Item("MK1", "Milk", 4.75)
ITEMS["om1"] = Item("OM1", "Oatmeal", 3.69)

MODES= {"add": "Add a new item to the cart",
#        "remove": "Remove an item from the cart",
        "total": "Print the current cart",
        "checkout": "Clear the cart",
        "discounts": "Show all discounts",
        "quit": "Quit the application"}

DISCOUNTS = {"bogo": "Buy One Get One Free Coffee",
             "appl": "Apple price drops to $4.50 after buying 3 or more bags of apples",
             "chmk": "Purchase a box of Chai and get milk free. (Limit 1)",
             "apom": "Purchase a bag of Oatmeal and get 50% off a bag of Apples"}

def decho(value):
    if DEBUG:
        print(value)

def printItems():
    for x in ITEMS.keys():
        print("%s: code: %s, price: %.2f" %(ITEMS[x].name, ITEMS[x].code, ITEMS[x].price))

class Cart(object):
    def __init__(self):
        self.itemList = []
        self.apple_count = 0
        self.freecoffee = False
        self.freemilk = False
        self.fm_used = False
        self.fifty_apple = False

    def check_discounts(self, data, i):
        """
        Utility function to check the discounts for the item passed in
        """
        # Apples are basically a raw count for the discount, so just increment a counter
        if data == "ap1":
            self.apple_count +=1
            if self.fifty_apple:
                i.discount = "apom"
                i.disprice = -3

        # OK, we have 3, so now set all the discounted prices
        if self.apple_count == 3:
            for x in self.itemList:
                if x.code.lower() == "ap1" and not x.discount:
                    x.discount = "appl"
                    x.disprice = -1.5

        # So anything greater than 2 needs to just update the object in the list
        if self.apple_count > 2 and data=="ap1":
            i.discount = "appl"
            i.disprice = -1.5

        # Now check for any coffee
        if data == "cf1":

            # We have already gotten one coffee, this one is free
            if self.freecoffee:
                i.disprice = -11.23
                i.discount = "bogo"
                self.freecoffee = False

            else:
                self.freecoffee = True

        # Now check to see if we have free milk
        if data == "ch1" and not self.freemilk and not self.fm_used:
            self.freemilk = True
            milk = False

            # check to see if we had already gotten a milk in there
            for x in self.itemList:
                if x.code.lower() == "mk1":
                    x.discount = "chmk"
                    x.disprice = -4.75
                    self.freemilk = False
                    self.fm_used = True

        # No milk in the cart already, time to just add it in
        if data == "mk1" and self.freemilk and not self.fm_used:
            self.freemilk = False
            self.fm_used = True
            i.disprice = -4.75
            i.discount = "chmk"

        # Now check for the Oatmeal
        if data == "om1":

            # Hey there's an apple in here
            if self.apple_count != 0:

                # Find it and update it
                for x in self.itemList:
                    if x.code.lower() == "ap1":
                        x.discount = "apom"
                        x.disprice = -3
                        break
            else:
                self.fifty_apple = True

    def addItem(self):
        while True:
            print ("Please select the item code from the list below")
            printItems()
            data = input().lower()

            try:
                i = copy.deepcopy(ITEMS[data])
                print(i)
            except KeyError:
                print("Not a valid item: %s" %data)
                continue

            break
        self.check_discounts(data, i)
        self.itemList.append(i)

    def Total(self):
        """ Utility function to print out the total price of the cart """
        out="Item\t\tPrice\n"
        out+="----\t\t-----\n"
        price = 0

        for x in self.itemList:
            out+="%s\t\t%.2f\n" %(x.code, ITEMS[x.code.lower()].price)
            price= price + x.price + x.disprice

            if x.discount:
                out+="    \t%s\t%.2f\n" %(x.discount.upper(), x.disprice)
            

        out+="---------------------\n"
        out+="    \t\t%.2f\n" %(price)

        print(out)
        

def displayMenu():
    """
    Utility function to print out the menu
    """
    print("Please enter what mode to use, all entries are case insensitive")
    print("Modes:")
    for x in MODES.keys():
        print("\t%s: %s" %(x, MODES[x]))

    mode = input()
    decho ("Mode: '%s'" %mode)
    return mode.lower()


if __name__ == "__main__":
    cart = Cart()
    while True:
        mode = displayMenu()

        # First check for time to quit
        if mode == "quit":
            break

        if mode == "add":
            cart.addItem()
            continue

        if mode == "total":
            cart.Total()
            continue

        if mode == "checkout":
            cart.Total()
            del cart
            cart = Cart()
            continue

        if mode == "discounts":
            print ("Available discounts:")
            for x in DISCOUNTS.keys():
                print ("\t%s: %s" %(x, DISCOUNTS[x]))
            continue

        # If we got here, it's an unsupported mode
        print("Warning: Invalid mode: %s" %mode)

        

        
            
