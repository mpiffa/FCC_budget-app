import math

class Category:
    
    def __init__(self, category, ledger = None):
        if ledger is None:
            ledger = []
        self.category = category
        self.ledger = ledger

    def __str__(self):
        """
        When the budget object is printed it should display:
        - A title line of 30 characters where the name of the category is centered in a line of * characters.
        - A list of the items in the ledger. Each line should show the description and amount. 
          The first 23 characters of the description should be displayed, then the amount. 
          The amount should be right aligned, contain two decimal places, and display a maximum of 7 characters.
        - A line displaying the category total.
        """
        len_category = len(self.category)
        first_part = int(math.floor((30-len_category) / 2)) * "*"
        second_part = int(math.ceil((30-len_category) / 2)) * "*"
        headliner = first_part + self.category + second_part + "\n"
        string_to_print = headliner
        for element in self.ledger:
            description = element["description"][:23]
            len_description = len(description)
            spaces = ((23 - len_description) * " ")
            cat_amount = "%.2f" % round(element["amount"], 2)
            if len(cat_amount) < 7:
                spaces += " "
            string_to_print += description + spaces + str(cat_amount).rjust(6) + "\n"
        string_to_print += "Total: " + str(self.get_balance())
        return string_to_print


    def deposit(self, amount: float, description=""):
        """
        A deposit method that accepts an amount and description. If no description is given, 
        it should default to an empty string. The method should append an object to the ledger 
        list in the form of {"amount": amount, "description": description}.
        """
        self.amount = amount
        self.description = description
        self.ledger.append({'amount': amount, 'description': description})


    def withdraw(self, amount: float, description=""):
        """
        A withdraw method that is similar to the deposit method, but the amount passed in should 
        be stored in the ledger as a negative number. If there are not enough funds, nothing should 
        be added to the ledger. This method should return True if the withdrawal took place, and False otherwise.
        """
        self.amount = amount
        self.description = description
        if self.check_funds(amount):
            self.ledger.append({'amount': -abs(amount), 'description': description})
            return True
        else:
            return False


    def get_balance(self):
        """
        A get_balance method that returns the current balance of the budget category 
        based on the deposits and withdrawals that have occurred.
        """
        balance = 0
        for element in self.ledger:
            balance += element["amount"]
        return balance


    def transfer(self, amount:float, category):
        """
        A transfer method that accepts an amount and another budget category as arguments. 
        The method should add a withdrawal with the amount and the description "Transfer to 
        [Destination Budget Category]". The method should then add a deposit to the other budget 
        category with the amount and the description "Transfer from [Source Budget Category]". 
        If there are not enough funds, nothing should be added to either ledgers. 
        This method should return True if the transfer took place, and False otherwise.
        """
        self.amount = amount
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.category}")
            category.deposit(amount, f"Transfer from {self.category}")
            return True
        else:
            return False


    def check_funds(self, amount: float):
        """
        A check_funds method that accepts an amount as an argument. It returns False if the 
        amount is greater than the balance of the budget category and returns True otherwise. 
        This method should be used by both the withdraw method and transfer method.
        """
        self.amount = amount
        if self.get_balance() >= amount:
            return True
        else:
            return False

def create_spend_chart(categories):
    """
    create_spend_chart takes a list of categories as an argument. It should return a string that is a bar chart.
    The chart should show the percentage spent in each category passed in to the function. The percentage spent 
    should be calculated only with withdrawals and not with deposits. Down the left side of the chart should be 
    labels 0 - 100. The "bars" in the bar chart should be made out of the "o" character. The height of each bar 
    should be rounded down to the nearest 10. The horizontal line below the bars should go two spaces past the 
    final bar. Each category name should be written vertically below the bar. There should be a title at the top 
    that says "Percentage spent by category".
    """
    max_category_lenght = 0
    total_withdraw = 0
    for category in categories:
        if len(category.category) > max_category_lenght:
            max_category_lenght = len(category.category)
        for amount in category.ledger:
                if amount["amount"] < 0:
                    total_withdraw += abs(amount["amount"])
    title = "Percentage spent by category\n"
    string_to_print = title
    
    for element in range(100, -1, -10):
        element_string = str(element).rjust(3) + "| "
        for category in categories:
            amount_spent = 0
            for amount in category.ledger:
                if amount["amount"] < 0:
                    amount_spent += amount["amount"]
            if element <= math.floor(abs(amount_spent)*100/total_withdraw):
                element_string += "o  "
            else:
                element_string += "   "
        string_to_print += element_string + "\n"
    
    separator = "    " + "-" * (3 * len(categories) + 1) + "\n" 
    string_to_print += separator

    for character in range(max_category_lenght):
        character_string = "     "
        for category in categories:
            try: 
                char = category.category[character]
                character_string += char + "  " 
            except:
                character_string += "   "
        if character != max_category_lenght - 1:
            character_string += "\n"
        string_to_print += character_string

    return string_to_print