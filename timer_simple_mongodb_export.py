#
# usage:
#
# python3 timer_simple_mongodb_export.py --min 10 --json ./files_formatted_records_in_json/formatted_requests.json --db 'carmino_data' --coll 'url_data' --many True --ObjectId '5e4ef6f3ea61c4adb36c7b3c'
#
# python3 timer_simple_mongodb_export.py --min 10 --json ./files_xml_data_in_json/xml_data_to_json.json --db 'carmino_data' --coll 'xml_data' --ObjectId '5e4ef70d1af7370cdec1d273'
#
# to run as background tasks
#
# python3 timer_simple_mongodb_export.py --min 10 --json ./files_formatted_records_in_json/formatted_requests.json --db 'carmino_data' --coll 'url_data' --many True --ObjectId '5e4ef6f3ea61c4adb36c7b3c' &
#
# python3 timer_simple_mongodb_export.py --min 10 --json ./files_xml_data_in_json/xml_data_to_json.json --db 'carmino_data' --coll 'xml_data' --ObjectId '5e4ef70d1af7370cdec1d273' &
#
# or
#
# nohup python3 timer_simple_mongodb_export.py --min 10 --json ./files_formatted_records_in_json/formatted_requests.json --db 'carmino_data' --coll 'url_data' --many True --ObjectId '5e4ef6f3ea61c4adb36c7b3c' &
#
# nohup python3 timer_simple_mongodb_export.py --min 10 --json ./files_xml_data_in_json/xml_data_to_json.json --db 'carmino_data' --coll 'xml_data' --ObjectId '5e4ef70d1af7370cdec1d273' &
#
#
# to stop background running tasks - pid is the process id for process started above in back background
#
# kill pid
#

import os
import time
import argparse

default_minutes_to_run_timer=10
exported_data_dirname='files_exported_data_in_json'
default_data_file=exported_data_dirname + '/exported_data.json'
default_db='camino_data'
default_collection='timed_task'

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-mi", "--min",
	help="minutes to run timer")
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

# check and read command argument --min
if not args.get("min", False):
    minutes_to_run_timer = default_minutes_to_run_timer

# otherwise, grab a reference to the default json url
else:
	minutes_to_run_timer = args["min"]
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
## Object Id to find one or many documents
if not args.get("ObjectId", False):
    object_id_str = 'ObjectId("5e4eea619c4c85f4a779257e")'
# otherwise, grab a reference to the default json url
else:
	object_id_str = args["ObjectId"]

while True:

	print("Exporter Timer [" + str(minutes_to_run_timer) + " minutes] based task execution started at " + time.ctime())

	## insert one document
	if not many_documents_to_insert:
	    os.system('python3 simple_mongodb_export.py --json ' + json_file_to_import + ' --db ' + mongodb_dbname +' --coll ' + mongodb_db_collectioname + ' --ObjectId ' + object_id_str )
	## otherwise, insert many documents
	else:
		os.system('python3 simple_mongodb_export.py --json ' + json_file_to_import + ' --db ' + mongodb_dbname +' --coll ' + mongodb_db_collectioname + ' --many True' + ' --ObjectId ' + object_id_str )

	print("Exporter Timer [" + str(minutes_to_run_timer) + " minutes] based task execution finished at " + time.ctime())
	##time.sleep() takes seconds
	seconds_to_run_timer=int(minutes_to_run_timer)*60
	time.sleep(seconds_to_run_timer)
