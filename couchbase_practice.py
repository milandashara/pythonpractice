__author__ = 'milanashara'
import json
from couchbase.bucket import Bucket
from couchbase_pool import Pool
from couchbase.views.params import STALE_OK, Query
import ConfigParser
import os
import logging

ids=["GB.4698.5772.20150817.21",
"RU.5227.16931.20150902.15",
"JP.13068.14213.20150920.6",
"GB.4698.5947.20150815.12",
"RU.5227.6781.20150912.8",
"JP.13068.14213.20150920.7",
"IE.11154.14151.20150919.2",
"GB.11316.15434.20150928.7",
"RU.17620.12191.20151031.7"]
bucket = Bucket('http://skysgd112.corp.skyscanner.local/default',password='')
#print bucket.get(ids[2])


#bucket1=Bucket('http://localhost1/default')

path_to_config_file = os.path.dirname(os.path.realpath(__file__)) + '/couchbase.ini'
config = ConfigParser.ConfigParser()
config.read(path_to_config_file)

# def insert():
#     for id in ids:
#         bucket1.insert(id,json.loads(bucket.get(id).value))

def get(document_id):
    return bucket.get(document_id)

print get("AU.10041.13416.20150825.23").value

travel_rankings_pool = Pool(initial=config.getint('travelrankings_pool', 'min'),
                            max_clients=config.getint('travelrankings_pool', 'max'),
                            connstr=config.get('travelrankings_pool', 'connstr'),
                            )

q = Query(stale=STALE_OK,
                  startkey=['fnus','US'], endkey=['fnus','US',Query.STRING_RANGE_END],

                  limit=100,
                  skip=0)

print list(travel_rankings_pool.get_resultset_from_view("dev_%2Ftest","test",q))
