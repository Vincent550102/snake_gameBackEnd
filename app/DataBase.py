# -*- coding: UTF-8 -*-
import json
from pymongo import MongoClient#,dnspython
from operator import itemgetter, attrgetter

class DataBase():
    def __init__(self):
        client = MongoClient('mongodb+srv://Vincent550102:Vincent55920102@cluster0.khbuw.mongodb.net/snake_game?retryWrites=true&w=majority')
        #mongodb+srv://Vincent550102:Vincent55920102@cluster0.khbuw.mongodb.net/snake_game?retryWrites=true&w=majority

        self.db = client["snake_game"]
        self.db_userdatas = self.db['userdata']
    def insert_data(self,obj):
        status_mess = ""
        if self.db_userdatas.find_one({'uid': obj['uid']}):
            self.db_userdatas.update_one({"uid":obj['uid']},{
                '$set' : {
                    "time":obj['time'],
                    "score":obj['score']
                }
            })
            status_mess = "1"
        else:
            self.db_userdatas.insert_one({
                "uid":obj['uid'],
                "time":obj['time'],
                "score":obj['score']
            })
            status_mess = "2"
        return status_mess

    def find_userdata(self,uid):
        return_mess = dict()
        if self.db_userdatas.find_one({'uid': uid}):
            udata = self.db_userdatas.find_one({'uid': uid})
            return_mess = {
                "already":True,
                "time":udata["time"],
                "score":udata['score']
            }
        else:
            return_mess = {
                "already":False
            }
        return return_mess

    def find_all_userdata(self):
        return_mess = list()
        udatas = self.db_userdatas.find()
        for data in udatas:
            del data['_id']
            return_mess.append(data)
        return_mess.sort(key = itemgetter("score","time"),reverse=True)
        return return_mess

if __name__ == "__main__":
    pass
    # database = DataBase()
    # database.insert_data({
    #     "uid":"jeff",
    #     "time":10,
    #     "score":70
    # })
    # for i in database.find_all_userdata():
    #     print(i)

