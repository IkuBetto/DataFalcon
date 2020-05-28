import json
import boto3
import pandas as pd
from time import sleep

# dfを読み込みdataframeを返す
def read_csv_from_S3(bucket, path):
    s3 = boto3.client('s3')
    obj = s3.get_object(Bucket=bucket, Key=path)
    df = pd.read_csv(obj['Body'], index_col=0)
    return df

# dfを指定したバケットの指定したパスに保存する関数
def put_df_to_S3(df, bucket, path):
    from io import StringIO
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, path).put(Body=csv_buffer.getvalue())

def lambda_handler(event, context):
    # 今週開催されるcalendarを取得
    next_week_calendar_df = read_csv_from_S3('rpa-horse-racing', "next_week_calendar.csv")
    date_list = next_week_calendar_df["date"]

    all_data_for_django_df = pd.DataFrame()
    
    # 日付の数だけ繰り返す
    for date in date_list:
        data_for_django_df = read_csv_from_S3('rpa-horse-racing', "{}/data_for_django.csv".format(date))
        all_data_for_django_df = pd.concat([all_data_for_django_df, data_for_django_df], axis=0, ignore_index=0)
    print(all_data_for_django_df)
    put_df_to_S3(all_data_for_django_df, 'rpa-horse-racing', 'data_for_django.csv')
    return
