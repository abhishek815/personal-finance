import os


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
