import os

import mintapi
import pandas as pd

from personal_finance.utils import constants, utils
from personal_finance.utils.logger import get_logger

LOGGER = get_logger(__name__)


class MintRepository:
    def __init__(self, headless=True, mfa_method="email") -> None:
        LOGGER.info(f"Signing in and scraping your Mint account.")
        try:
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
        except:
            LOGGER.warn(
                f"Failed to authenticate using IMAP. Retrying with email MFA. Check your email account {os.environ.get('MINT_EMAIL')} for a 6 digit code."
            )
            self.mint = mintapi.Mint(
                os.environ.get("MINT_EMAIL"),  # Email used to log in to Mint
                os.environ.get("MINT_PWD"),  # Your password used to log in to mint
                headless=headless,
                mfa_method=mfa_method,
            )

        LOGGER.info(
            f'Successfully connected to mint with email {os.environ.get("MINT_EMAIL")}'
        )

    def get_data(self, file_dir: str = constants.FILE_DIR) -> pd.DataFrame:
        df = self.get_transaction_data()
        utils.check_dir(file_dir)
        file_path = os.path.join(file_dir, constants.RAW_FILE_NAME)
        df.to_parquet(file_path)

        LOGGER.info(f"Pulled transaction data and saved to {file_path}")
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
