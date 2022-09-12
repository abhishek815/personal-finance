import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import pandas as pd
from finance import FinanceType

from personal_finance.utils import constants, utils


class Income(FinanceType):
    def __init__(self, data_dir: str = constants.FILE_DIR) -> None:
        super().__init__(data_dir)
        self.name = "income"

    def transform(self, month: int, year: int) -> pd.DataFrame:
        filtered = super().transform(month, year)
        income = filtered.loc[filtered["type"] == "CashAndCreditTransaction"]

        # TODO: make this check prettier
        if not len(income):
            return pd.DataFrame(columns=constants.FINAL_COLS)
        paycheck = []
        # TODO: seperate out paycheck and extra forms of income
        for _, values in income.iterrows():
            if (
                values["category"]["name"] == "Paycheck"
                or values["category"]["name"] == "Income"
            ):
                paycheck.append(values)

        # TODO: make this check prettier
        if not len(paycheck):
            return pd.DataFrame(columns=constants.FINAL_COLS)

        pure_paycheck = pd.DataFrame(paycheck)
        pure_paycheck[constants.CATEGORY] = "Paycheck"

        return self.collapse(pure_paycheck[constants.FINAL_COLS])

    def collapse(self, df: pd.DataFrame) -> pd.DataFrame:
        return df
