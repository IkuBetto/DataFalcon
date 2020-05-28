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

def lambda_handler(event, context):
    # 今週開催されるcalendarを取得
    next_week_calendar_df = read_csv_from_S3('rpa-horse-racing', "next_week_calendar.csv")
    date_list = next_week_calendar_df["date"]

    # 日付の数だけ繰り返す
    for date in date_list:
        # 引数
        input_event = {
            "date": date
        }
        Payload = json.dumps(input_event) # jsonシリアライズ

        # 呼び出し
        response = boto3.client('lambda').invoke(
            FunctionName='HORSE_called_making_data_for_dango',
            InvocationType='Event',
            Payload=Payload
        )
        print("---02: response:", response)
    return
