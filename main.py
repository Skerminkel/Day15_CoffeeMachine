from Data import MENU
from resources import resources as rsc
from resources import money
WATER, MILK, COFFEE = rsc["water"], rsc["milk"], rsc["coffee"]
MONEY = money


def make_or_report(instruction, selected_drink, money_in):
    """
    :param instruction: 'make' or 'report'
    :param selected_drink: 'user input' or None
    :return: if instruction = report, else just tracking usage
    """

    global WATER, MILK, COFFEE, MONEY

    if instruction == "make":

        ingredients = MENU[selected_drink]["ingredients"]
        tw = WATER - list((ingredients[ingredient] for ingredient in ingredients if ingredient == "water"))[0]
        tm = MILK - list((ingredients[ingredient] for ingredient in ingredients if ingredient == "milk"))[0]
        tc = COFFEE - list((ingredients[ingredient] for ingredient in ingredients if ingredient == "coffee"))[0]

        if tw < 0 or tm < 0 or tc < 0:
            return False

        else:
            WATER, MILK, COFFEE = tw, tm, tc
            MONEY += money_in
            return True

    elif instruction == "report":
        return f"water: {WATER},\n milk: {MILK},\n coffee: {COFFEE}\n money: ${MONEY}"


def refill():

    global MILK, WATER, COFFEE

    WATER += float(input("How much water?:\n>"))
    MILK += float(input("How much milk?:\n>"))
    COFFEE += float(input("How much coffee?:\n>"))


def coins_in(selected_drink):

    cash = 0
    cost = MENU[selected_drink]["cost"]

    while cost > cash:
        print(f"A {selected_drink} is ${cost}, you've paid ${cash} so far.")
        cash = float(input("How many pennies?:\n")) * 0.01
        cash += float(input("How many nickels?:\n")) * 0.05
        cash += float(input("How many dimes?:\n")) * 0.1
        cash += float(input("How many quarters?:\n")) * 0.25

    return cash


def main():

    is_on = True
    while is_on:
        print("What would you like to order?")
        print("Espresso, Latte, or Cappuccino?")
        selection = input("> ").lower()

        if selection in MENU:
            cost = MENU[selection]["cost"]
            money = coins_in(selection)
            change = money - cost

            if make_or_report("make", selection, cost):
                print(f"Enjoy your {selection}. Your change is ${round(change, 2)}")

            else:
                print(f"Sorry, there aren't enough ingredients to make your {selection}.")
                print(f"Here is a refund of your ${money}.")

        elif selection == "report":
            print(make_or_report(selection, None, None))
            refill_ask = input("Do you want to refill? Yes, No?:\n").lower()
            if refill_ask == "y" or refill_ask == "yes":
                refill()

        elif selection == "off":
            with open("resources.py", "w") as f:
                new_resources = {"water": WATER,
                                 "milk": MILK,
                                 "coffee": COFFEE}
                f.write(f"resources = {new_resources}\nmoney = {MONEY}")

            is_on = False


main()
