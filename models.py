from pymodm import connect
from pymodm import MongoModel, fields
from pymongo.write_concern import WriteConcern

connect("mongodb://localhost:27017/kaggle", alias="kaggle-app")

class Leaderboard(MongoModel):
    rank     = fields.CharField()
    teamId   = fields.CharField()
    entries  = fields.CharField()
    score    = fields.CharField()
    medal    = fields.CharField()
    teamName = fields.CharField()

    class Meta:
        connection_alias = 'kaggle-app'
        write_concern = WriteConcern(j=True)

