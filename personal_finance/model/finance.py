import os
from abc import ABC, abstractmethod

import pandas as pd

from personal_finance.utils import constants, utils


class FinanceType(ABC):
    def __init__(self, data_dir) -> None:
        self.data = pd.read_parquet(os.path.join(data_dir, "transactions_raw.parquet"))

    @abstractmethod
    def transform(self, month: int) -> pd.DataFrame:
        pass
