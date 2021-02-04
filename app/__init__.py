# -*- coding: UTF-8 -*-
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from app.DataBase import DataBase
import json

app = Flask(__name__)
CORS(app)
database = DataBase()

jwt = JWTManager()

app.config['JWT_SECRET_KEY'] = 'catcatcat314159hahafoundit'
jwt.init_app(app)

@app.route('/catcatGettok', methods=['POST'])
def login():
    uid = request.json.get('uid', None)
    access_token = create_access_token(identity=uid)
    return jsonify(access_token=access_token)


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
@jwt_required
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