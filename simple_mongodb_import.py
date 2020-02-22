#
# usage:
#
# python3 simple_mongodb_import.py --json ./files_formatted_records_in_json/formatted_requests.json --db 'carmino_data' --coll 'url_data' --many True
#
# python3 simple_mongodb_import.py --json ./files_xml_data_in_json/xml_data_to_json.json --db 'carmino_data' --coll 'xml_data'
#
#
# pymongo is the module to be installed by the following command
#
# pip3 install pymongo
#
# Installing collected packages: pymongo
# Successfully installed pymongo-3.10.1
#
import json
from pymongo import MongoClient

import os
import shutil
import argparse
import subprocess

current_file_path = __file__
current_file_dir = os.path.dirname(__file__)

imported_data_dirname='files_imported_data_in_json'

default_data_file=imported_data_dirname + '/imported_data.json'

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

if not args.get("many", False):
    many_documents_to_insert = False
# otherwise, grab a reference to the default json url
else:
	many_documents_to_insert = True

if not os.path.exists(imported_data_dirname):
    os.mkdir(imported_data_dirname)
    print("Directory " , imported_data_dirname ,  " Created ")
else:
    print("Directory " , imported_data_dirname ,  " already exists")

## insert into MongoDB option #1
## using pymongo MongoClient
client = MongoClient('127.0.0.1', 27017)
db = client[mongodb_dbname]
collection_credit_data = db[mongodb_db_collectioname]

with open(json_file_to_import) as f:
    loaded_json_file_to_import = json.load(f)

## Successfully installed pymongo-3.10.1
#
## if pymongo < 3.0, use insert()
##collection_credit_data.insert(loaded_json_file_to_import)

## if pymongo >= 3.0 use insert_one() for inserting one document
#collection_credit_data.insert_one(loaded_json_file_to_import)

## if pymongo >= 3.0 use insert_many() for inserting many documents
#collection_credit_data.insert_many(loaded_json_file_to_import)
post_id=mongodb_db_collectioname
if not many_documents_to_insert:
    post_id=collection_credit_data.insert_one(loaded_json_file_to_import).inserted_id
# otherwise, grab a reference to the default json url
else:
	post_id=collection_credit_data.insert_many(loaded_json_file_to_import).inserted_ids
print('[Post Id] ', post_id)
client.close()

print('Saved ' + json_file_to_import + ' into local MongoDB successfully.')

## copy imported file to import folder - to record files that's been imported already
##
newPath = shutil.copy(json_file_to_import, imported_data_dirname + '/' + str(post_id) + '.json')
print('Copied imported file to new location: ' + newPath)

## insert into MongoDB option #2
##
## using mongoimport command line with Python subprocess.run()
##
## mongoimport --db databaseName --collection tableName --file filepath.json
## mongoimport --host <host_name>:<host_port> --db <database_name> --collection <collection_name>  --file <path_to_dump_file> -u <my_user> -p <my_pass>
##

# test subprocess.run()
# replace "ls -l" with mongoimport command similar above when inserting to MongoDB
# un-comment pymongo client code lines above first
##
## subprocess.run(["ls", "-l"])

#cp = subprocess.run(["ls","-lha"], universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

#if not cp.returncode==0:
#	print(cp.stderr)
#else:
#	print(cp.stdout)
#	print(cp.returncode)

##with open(imported_xml_data_dirname + '/' + mongodb_db_collectioname + '.json', 'w+') as json_file:
    ##json.dump(loaded_json_file_to_import, json_file, ensure_ascii=False, indent=4, sort_keys=True)
