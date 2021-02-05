# -*- coding: UTF-8 -*-
import os
from flask import Flask, request, jsonify, render_template, render_template_string
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, decode_token
)
from app.DataBase import DataBase
import json

app = Flask(__name__)
CORS(app, resources={r"./*": {"origins": "none"}})
database = DataBase()
jwt = JWTManager()#https://vincent550102.github.io

app.config['JWT_SECRET_KEY'] = str(os.urandom(64).hex())
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
    decode = decode_token(request.headers['Authorization'].split('Bearer ')[-1])['identity']
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
    if insert_val['score'] > 1000 or insert_val['time'] < 0 or decode!=insert_val['uid']:
        return render_template_string("cheat you")
    return jsonify(render_template_string(database.insert_data(insert_val)))

@app.route('/Alldatas',methods = ["GET"])
def Show_alldata():
    datas = database.find_all_userdata()
    return jsonify({"datas":datas})

if __name__ == '__main__':
    app.run()