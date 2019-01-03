from flask import Flask, render_template, Response,request
from flask_restful import Resource, Api
from flask_cors import CORS
import os
import json
import pandas as pd
import re
import requests
import io
import urllib3
from models import *
http = urllib3.PoolManager()
app = Flask(__name__)
api = Api(app)
CORS(app)


class Competitions(Resource):
    def get(self):
        headers = request.headers
        try:
            url = http.request('GET', 'https://www.kaggle.com/competitions.json?sortBy=grouped&group=general&page=1&pageSize=20')
            url_header = url.headers
        except requests.ConnectionError:
            return "Connection Error"
        rawData = pd.read_table(io.StringIO(url.data.decode('utf-8')),index_col=False)
        all_raw_data = list(rawData.columns.values)
        all_raw_data = json.loads(all_raw_data[0])
        all_leaderboards = []
        all_data = pd.DataFrame()
        for i in range(0,len(all_raw_data['pagedCompetitionGroup']['competitions'])):
            competitionId = all_raw_data['pagedCompetitionGroup']['competitions'][i]['competitionId']
            leaderboard = "https://www.kaggle.com/c/{}/leaderboard.json?includeBeforeUser=false&includeAfterUser=false".format(competitionId)
            try:
                uResponse = requests.get(leaderboard)
            except requests.ConnectionError:
                return "Connection Error"  
            Jresponse = uResponse.text
            data = json.loads(Jresponse)['submissions']
            
            df = pd.DataFrame(data, columns=['rank', 'teamId', 'entries', 'score', 'medal', 'teamName'])
            all_data = all_data.append(df)
        all_data.to_csv('data.csv',  index=False)
        return {'msg':  "Successfully Uploaded"}


# class Leaderboard(Resource):
#     def get(self):
#         uri = "https://www.kaggle.com/c/9933/leaderboard.json?includeBeforeUser=false&includeAfterUser=false"
#         try:
#             uResponse = requests.get(uri)
#         except requests.ConnectionError:
#             return "Connection Error"  
#         Jresponse = uResponse.text
#         data = json.loads(Jresponse)
#         # jsonify({'data':1233}) 
#         return data

api.add_resource(Competitions, '/competitions')

if __name__ == '__main__':
    app.run(port="5001", debug=True)