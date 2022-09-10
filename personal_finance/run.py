import os
import sys

import click

from personal_finance.model import income, investments, spending
from personal_finance.repository.mint_repository import MintRepository
from personal_finance.utils import constants, utils


@click.command()
@click.option("-y", "--year", default=2022)
@click.option("-f", "--file_dir", default=constants.FILE_DIR)
def main(year, file_dir):
    # Run repo to get data
    MintRepository().get_data()

    finance_types = [income.Income(), investments.Investments(), spending.Spending()]

    for finance_type in finance_types:
        file_name = f"{finance_type.name}_monthly_aggregated.csv"
        finance_df = finance_type.get_aggregated_monthly(year=str(year))
        utils.check_dir(file_dir)
        finance_df.to_csv(os.path.join(file_dir, file_name))


if __name__ == "__main__":
    main()
