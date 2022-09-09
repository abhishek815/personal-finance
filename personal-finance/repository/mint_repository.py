import mintapi
import pandas as pd
from os import environ


class MintRepository:
    def __init__(self, headless=True, mfa_method='email') -> None:
        self.mint = mintapi.Mint(
            environ.get('MINT_EMAIL'),  # Email used to log in to Mint
            environ.get('MINT_PWD'),  # Your password used to log in to mint
            headless=headless,
            mfa_method=mfa_method,
            imap_account= environ.get('MINT_EMAIL'), # account name used to log in to your IMAP server
            imap_password= environ.get('EMAIL_PWD'), # account password used to log in to your IMAP server
            imap_server='imap.gmail.com',  # IMAP server host name
            imap_folder='INBOX',  # IMAP folder that receives MFA email
        )

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