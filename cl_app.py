import logging
import shelve
import questionary
from utils import helpers as hf

from user import User

from qualifier.utils.fileio import (load_bank_data, save_csv)

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value

def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered

def save_qualifying_loans(qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    if questionary.confirm("Would you like to save the file?").ask():
        filename = questionary.text("Enter the filename to save:").ask()
        filepath = 'data/output/' + filename
        save_csv(filepath, qualifying_loans)
        print(f"File {filename} saved to the data/output folder.")

def run():
    user = User()
    username = user.username
    logging.info(f"Hello, {username}!")
    hf.create_directory(hf.shelf_path)
    with shelve.open(hf.shelf) as sh:
        if username in sh:
            user.user_dict = sh[username]
        else:
            sh[username] = user.create_user_dict()
    print(user.user_dict)
    
    # Load bank data from csv
    bank_data = load_bank_data()
    logging.info(f"{len(bank_data)} banks loaded")

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, 
        user.user_dict["Financial Info"]["Credit Score"], 
        user.user_dict["Financial Info"]["Monthly Debt"], 
        user.user_dict["Financial Info"]["Monthly Income"], 
        user.user_dict["Financial Info"]["Loan Amount"], 
        user.user_dict["Financial Info"]["Home Value"]
    )

    # Save qualifying loans (if the list is not empty)
    if len(qualifying_loans) != 0:
        save_qualifying_loans(qualifying_loans)

if __name__ == "__main__":
    logging.basicConfig(
        # filename='debug.log', 
        level=logging.DEBUG)
    run()