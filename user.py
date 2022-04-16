import logging
import shelve
import questionary
from utils import helpers as hf

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
        # initialize user account list
        self.user_dict = {'Accounts': []}
        self.user_dict['Personal Info'] = {}
        self.add_user_account()


def run():
    user = User()
    username = user.username
    logging.info(f"Hello, {username}!")
    hf.create_directory(hf.shelf_path)
    with shelve.open(hf.shelf) as sh:
        if username in sh:
            user.user_dict = sh[username]
        pass

if __name__ == "__main__":
    logging.basicConfig(
        # filename='debug.log', 
        level=logging.DEBUG)
    run()
