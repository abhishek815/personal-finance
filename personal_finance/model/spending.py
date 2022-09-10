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
        super().__init__(data_dir)

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
                and values["category"]["parentName"] not in constants.EXCLUDE_CREDIT
            ):
                new_df.append(values)
                categories.append(category)

        cash_credit = pd.DataFrame(new_df)
        cash_credit[constants.CATEGORY] = categories
        cash_credit["payment_type"] = "Credit"

        return cash_credit[constants.FINAL_COLS + ["payment_type"]]
