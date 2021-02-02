from flask import Flask, request, jsonify
from flask_cors import CORS
from DataBase import DataBase
import json
app = Flask(__name__)
CORS(app)
database = DataBase()

@app.route("/")
def index():
    return "Hello"

@app.route("/CheckData", methods = ["POST"])
def CHK_postinput():
    '''
    get mess
    {
        "uid":"Vincent550102"
    }
    '''
    insert_val = request.get_json()
    db_mess = database.find_userdata(insert_val['uid'])
    '''
    return mess
    {
        "already":true or false,
        "time"123 or null,
        "score":87 or null
    }
    '''
    return jsonify(db_mess)

@app.route("/InsertData", methods = ["POST"])
def INSERT_postinput():
    insert_val = request.get_json()
    '''
    {
        "uid":"Vincent550102",
        "time":123,
        "score":87
    }
    '''
    '''
        1 = OK already edit
        2 = OK no this user but already add
    '''
    return jsonify(database.insert_data(insert_val))

@app.route('/Alldatas',methods = ["GET"])
def Show_alldata():
    datas = database.find_all_userdata()
    return jsonify({"datas":datas})

if __name__ == '__main__':
    app.run()