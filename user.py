import logging
import shelve
import questionary
from utils import helpers as hf
import fire

class User:
    def __init__(self, username=None):
        logging.debug("Instantiate User")

        # username is None by default, set with get_user funcion 
        if username is None:
            self.username = self.get_user()
        else:
            self.username = username

        # user dictionary
        self.user_dict = {}

    def get_user(self):
        return questionary.text("What is your name?").ask()

    def create_user_dict(self):
        # initialize user dictionary
        self.user_dict['Financial Info'] = self.get_financial_info()
        return self.user_dict

    def get_financial_info(self):
        """Prompt dialog to get the user's financial information.

        Returns:
            Returns the user's financial information.
        """

        credit_score = int(questionary.text("What's your credit score?").ask())
        monthly_debt = float(questionary.text("What's your current amount of monthly debt?").ask())
        monthly_income = float(questionary.text("What's your total monthly income?").ask())
        loan_amount = float(questionary.text("What's your desired loan amount?").ask())
        home_value = float(questionary.text("What's your home value?").ask())

        return {'Credit Score': credit_score, 'Monthly Debt': monthly_debt, 'Monthly Income': monthly_income, 'Loan Amount': loan_amount, 'Home Value': home_value}


def run(username=None):
    user = User(username)
    username = user.username
    logging.info(f"Hello, {username}!")
    hf.create_directory(hf.shelf_path)
    with shelve.open(hf.shelf) as sh:
        if username in sh:
            user.user_dict = sh[username]
        else:
            sh[username] = user.create_user_dict()
        print(user.user_dict)
        while questionary.confirm("Update financial info?").ask():
            user.user_dict['Financial Info'] = user.get_financial_info()
        else:
            sh[username] = user.user_dict

if __name__ == "__main__":
    logging.basicConfig(
        # filename='debug.log', 
        level=logging.DEBUG)
    fire.Fire(run)
