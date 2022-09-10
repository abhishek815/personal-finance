import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import json

import pandas as pd
from finance import FinanceType

from personal_finance.utils import constants, utils


class Investments(FinanceType):
    def __init__(self, data_dir: str = constants.FILE_DIR) -> None:
        super().__init__(data_dir)

    def transform(self, month: int) -> pd.DataFrame:
        filtered = super().transform(month)
        if not len(filtered):
            return pd.DataFrame(columns=constants.FINAL_COLS + [constants.INVESTMENT])
        investment = filtered.loc[filtered["type"] == "InvestmentTransaction"]

        final_investments = investment.loc[investment["isExpense"] == False]
        final_investments[constants.CATEGORY] = "Investments"

        final_investments = final_investments[
            final_investments[["price", "quantity"]].isna().any(axis=1)
        ]

        investment_type = []
        for _, values in final_investments.iterrows():
            investment_type.append(values["accountRef"]["name"])
        print(investment_type)
        final_investments[constants.INVESTMENT] = investment_type

        return final_investments[constants.FINAL_COLS + [constants.INVESTMENT]]
