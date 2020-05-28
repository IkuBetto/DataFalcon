import pandas as pd
import os
from datetime import datetime as dt
import numpy as np
import boto3
import s3fs
# horse_csv_path = os.path.join(".", "csv_src", "data_for_django.csv")
# DF_HORSE = pd.read_csv(horse_csv_path, encoding="utf-8", index_col=0).fillna('-')

def read_csv_from_S3():
    # bucket = 'rpa-horse-racing'
    # horse_csv_path = "data_for_django.csv"
    # s3 = boto3.client('s3')
    # obj = s3.get_object(Bucket=bucket, Key=horse_csv_path)
    # df = pd.read_csv(obj['Body'], encoding="utf-8", index_col=0).fillna('-')
    df = pd.read_csv('s3n://rpa-horse-racing/data_for_django.csv', encoding="utf-8", index_col=0).fillna('-').astype("str")
    return df
    



""" データの小数を四捨五入 """
# float型の判定
def isfloat(parameter):
    try:
        parameter.isdecimal()
    except AttributeError:
        return False
    if not parameter.isdecimal():
        try:
            float(parameter)
            return True
        except ValueError:
            return False
    else:
        return False

def rounddata(data):    
    for i in range(len(data)):
        for j in range(len(data[i])):
            if j != 0 and isfloat(data[i][j]):
                data[i][j] = str(round(float(data[i][j]), 1))
    return data


""" レース別馬一覧データ """

def emphasize(df_place_horse):
    color = ["white", "rgb(199,228,219)", "rgb(171,214,201)"]
    for i in range(len(df_place_horse)):
        for j in range(5):
            color_index = 0
            if df_place_horse[i][10+j].isdecimal():
                if 4 <= int(df_place_horse[i][10+j]) <=8 :
                    if 2 <= (float(df_place_horse[i][20+j]) if isfloat(df_place_horse[i][20+j]) else 0) <= 6 :
                        color_index = 2
                    elif 2 <= (float(df_place_horse[i][25+j]) if isfloat(df_place_horse[i][25+j]) else 0) <= 6:
                        color_index = 2
                    else : 
                        color_index  = 1
                elif 2 <= ((float(df_place_horse[i][20+j]) if isfloat(df_place_horse[i][20+j]) else 0) * (int(df_place_horse[i][10+j])-1) +  (float(df_place_horse[i][25+j]) if isfloat(df_place_horse[i][25+j]) else 0) * (int(df_place_horse[i][15+j])-int(df_place_horse[i][10+j])))/(int(df_place_horse[i][15+j])-1) <=4:
                    color_index = 1
                else:
                    color_index = 0
            else :
                color_index = 0
            df_place_horse[i].append(color[color_index])
    return df_place_horse


# 帽子の色を追加
def HorseColor(df_place):
    color= ["white", "black", "red", "blue", "yellow", "green", "#FF4F02","fuchsia"]
    length = len(df_place)
    q = length // 8
    colorlist=[]
    pencolor = []
    if q==0:
        for i in range(len(df_place)):
            colorlist.append(color[i])
            if color[i]=='black':
                pencolor.append('white')
            else :
                pencolor.append('black')
    else:
        for i in range(8):
            if i < 8 - (length%8):
                for j in range(q):
                    colorlist.append(color[i])
                    if color[i]=='black':
                        pencolor.append('white')
                    else :
                        pencolor.append('black')
            else:
                for j in range(q+1):
                    colorlist.append(color[i])
                    if color[i]=='black':
                        pencolor.append('white')
                    else :
                        pencolor.append('black')
    for i in range(len(df_place)):
        df_place[i].append(colorlist[i])
        df_place[i].append(pencolor[i])
    return emphasize(df_place)

# 一つのレースの馬データ
def HorseList(date, place, race_num):
    DF_HORSE = read_csv_from_S3()
    df_date = DF_HORSE[DF_HORSE.date==date]
    df_num = df_date[df_date.race_num==race_num]
    df_place = df_num[df_num.place==place]
    df_list = df_place.values.tolist()
    for i in range(len(df_list)):
        for j in range(len(df_list[i])):
            if j != 0 and isfloat(df_list[i][j]):
                df_list[i][j] = str(round(float(df_list[i][j]), 1)) 
            elif j>=10 and df_list[i][j].isalpha():
                df_list[i][j] = '-'
    return HorseColor(df_list)


""" 全馬一覧データ """

# 最初の日
def firstDate():
    DF_HORSE = read_csv_from_S3()
    return DF_HORSE.iloc[0, 0] 

# ソート後の型変換(numpyオブジェクトから整数など)
def castList(horselist):
    for i in range(len(horselist)):
        for j in range(len(horselist[i])):
            obj = horselist[i][j]
            if isinstance(obj, np.integer):
                horselist[i][j] = int(obj)
            elif isinstance(obj, np.floating):
                horselist[i][j] = float(obj)
    return rounddata(horselist)

#日付ごとの馬情報
def HorseByDay():
    DF_HORSE = read_csv_from_S3()
    days = DF_HORSE[~DF_HORSE.duplicated(subset="date")].iloc[:,0].to_list()
    horse_dic = {}
    for i in days:
        horse_dic[i] =  DF_HORSE[DF_HORSE.date==i]
    return horse_dic

# 通常のデータ
def HorseNomalSort(date, rankto, rankfrom):
    DF_HORSE = read_csv_from_S3()
    if date == '':
        date = DF_HORSE.values.tolist()[0][0]
    df_date = HorseByDay()[date]
    horse_list_nomal = []
    for i in range(len(df_date)):
        for j in range(5):
            horse_info = df_date.iloc[i, [0,1,2,3,4,5+j, 10+j, 15+j, 20+j, 25+j]].values.tolist()
            horse_info.append(j+1)
            if horse_info[5] != '-' and horse_info[6].isdecimal():
                if rankto == '' and rankfrom == '':
                    horse_list_nomal.append(horse_info)
                elif rankto == '' and rankfrom != '':
                    if int(horse_info[6])>= int(rankfrom):
                        horse_list_nomal.append(horse_info)
                elif rankto != '' and rankfrom == '':
                    if int(horse_info[6]) <= int(rankto):
                        horse_list_nomal.append(horse_info)
                elif rankto != '' and rankfrom != '':
                    if int(rankfrom) <= int(horse_info[6]) <= int(rankto):
                        horse_list_nomal.append(horse_info)
    return castList(horse_list_nomal)


# 順位でのソート
def HorseRankSort(date, startIndex, rankto, rankfrom):
    DF_HORSE = read_csv_from_S3()
    if date == '':
        date = DF_HORSE.values.tolist()[0][0]
    df_date = HorseByDay()[date]
    horse_rank = df_date.iloc[:, startIndex:(startIndex+5)]
    horse_rank_list = horse_rank.values.flatten()
    for i in range(len(horse_rank_list)):
        if horse_rank_list[i] == '-':
            horse_rank_list[i] = float(0)
        elif type(horse_rank_list[i]) == type(""):
            try:
                horse_rank_list[i] = float(horse_rank_list[i])
            except:
                horse_rank_list[i] = float(0)
        else :
            horse_rank_list[i] = float(0)
    rank_index = np.argsort(horse_rank_list)
    index_list = []
    for i in range(len(rank_index)):
        column_index = rank_index[i] // 5
        row_index = rank_index[i] % 5
        index_list.append((column_index, row_index))
    horse_rank_index = []
    for i, j in index_list:
        horse_data = df_date.iloc[i, [0,1,2,3,4,5+j, 10+j, 15+j, 20+j, 25+j]].values.tolist()
        horse_data.append(j+1)
        if(rankfrom=='' and rankto==''):
            try:
                float(df_date.iloc[i, startIndex+j])
                if type(df_date.iloc[i, startIndex+j]) != type(float(0)):
                    horse_rank_index.append(horse_data)
            except:
                pass
        elif(rankfrom=='' and rankto!=''):
            try:
                float(df_date.iloc[i, startIndex+j])
                if(int(rankto) >= float(df_date.iloc[i, 10+j])):
                    if type(df_date.iloc[i, startIndex+j]) != type(float(0)):
                        horse_rank_index.append(horse_data)
            except:
                pass
        elif(rankfrom!='' and rankto==''):
            try:
                float(df_date.iloc[i, startIndex+j])
                if(int(rankfrom) <= float(df_date.iloc[i, 10+j])):
                    if type(df_date.iloc[i, startIndex+j]) != type(float(0)):
                        horse_rank_index.append(horse_data)
            except:
                pass
        elif(rankfrom!='' and rankto!=''):
            try:
                float(df_date.iloc[i, startIndex+j])
                if(int(rankfrom) <= float(df_date.iloc[i, 10+j]) <= int(rankto)):
                    if type(df_date.iloc[i, startIndex+j]) != type(float(0)): 
                        horse_rank_index.append(horse_data)
            except:
                pass
    return castList(horse_rank_index)


# ソートの確認
def HorseSort(date, sort,rankto,rankfrom):
    if(sort=='rank_acc'):
        return HorseRankSort(date, 10,rankto, rankfrom)
    elif(sort=='rank_dis'):
        return HorseRankSort(date, 10,rankto, rankfrom)[::-1]
    elif(sort=='upperrank_acc'):
        return HorseRankSort(date, 20,rankto, rankfrom)
    elif(sort=='upperrank_dis'):
        return HorseRankSort(date, 20,rankto, rankfrom)[::-1]
    elif(sort=='lowerrank_acc'):
        return HorseRankSort(date, 25,rankto, rankfrom)
    elif(sort=='lowerrank_dis'):
        return HorseRankSort(date, 25,rankto, rankfrom)[::-1]
    else:
        return HorseNomalSort(date, rankto, rankfrom)
