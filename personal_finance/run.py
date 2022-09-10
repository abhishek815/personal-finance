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

    months_df_dict = {}
    for finance_type in finance_types:
        file_name = f"{finance_type.name}_monthly_aggregated.csv"

        finance_df = finance_type.get_aggregated_monthly(year=str(year))
        months_df_dict[finance_type.name] = [
            finance_type.transform(month=month, year=year) for month in constants.MONTHS
        ]

        # ensure paths are present
        utils.check_dir(file_dir)
        utils.check_dir(os.path.join(file_dir, finance_type.name))

        # aggregated finance df's and transaction data saved in designated directory
        finance_df.to_csv(os.path.join(file_dir, file_name))
        utils.list_df_to_directory(
            months_df_dict[finance_type.name],
            finance_type.name,
            os.path.join(file_dir, finance_type.name),
            offset=1,
        )


if __name__ == "__main__":
    main()
