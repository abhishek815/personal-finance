import os

import mintapi
import pandas as pd

from personal_finance.utils import constants


class MintRepository:
    def __init__(self, headless=True, mfa_method="email") -> None:
        self.mint = mintapi.Mint(
            os.environ.get("MINT_EMAIL"),  # Email used to log in to Mint
            os.environ.get("MINT_PWD"),  # Your password used to log in to mint
            headless=headless,
            mfa_method=mfa_method,
            imap_account=os.environ.get(
                "MINT_EMAIL"
            ),  # account name used to log in to your IMAP server
            imap_password=os.environ.get(
                "EMAIL_PWD"
            ),  # account password used to log in to your IMAP server
            imap_server="imap.gmail.com",  # IMAP server host name
            imap_folder="INBOX",  # IMAP folder that receives MFA email
        )

    def get_data(self, file_dir: str = "./personal_finance/data") -> pd.DataFrame:
        df = self.get_transaction_data()
        if not os.path.isdir(file_dir):
            os.makedirs(file_dir)
        df.to_parquet(os.path.join(file_dir, "transactions_raw.parquet"))
        return df

    def get_transaction_data(self) -> pd.DataFrame:
        return pd.DataFrame(self.mint.get_transaction_data())

    def get_account_data(self):
        return self.mint.get_account_data()

    def get_net_worth_data(self):
        return self.mint.get_net_worth_data()

    def get_credit_score_data(self):
        return self.mint.get_credit_score_data()

    def get_investment_data(self):
        return self.mint.get_investment_data()

    def close(self):
        self.mint.close()


if __name__ == "__main__":
    mint = MintRepository()
    mint.close()
