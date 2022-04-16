# Import pathlib
from pathlib import Path

#Import fileio
from qualifier.utils import fileio

# Import Calculators
from qualifier.utils import calculators

# Import Filters
from qualifier.filters import credit_score
from qualifier.filters import debt_to_income
from qualifier.filters import loan_to_value
from qualifier.filters import max_loan_size

def test_save_csv():
    testpath = Path("./data/output/qualifying_loans_test.csv")
    fileio.save_csv(testpath, {})
    assert testpath.exists()

def test_calculate_monthly_debt_ratio():
    assert calculators.calculate_monthly_debt_ratio(1500, 4000) == 0.375

def test_calculate_loan_to_value_ratio():
    assert calculators.calculate_loan_to_value_ratio(210000, 250000) == 0.84

def test_filters():
    bank_data = fileio.load_csv(Path('./data/daily_rate_sheet.csv'))
    current_credit_score = 750
    debt = 1500
    income = 4000
    loan = 210000
    home_value = 250000

    monthly_debt_ratio = debt / income

    loan_to_value_ratio = loan / home_value

    loans = len(max_loan_size.filter_max_loan_size(loan, bank_data))
    # The number of loans qualifying with a loan amount of 210000 is 18
    assert loans == 18
    credit = len(credit_score.filter_credit_score(current_credit_score, bank_data))
    # The number of loans qualifying with a credit score of 750 should be 15
    assert credit == 15
    dti = len(debt_to_income.filter_debt_to_income(monthly_debt_ratio, bank_data))
    # The number of loans qualifying with a debt to income ratio of 0.375 should be 19
    assert dti == 19
    ltv = len(loan_to_value.filter_loan_to_value(loan_to_value_ratio, bank_data))
    # The number of loans qualifying with a loan to value ratio of 0.84 should be 19
    assert ltv == 19