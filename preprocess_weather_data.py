import pandas as pd


def get_weather_df(input_file_path):
    # df = pd.read_csv('input_data/full_weather_data_2023.csv')
    df = pd.read_csv(input_file_path)
    print(df.keys())
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # print(df)
    # print(df['Date'].dtype)
    return df

