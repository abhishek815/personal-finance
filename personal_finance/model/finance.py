import os
from abc import ABC, abstractmethod
from functools import reduce

import pandas as pd

from personal_finance.utils import constants, utils

pd.options.mode.chained_assignment = None


class FinanceType(ABC):
    def __init__(self, data_dir) -> None:
        self.data = pd.read_parquet(os.path.join(data_dir, "transactions_raw.parquet"))

    @abstractmethod
    def collapse(self, df: pd.DataFrame) -> pd.DataFrame:
        pass

    def get_aggregated_monthly(self, year: int) -> pd.DataFrame:
        dfs = []
        for month in constants.MONTHS:
            df = self.transform(month=month, year=year)
            month_df = (
                df.groupby([constants.CATEGORY])
                .agg({"amount": sum})
                .rename(columns={"amount": constants.MONTHS_MAPPING[month]})
            )

            dfs.append(month_df)

        df = reduce(
            lambda left, right: pd.merge(
                left, right, on=["category_type"], how="outer"
            ),
            dfs,
        ).fillna(0)

        return df

    def transform(self, month: int, year: int) -> pd.DataFrame:
        month = utils.determine_month(month)
        filtered = self.data.loc[
            (self.data["date"] >= f"{year}-{month}-01")
            & (self.data["date"] <= f"{year}-{month}-31")
        ]
        return filtered
