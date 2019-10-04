#-*- coding: utf-8 -*-
import sys
import requests
from bs4 import BeautifulSoup
import json
import os
import csv
import time
import datetime

def get_program_detail(program, rCount, csvfile, id_csvfile):
    reviewPages = int((rCount/10)+1)
    id_csvfile.write(program['title'].replace(',','.')+"\n")
    for i in range(reviewPages):
        req = requests.get('REQUEST URL')
        datas = req.text
        parsed_datas = json.loads(datas)
        for data in parsed_datas:
            catchPhrase = ""
            con = ""
            for catchval in program['catchPhrase'].split("\n"):
                catchPhrase += catchval
            for content_val in data['content'].split("\n"):
                con += content_val
            id_row = str("{0}\n".format(con.replace(',','.')))
            row = str("{0},{1},{2},{3},{4},{5},{6}\n".format(program['id'],program['title'].replace(',','.'),catchPhrase.replace(',','.'),\
                        data['customer']['id'],data['customer']['name'],data['rating'],con.replace(',','.')))
            id_csvfile.write(id_row)
            csvfile.write(row)
    print(str(program['id'])+' saved!')

if __name__=='__main__':

    nowDatetime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    process_time = 0
    # preset full review csv file
    csv_dir = "datas/"+nowDatetime
    os.makedirs(csv_dir)
    download_dir = csv_dir+"/frip_reviews.csv"
    csvfile = open(download_dir, "w")
    columnTitleRow = "id,title,catchPhrase,customerId,customerName,rating,content\n"
    csvfile.write(columnTitleRow)

    num = 1
    item_num = 100
    while 1:
        start_time = time.time()
        req = requests.get('REQUEST URL')
        datas = req.text
        if datas=='[]':
            print('END!')
            break
        else:
            parsed_datas = json.loads(datas)
            for data in parsed_datas:
                rCount = data['reviewCount']
                if rCount!=0:
                    id_csvfile = open("datas/"+str(data['id'])+".csv", "w")
                    get_program_detail(data, rCount, csvfile, id_csvfile)
                    id_csvfile.close()
        num += 1
        end_time = time.time()
        process_time += end_time-start_time
        print(str(num)+" : WorkingTime: {} sec".format(end_time-start_time))
    csvfile.close()
    print("Total WorkingTime: {} sec".format(process_time))
