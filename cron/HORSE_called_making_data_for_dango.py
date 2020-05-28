import json
import boto3
import pandas as pd
from time import sleep

# dfを読み込みdataframeを返す
def read_csv_from_S3(bucket, path):
    s3 = boto3.client('s3')
    try:
        obj = s3.get_object(Bucket=bucket, Key=path)
    except:
        print('%s が見つかりません' % path)
        raise
    
    print('%s を読み込みます' % path)
    df = pd.read_csv(obj['Body'], index_col=0)
    return df
    
# dfを指定したバケットの指定したパスに保存する関数
def put_df_to_S3(df, bucket, path):
    from io import StringIO
    csv_buffer = StringIO()
    df.to_csv(csv_buffer)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, path).put(Body=csv_buffer.getvalue())

# 開催地、レース名、馬名を引数、all_past_race_result_dfとして上位馬下位馬の平均順位をだす関数
def upper_lower_rank_def(date, place, race_num, race_name, horse_name, all_past_race_result_df):
    print("=" * 100)
    print(date, place, horse_name)
    # upper,lowerのあるCSVを取得する
    all_past_race_result_df = all_past_race_result_df[all_past_race_result_df["date"] == date][all_past_race_result_df["place"] == place][all_past_race_result_df["place"] == place][all_past_race_result_df["horse_name"] == horse_name]
    # 幾つの過去レースがあるか
    past_race_result_num = all_past_race_result_df.shape[0]
    
    # 例：upper_rank_list == [1.2, 3.0, -, 1, 2]
    upper_rank_list = []
    lower_rank_list = []
    
    past_race_name_list = []
    past_horse_rank_list = []
    past_horse_num_list = []
    
    # 過去レースのある分計算をする
    for all_past_race_result_index in all_past_race_result_df.index:
        place = all_past_race_result_df["place"][all_past_race_result_index]
        race_num = all_past_race_result_df["race_num"][all_past_race_result_index]
        horse_name = all_past_race_result_df["horse_name"][all_past_race_result_index]
        race_name = all_past_race_result_df["race_name"][all_past_race_result_index]
        past_race_num = all_past_race_result_df["past_race_num"][all_past_race_result_index]
        past_race_name = all_past_race_result_df["past_race_name"][all_past_race_result_index]
        #past_horse_rank = all_past_race_result_df["past_horse_rank"][all_past_race_result_index]
        past_horse_rank = str(all_past_race_result_df["past_horse_rank"][all_past_race_result_index])
        past_horse_num = all_past_race_result_df["past_horse_num"][all_past_race_result_index]
        
        past_race_name_list.append(past_race_name)
        past_horse_rank_list.append(past_horse_rank)
        past_horse_num_list.append(past_horse_num)
        
        print(past_race_name, past_horse_rank)
        

        # 稀に馬が怪我などで走れなくなっているため、馬の順位はpast_horse_rankの内容で精査する
        if past_horse_rank.isdecimal():
            try:
                upper_df = read_csv_from_S3('rpa-horse-racing', "{}/{}/{}_{}/{}/{}_{}/upper.csv".format(date,place,race_num,race_name,horse_name,past_race_num,past_race_name))
#                lower_df = read_csv_from_S3('rpa-horse-racing', "{}/{}/{}_{}/{}/{}_{}/lower.csv".format(date,place,race_num,race_name,horse_name,past_race_num,past_race_name))
            except:
                print("%s %s のupperを飛ばします" % (past_race_name, past_horse_rank))
                upper_next_average_rank = "scraping_err"
            else:
                # 次走平均順位の計算
                if upper_df.shape[0] > 0:
                    upper_next_average_rank = upper_df[upper_df["next_average_rank"] != 0].mean()["next_average_rank"]
                else:
                    upper_next_average_rank = "-"
#            if lower_df.shape[0] > 0:
#                lower_next_average_rank = lower_df[lower_df["next_average_rank"] != 0].mean()["next_average_rank"]
#            else:
#                lower_next_average_rank = "-"
            finally:
                upper_rank_list.append(upper_next_average_rank)
            
            try:
                lower_df = read_csv_from_S3('rpa-horse-racing', "{}/{}/{}_{}/{}/{}_{}/lower.csv".format(date,place,race_num,race_name,horse_name,past_race_num,past_race_name))
            except:
                print("%s %s のlowerを飛ばします" % (past_race_name, past_horse_rank))
                lower_next_average_rank = "scraping_err"
            else:
                # 次走平均順位の計算
                if lower_df.shape[0] > 0:
                    lower_next_average_rank = lower_df[lower_df["next_average_rank"] != 0].mean()["next_average_rank"]
                else:
                    lower_next_average_rank = "-"
            finally:
                lower_rank_list.append(lower_next_average_rank)
        
        else:
            upper_next_average_rank = "-"
            lower_next_average_rank = "-"
            upper_rank_list.append(upper_next_average_rank)
            lower_rank_list.append(lower_next_average_rank)
        
    # もし5つ過去レースが無い場合、"-"を挿入する
    if past_race_result_num < 5:
        for i in range(5 - past_race_result_num):
            upper_rank_list.append("-")
            lower_rank_list.append("-")
            past_race_name_list.append("-")
            past_horse_rank_list.append("-")
            past_horse_num_list.append("-")

    return upper_rank_list, lower_rank_list, past_race_name_list, past_horse_rank_list, past_horse_num_list


def lambda_handler(event, context):
    # 今週開催されるcalendarを取得
    next_week_calendar_df = read_csv_from_S3('rpa-horse-racing', "next_week_calendar.csv")
    date = event["date"]
    #date = str(event)
    
    # 保存すべき値
    # 日付,開催地,レース番号,レース名,馬番号,馬名,1走前の過去レース名,2走前の過去レース名,3走前の過去レース名,4走前の過去レース名,5走前の過去レース名,
    # 1走前の着順,2走前の着順,3走前の着順,4走前の着順,5走前の着順,1走前の頭数,2走前の頭数,3走前の頭数,4走前の頭数,5走前の頭数,
    # 1走前の上位馬の平均順位,1走前の下位馬の平均順位,2走前の上位馬の平均順位,2走前の下位馬の平均順位,3走前の上位馬の平均順位,3走前の下位馬の平均順位,4走前の上位馬の平均順位,4走前の下位馬の平均順位,5走前の上位馬の平均順位,5走前の下位馬の平均順位
    date_list_to_save = []
    place_list_to_save = []
    race_num_list_to_save = []
    race_name_list_to_save = []
    horse_name_list_to_save = []
    past_race_name_list_to_save_1 = []
    past_race_name_list_to_save_2 = []
    past_race_name_list_to_save_3 = []
    past_race_name_list_to_save_4 = []
    past_race_name_list_to_save_5 = []
    past_horse_rank_list_to_save_1 = []
    past_horse_rank_list_to_save_2 = []
    past_horse_rank_list_to_save_3 = []
    past_horse_rank_list_to_save_4 = []
    past_horse_rank_list_to_save_5 = []
    past_horse_num_list_to_save_1 = []
    past_horse_num_list_to_save_2 = []
    past_horse_num_list_to_save_3 = []
    past_horse_num_list_to_save_4 = []
    past_horse_num_list_to_save_5 = []
    upper_rank_list_to_save_1 = []
    upper_rank_list_to_save_2 = []
    upper_rank_list_to_save_3 = []
    upper_rank_list_to_save_4 = []
    upper_rank_list_to_save_5 = []
    lower_rank_list_to_save_1 = []
    lower_rank_list_to_save_2 = []
    lower_rank_list_to_save_3 = []
    lower_rank_list_to_save_4 = []
    lower_rank_list_to_save_5 = []
    
    
    
    all_past_race_result_df = read_csv_from_S3('rpa-horse-racing', "{}/all_past_race_result.csv".format(date))
    all_horse_list_URL_df = read_csv_from_S3('rpa-horse-racing', "{}/all_horse_list_URL.csv".format(date))
    
    
    # horse_list_URL_dfの中から走順を取得する
    horse_order = 0
    horse_order_index_dict = {}
    for horse_list_URL_df_index in all_horse_list_URL_df.index:
        now_place_name = all_horse_list_URL_df["race_name"][horse_list_URL_df_index]
        horse_order += 1
        if horse_list_URL_df_index != all_horse_list_URL_df.shape[0] - 1:
            next_place_name = all_horse_list_URL_df["race_name"][horse_list_URL_df_index + 1]
            if next_place_name != now_place_name:
                horse_order = 0
        horse_order_index_dict[horse_list_URL_df_index] = horse_order
    
    
    # 日付,開催地,レース番号,レース名,馬番号,馬名,何走前か,過去レース名,着順,頭数,上位馬の平均順位,下位馬の平均順位
    # all_past_race_result_dfのインデックス数分繰り返す
    for all_horse_list_URL_df_index in all_horse_list_URL_df.index:
        place = all_horse_list_URL_df["place"][all_horse_list_URL_df_index]
        race_name = all_horse_list_URL_df["race_name"][all_horse_list_URL_df_index]
        race_num = all_horse_list_URL_df["race_num"][all_horse_list_URL_df_index]
        horse_order_num = horse_order_index_dict[all_horse_list_URL_df_index]
        horse_name = all_horse_list_URL_df["horse_name"][all_horse_list_URL_df_index]
        
        
        print(date, place, race_num, race_name, horse_name)
        upper_rank_list, lower_rank_list, past_race_name_list, past_horse_rank_list, past_horse_num_list = upper_lower_rank_def(date, place, race_num, race_name, horse_name, all_past_race_result_df)
        
        
        
        # データ保存のためにデータをリストに格納
        date_list_to_save.append(date)
        place_list_to_save.append(place)
        race_num_list_to_save.append(race_num)
        race_name_list_to_save.append(race_name)
        horse_name_list_to_save.append(horse_name)
        
        past_race_name_list_to_save_1.append(past_race_name_list[0])
        past_race_name_list_to_save_2.append(past_race_name_list[1])
        past_race_name_list_to_save_3.append(past_race_name_list[2])
        past_race_name_list_to_save_4.append(past_race_name_list[3])
        past_race_name_list_to_save_5.append(past_race_name_list[4])
        past_horse_rank_list_to_save_1.append(past_horse_rank_list[0])
        past_horse_rank_list_to_save_2.append(past_horse_rank_list[1])
        past_horse_rank_list_to_save_3.append(past_horse_rank_list[2])
        past_horse_rank_list_to_save_4.append(past_horse_rank_list[3])
        past_horse_rank_list_to_save_5.append(past_horse_rank_list[4])
        past_horse_num_list_to_save_1.append(past_horse_num_list[0])
        past_horse_num_list_to_save_2.append(past_horse_num_list[1])
        past_horse_num_list_to_save_3.append(past_horse_num_list[2])
        past_horse_num_list_to_save_4.append(past_horse_num_list[3])
        past_horse_num_list_to_save_5.append(past_horse_num_list[4])
        upper_rank_list_to_save_1.append(upper_rank_list[0])
        upper_rank_list_to_save_2.append(upper_rank_list[1])
        upper_rank_list_to_save_3.append(upper_rank_list[2])
        upper_rank_list_to_save_4.append(upper_rank_list[3])
        upper_rank_list_to_save_5.append(upper_rank_list[4])
        lower_rank_list_to_save_1.append(lower_rank_list[0])
        lower_rank_list_to_save_2.append(lower_rank_list[1])
        lower_rank_list_to_save_3.append(lower_rank_list[2])
        lower_rank_list_to_save_4.append(lower_rank_list[3])
        lower_rank_list_to_save_5.append(lower_rank_list[4])


    data_for_django_df = pd.DataFrame({
        "date": date_list_to_save,
        "place": place_list_to_save,
        "race_num": race_num_list_to_save, 
        "race_name": race_name_list_to_save,
        # "horse_num": horse_num_list_to_save,
        "horse_name": horse_name_list_to_save,
        "past_race_name_1": past_race_name_list_to_save_1,
        "past_race_name_2": past_race_name_list_to_save_2,
        "past_race_name_3": past_race_name_list_to_save_3,
        "past_race_name_4": past_race_name_list_to_save_4,
        "past_race_name_5": past_race_name_list_to_save_5,
        "past_horse_rank_1": past_horse_rank_list_to_save_1,
        "past_horse_rank_2": past_horse_rank_list_to_save_2,
        "past_horse_rank_3": past_horse_rank_list_to_save_3,
        "past_horse_rank_4": past_horse_rank_list_to_save_4,
        "past_horse_rank_5": past_horse_rank_list_to_save_5,
        "past_horse_num_1": past_horse_num_list_to_save_1,
        "past_horse_num_2": past_horse_num_list_to_save_2,
        "past_horse_num_3": past_horse_num_list_to_save_3,
        "past_horse_num_4": past_horse_num_list_to_save_4,
        "past_horse_num_5": past_horse_num_list_to_save_5,
        "upper_rank_1": upper_rank_list_to_save_1,
        "upper_rank_2": upper_rank_list_to_save_2,
        "upper_rank_3": upper_rank_list_to_save_3,
        "upper_rank_4": upper_rank_list_to_save_4,
        "upper_rank_5": upper_rank_list_to_save_5,
        "lower_rank_1": lower_rank_list_to_save_1,
        "lower_rank_2": lower_rank_list_to_save_2,
        "lower_rank_3": lower_rank_list_to_save_3,
        "lower_rank_4": lower_rank_list_to_save_4,
        "lower_rank_5": lower_rank_list_to_save_5,
    })
    
    put_df_to_S3(data_for_django_df, "rpa-horse-racing", "{}/data_for_django.csv".format(date))
    
    return