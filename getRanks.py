#-*- coding: utf-8 -*-
import os
from konlpy.tag import Kkma
from collections import Counter
import time

class Activity:
    def __init__(self):
        self.id = ""
        self.title = ""
        self.keywords = []
    
    def setData(self, id, title, keywords):
        self.id = id
        self.title = title
        self.keywords = keywords

def getId(var):
    return var.split('.')[0]

def getTitle(var):
    f = open("datas/"+filename, "r")
    title = f.readline()
    f.close()
    return title

def getKeywords(var):
    f = open("datas/"+filename, "r")
    next(f)
    data = "".join(f.read().splitlines())
    nouns = Kkma().nouns(data)
    count = Counter(nouns)

    tag_count = []
    tags = []

    for n, c in count.most_common(20):
        dics = {'tag': n, 'count': c}
        if len(dics['tag']) >= 2:
            tag_count.append(dics)
            tags.append(dics['tag'])

    f.close()
    return tags


def createKeywordsReport(activities):
    f = open("keywords.csv", "w")
    f.write("id,title,keywords\n")
    for act in activities:
        keywords_data = ".".join(act.keywords)
        data = str("{0},{1},{2}\n".format(act.id, act.title.rstrip('\n'), keywords_data))
        f.write(data)
    f.close()
    print("report saved!")


if __name__ == "__main__":
    start_time = time.time()
    activities = []
    length = len(os.listdir(os.getcwd()+"/datas"))
    idx = 1
    for filename in os.listdir(os.getcwd()+"/datas"):
        try:        
            act = Activity()
            # filename is activity's id
            id = getId(filename)        
            title = getTitle(filename)
            keywords = getKeywords(filename)
            act.setData(id, title, keywords)
            activities.append(act)
        except Exception as e:
            a = True
        print(str(idx)+"/"+str(length)+" process complete")
        idx += 1

        
    createKeywordsReport(activities)
    end_time = time.time()
    print("WorkingTime: {} sec".format(end_time-start_time))
        

