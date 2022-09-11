import os
from datetime import datetime

import pandas as pd

from personal_finance.utils import constants


def determine_month(month: int) -> str:
    if month >= 1 and month < 10:
        return f"0{month}"
    elif month >= 10 and month <= 12:
        return month
    else:
        raise Exception("Invalid month value, please enter a value between 1 and 12")


def check_dir(file_dir) -> None:
    if not os.path.isdir(file_dir):
        os.makedirs(file_dir)


def list_df_to_directory(
    dfs: list, finance_type_name: str, dir_name: str, offset: int
) -> None:
    for i, df in enumerate(dfs):
        file_name = os.path.join(dir_name, f"{finance_type_name}_{offset+i}.csv")
        df.to_csv(file_name)


def to_excel_format(year: int, file_dir: str):
    income = format_df(
        pd.read_csv(file_dir + "/income_monthly_aggregated.csv", sep=",").rename(
            columns={constants.CATEGORY: "Income (Post Tax)"}
        ),
        constants.MONTHS_MAPPING.values(),
    )
    spending = format_df(
        pd.read_csv(file_dir + "/spending_monthly_aggregated.csv", sep=",").rename(
            columns={constants.CATEGORY: "Expenses"}
        ),
        constants.MONTHS_MAPPING.values(),
    )
    investments = format_df(
        pd.read_csv(file_dir + "/investments_monthly_aggregated.csv", sep=",").rename(
            columns={constants.CATEGORY: "Investments 📈"}
        ),
        constants.MONTHS_MAPPING.values(),
    )

    # datetime object containing current date and time
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    income_start_row = 3
    income_end_row = income_start_row + len(income) + 1

    spending_start_row = income_end_row + 3
    spending_end_row = spending_start_row + len(spending) + 1

    investments_start_row = spending_end_row + 3
    investments_end_row = investments_start_row + len(investments) + 1

    left_over_start_row = investments_end_row + 3

    writer = pd.ExcelWriter(
        file_dir + f"/annual_report_{year}.xlsx", engine="xlsxwriter"
    )

    income.to_excel(
        writer,
        sheet_name="Yearly Report",
        index=False,
        startrow=income_start_row,
        startcol=0,
    )
    spending.to_excel(
        writer,
        sheet_name="Yearly Report",
        index=False,
        startrow=spending_start_row,
        startcol=0,
    )
    investments.to_excel(
        writer,
        sheet_name="Yearly Report",
        index=False,
        startrow=investments_start_row,
        startcol=0,
    )
    workbook = writer.book
    worksheet = writer.sheets["Yearly Report"]

    worksheet.set_zoom(90)

    # add title
    title = "Yearly Financial Report"
    # merge cells
    format = workbook.add_format()
    format.set_font_size(20)
    format.set_font_color("#333333")
    subheader = f"Financial report generated on {dt_string}"
    worksheet.merge_range("A1:AS1", title, format)
    worksheet.merge_range("A2:AS2", subheader)
    worksheet.set_row(2, 15)  # Set the header row height to 15

    worksheet.set_column("A:M", 16)

    format_header("#ffd965", worksheet,
        workbook,
        investments_start_row,
        investments_end_row,
        investments,
    )
    format_header(
        "#ea9999", worksheet, workbook, spending_start_row, spending_end_row, spending
    )
    format_header(
        "#b7d7a8", worksheet, workbook, income_start_row, income_end_row, income
    )

    header_format = workbook.add_format(
        {"bold": True, "bottom": 2, "bg_color": "#a2c4c9"}
    )
    # leftover
    for col_num, value in enumerate(income.columns.values):
        if col_num == 0:
            worksheet.write(left_over_start_row, col_num, "Leftover 🤑", header_format)
        else:
            worksheet.write(left_over_start_row, col_num, value, header_format)
            col_val = chr(ord("@") + (col_num + 1))
            worksheet.write_formula(
                f"{col_val}{left_over_start_row+2}",
                f"=({col_val}{income_end_row+1})-({col_val}{spending_end_row+1} + {col_val}{investments_end_row+1})",
            )

    for month in constants.MONTHS:
        format_month(file_dir, month, workbook, writer)

    writer.save()


def format_month(
    file_dir, month: int, workbook, writer, mapping=constants.MONTHS_MAPPING
):
    month_name = mapping[month]

    spending = pd.read_csv(file_dir + f"/spending/spending_{month}.csv", sep=",").drop(
        columns={"Unnamed: 0"}
    )
    income = pd.read_csv(file_dir + f"/income/income_{month}.csv", sep=",").drop(
        columns={"Unnamed: 0"}
    )
    investments = pd.read_csv(
        file_dir + f"/investments/investments_{month}.csv", sep=","
    ).drop(columns={"Unnamed: 0"})
    income_month_start = 2
    income_month_end = income_month_start + len(income) + 1

    spending_month_start = income_month_end + 3
    spending_month_end = spending_month_start + len(spending) + 1

    investments_month_start = spending_month_end + 3
    investments_month_end = investments_month_start + len(investments) + 1

    income.to_excel(
        writer,
        sheet_name=month_name,
        index=False,
        startrow=income_month_start,
        startcol=0,
    )
    spending.to_excel(
        writer,
        sheet_name=month_name,
        index=False,
        startrow=spending_month_start,
        startcol=0,
    )
    investments.to_excel(
        writer,
        sheet_name=month_name,
        index=False,
        startrow=investments_month_start,
        startcol=0,
    )

    new_worksheet = writer.sheets[month_name]

    new_worksheet.autofilter(f"A{spending_month_start+1}:H{spending_month_start+1}")

    format_title = workbook.add_format({"bold": True})
    format_title.set_font_size(15)
    new_worksheet.write(income_month_start - 1, 0, "Income", format_title)

    new_worksheet.write(spending_month_start - 1, 0, "Spending", format_title)

    new_worksheet.write(investments_month_start - 1, 0, "Investments", format_title)

    title = f"{month_name} Financial Report"
    # merge cells
    format = workbook.add_format()
    format.set_font_size(20)
    format.set_font_color("#333333")
    new_worksheet.merge_range("A1:AS1", title, format)
    new_worksheet.set_row(2, 15)  # Set the header row height to 15
    new_worksheet.set_column("A:H", 16)
    new_worksheet.set_column("E:E", 35)


def format_header(color: str, worksheet, workbook, start_row, end_row, df):
    format_total = workbook.add_format({"bold": True})
    format = workbook.add_format({"bold": True, "bottom": 2, "bg_color": color})

    for col_num, value in enumerate(df.columns.values):
        worksheet.write(start_row, col_num, value, format)
        if col_num == 0:
            worksheet.write(end_row, col_num, "TOTAL", format_total)
        else:
            col_val = chr(ord("@") + (col_num + 1))
            worksheet.write_formula(
                f"{col_val}{end_row+1}",
                f"=SUM({col_val}{start_row+2}:{col_val}{end_row})",
            )


def format_df(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for value in columns:
        df[value] = df[value].astype(float)
        df[value] = df[value].abs()
    return df
