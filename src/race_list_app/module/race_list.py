import pandas as pd
import os
from datetime import datetime as dt
import boto3
import s3fs
"""csvファイルの読み込み"""
# race_csv_path = os.path.join(".", "csv_src", "data_for_django.csv")
# df_days = pd.read_csv(race_csv_path, encoding="utf-8", index_col=0)

def read_csv_from_S3():
    # bucket = 'rpa-horse-racing'
    # horse_csv_path = "data_for_django.csv"
    # s3 = boto3.client('s3')
    # obj = s3.get_object(Bucket=bucket, Key=horse_csv_path)
    # df = pd.read_csv(obj['Body'], encoding="utf-8", index_col=0)
    df = pd.read_csv('s3n://rpa-horse-racing/data_for_django.csv', encoding="utf-8", index_col=0).fillna('-').astype("str")
    return df


"""レースの日にちを返す"""
def Racedays():
    df_days = read_csv_from_S3()
    days = df_days[~df_days.duplicated(subset="date")].iloc[:,0].to_list()
    days_ja = [dt.strptime(i, '%Y_%m_%d').strftime('%-m月%-d日') for i in days]
    days_li = [[i,j] for i,j in zip(days, days_ja)]
    return days_li

"""レースの場所、名前一覧"""
def Raceplace():
    df_days = read_csv_from_S3()
    places = df_days[~df_days.duplicated(subset=["date", "place"])].iloc[:,:4].values.tolist()
    return places

"""レースの情報"""
"""def Raceinfo():
    races = df_days.values.tolist()
    return races
"""
def Raceinfo():
    df_days = read_csv_from_S3()
    places = df_days[~df_days.duplicated(subset=["date", "place","race_num"])].iloc[:,:4].values.tolist()
    return places