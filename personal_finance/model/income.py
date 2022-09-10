import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import json

import pandas as pd
from finance import FinanceType

from personal_finance.utils import constants, utils


class Income(FinanceType):
    def __init__(self, data_dir: str = constants.FILE_DIR) -> None:
        super().__init__(data_dir)

    def transform(self, month: int) -> pd.DataFrame:
        filtered = super().transform(month)
        if not len(filtered):
            return pd.DataFrame(columns=constants.FINAL_COLS)
        cash_credit = filtered.loc[filtered["type"] == "CashAndCreditTransaction"]
        paycheck = []
        for _, values in cash_credit.iterrows():
            if values["category"]["name"] == "Paycheck":
                paycheck.append(values)

        pure_paycheck = pd.DataFrame(paycheck)
        pure_paycheck[constants.CATEGORY] = "Paycheck"

        return pure_paycheck[constants.FINAL_COLS]