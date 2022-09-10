FILE_DIR = "./personal_finance/data"

EXCLUDE_CREDIT = ["Investments", "Transfer", "Paycheck"]

CATEGORY = "category_type"
INVESTMENT = "investment_type"

FINAL_COLS = ["type", "id", "accountId", "date", "description", "amount", CATEGORY]


MONTHS = [i for i in range(1, 13)]

MONTHS_MAPPING = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December",
}
