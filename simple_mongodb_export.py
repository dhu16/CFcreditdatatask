#
# usage:
#
# python3 simple_mongodb_export.py --json ./files_formatted_records_in_json/formatted_requests.json --db 'carmino_data' --coll 'url_data' --many True --ObjectId '5e4ef6f3ea61c4adb36c7b3c'
#
# python3 simple_mongodb_export.py --json ./files_xml_data_in_json/xml_data_to_json.json --db 'carmino_data' --coll 'xml_data' --ObjectId '5e4ef70d1af7370cdec1d273'
#
#
# pymongo is the module to be installed by the following command
#
# pip3 install pymongo
#
#
# Installing collected packages: pymongo
# Successfully installed pymongo-3.10.1
#
import json
from pymongo import MongoClient
from bson.objectid import ObjectId

import os
import shutil
import argparse
import subprocess

current_file_path = __file__
current_file_dir = os.path.dirname(__file__)

exported_data_dirname='files_exported_data_in_json'

default_data_file=exported_data_dirname + '/exported_data.json'

default_db='camino_data'
default_collection='timed_task'


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-j", "--json",
	help="path to the json file")
ap.add_argument("-d", "--db",
	help="mongo db name")
ap.add_argument("-c", "--coll",
	help="mongo db collection name")
ap.add_argument("-m", "--many",
	help="many documents collection")
ap.add_argument("-o", "--ObjectId",
	help="find one document - object id")

args = vars(ap.parse_args())
# if json file url was not supplied, grab the reference
# to the default json url
if not args.get("json", False):
    json_file_to_import = default_data_file
# otherwise, grab a reference to the default json url
else:
	json_file_to_import = args["json"]

## --db option
if not args.get("db", False):
    mongodb_dbname = default_db
# otherwise, grab a reference to the default json url
else:
	mongodb_dbname = args["db"]
## --coll option
if not args.get("coll", False):
    mongodb_db_collectioname = default_collection
# otherwise, grab a reference to the default json url
else:
	mongodb_db_collectioname = args["coll"]
## many or one
if not args.get("many", False):
    many_documents_to_insert = False
# otherwise, grab a reference to the default json url
else:
	many_documents_to_insert = True
## Object Id to find one or many documents
if not args.get("ObjectId", False):
    object_id_str = 'ObjectId("5e4eea619c4c85f4a779257e")'
# otherwise, grab a reference to the default json url
else:
	object_id_str = args["ObjectId"]

if not os.path.exists(exported_data_dirname):
    os.mkdir(exported_data_dirname)
    print("Directory " , exported_data_dirname ,  " Created ")
else:
    print("Directory " , exported_data_dirname ,  " already exists")

## insert into MongoDB option #1
## using pymongo MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client[mongodb_dbname]
mongodb_collection_data = db[mongodb_db_collectioname]

if not many_documents_to_insert:
    document=mongodb_collection_data.find_one({"_id" : ObjectId(object_id_str)})
# otherwise, grab a reference to the default json url
else:
	document=mongodb_collection_data.find_one({"_id" : ObjectId(object_id_str)})

client.close()

print('Find One ' + object_id_str + ' from local MongoDB successfully.')

exported_json_file=exported_data_dirname + '/exported_' + object_id_str + '.json'
with open(exported_json_file, 'w+') as json_file:
    json.dump(document, json_file, ensure_ascii=False, indent=4, sort_keys=True, default=str)

print('saved exported document in formatted json in formatted_requests.json')
