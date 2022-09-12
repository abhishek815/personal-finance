import os
import sys
from hashlib import new

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import pandas as pd
from finance import FinanceType

from personal_finance.utils import constants, utils


class Spending(FinanceType):
    def __init__(self, data_dir: str = constants.FILE_DIR) -> None:
        super().__init__(data_dir)
        self.name = "spending"

    def transform(self, month: int, year: int) -> pd.DataFrame:
        filtered = super().transform(month, year)
        # retreive all cash and credit type transactions
        cash_credit = filtered.loc[filtered["type"] == "CashAndCreditTransaction"]

        # TODO: make this check prettier
        if not len(cash_credit):
            return pd.DataFrame(columns=constants.FINAL_COLS + ["payment_type"])

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

        # TODO: make this check prettier
        if not len(new_df):
            return pd.DataFrame(columns=constants.FINAL_COLS + ["payment_type"])

        cash_credit = pd.DataFrame(new_df)
        cash_credit[constants.CATEGORY] = categories
        cash_credit["payment_type"] = "Credit"
        return self.collapse(cash_credit[constants.FINAL_COLS + ["payment_type"]])

    def collapse(self, df: pd.DataFrame) -> pd.DataFrame:
        METHODS = [self.collapse_airlines]
        for method in METHODS:
            df = method(df)
        return df

    def collapse_airlines(self, df: pd.DataFrame) -> pd.DataFrame:
        airlines = ["spirit", "frontier", "delta"]
        new_type, i = [], 0
        for _, values in df.iterrows():
            new_type.append(values[constants.CATEGORY])
            for airline in airlines:
                if airline in values["description"].lower():
                    new_type[i] = "Travel"
                    break
            i += 1
        df[constants.CATEGORY] = new_type
        return df
