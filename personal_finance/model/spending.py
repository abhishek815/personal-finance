import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import json

import pandas as pd
from finance import FinanceType

from personal_finance.utils import constants, utils


class Spending(FinanceType):
    def __init__(self, data_dir: str = constants.FILE_DIR) -> None:
        self.data = pd.read_parquet(os.path.join(data_dir, "transactions_raw.parquet"))

    def transform(self, month: int) -> pd.DataFrame:
        month = utils.determine_month(month)
        filtered = self.data.loc[
            (self.data["date"] >= f"2022-{month}-01")
            & (self.data["date"] <= f"2022-{month}-31")
        ]

        # retreive all cash and credit type transactions
        cash_credit = filtered.loc[filtered["type"] == "CashAndCreditTransaction"]

        new_df = []
        categories = []
        for _, values in cash_credit.iterrows():
            category = values["category"]["name"]
            if (
                category != "Credit Card Payment"
                and category not in constants.EXCLUDE_CREDIT
            ):
                new_df.append(values)
                categories.append(category)

        cash_credit = pd.DataFrame(new_df)
        cash_credit["category_type"] = categories

        return cash_credit
