from abc import ABC, abstractmethod

import pandas as pd


class FinanceType(ABC):
    @abstractmethod
    def transform(self) -> pd.DataFrame:
        pass
