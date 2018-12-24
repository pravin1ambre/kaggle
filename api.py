from flask import Flask, render_template, Response
from flask_restful import Resource, Api
from flask_cors import CORS
from flask import jsonify
import glob
import os
import datetime
import time
# from flask_mysqldb import MySQL
import csv
from zipfile import ZipFile
import glob
import ast
import json
import base64
import shutil 
import pandas as pd
import re
import requests
import io
import urllib3
http = urllib3.PoolManager()
app = Flask(__name__)
api = Api(app)
CORS(app)

# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine
# engine = create_engine('mysql://root:admin@localhost/io_dataload',echo=False)

#database configration with class

# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'Dad@12345'
# app.config['MYSQL_DB'] = 'io_dataload'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql = MySQL(app)



class Competitions(Resource):
    def get(self):
        
        # url = "https://www.kaggle.com/competitions.json?sortBy=grouped&group=general&page=1&pageSize=20"
        try:
            # urlData = requests.get(url).content
            url = http.request('GET', 'https://www.kaggle.com/competitions.json?sortBy=grouped&group=general&page=1&pageSize=20')
        except requests.ConnectionError:
            return "Connection Error"  
        rawData = pd.read_table(io.StringIO(url.data.decode('utf-8')),index_col=False)
        all_raw_data = list(rawData.columns.values)
        all_raw_data = json.loads(all_raw_data[0])
        print(all_raw_data)
        all_leaderboards = []
        for i in range(0,len(all_raw_data['pagedCompetitionGroup']['competitions'])):
            competitionId = all_raw_data['pagedCompetitionGroup']['competitions'][i]['competitionId']
            print(competitionId,'-----------competionId--------------')
            leaderboard = "https://www.kaggle.com/c/{}/leaderboard.json?includeBeforeUser=false&includeAfterUser=false".format(competitionId)
            try:
                uResponse = requests.get(leaderboard)
            except requests.ConnectionError:
                return "Connection Error"  
            Jresponse = uResponse.text
            all_leaderboards.append(json.loads(Jresponse))
        return all_leaderboards
        # from pandas.io.json import json_normalize
        
        # from flask_jsonpify import jsonpify
        # df_list = rawData.values.tolist()
        # JSONP_data = jsonpify(df_list)
        # return JSONP_data
        # print('----------------------------------------')

        # return jsonify(rawData)  

class Leaderboard(Resource):
    def get(self):
        uri = "https://www.kaggle.com/c/9933/leaderboard.json?includeBeforeUser=false&includeAfterUser=false"
        try:
            uResponse = requests.get(uri)
        except requests.ConnectionError:
            return "Connection Error"  
        Jresponse = uResponse.text
        data = json.loads(Jresponse)
        # jsonify({'data':1233}) 
        return data

api.add_resource(Competitions, '/competitions')
api.add_resource(Leaderboard, '/leaderboard')

if __name__ == '__main__':
    app.run(port="5001", debug=True)