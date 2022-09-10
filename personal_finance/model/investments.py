import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

import pandas as pd
from finance import FinanceType

from personal_finance.utils import constants, utils


class Investments(FinanceType):
    def __init__(self, data_dir: str = constants.FILE_DIR) -> None:
        super().__init__(data_dir)
        self.name = "investments"

    def transform(self, month: int, year: int) -> pd.DataFrame:
        filtered = super().transform(month, year)

        investment = filtered.loc[filtered["type"] == "InvestmentTransaction"]
        final_investments = investment.loc[investment["isExpense"] == False]

        final_investments[constants.CATEGORY] = "Investments"

        final_investments = final_investments[
            final_investments[["price", "quantity"]].isna().any(axis=1)
        ]
        if not len(final_investments):
            return pd.DataFrame(columns=constants.FINAL_COLS)

        investment_type = []
        for _, values in final_investments.iterrows():
            investment_type.append(values["accountRef"]["name"])
        final_investments[constants.CATEGORY] = investment_type

        return self.collapse(final_investments[constants.FINAL_COLS])

    def collapse(self, df: pd.DataFrame) -> pd.DataFrame:
        return df
