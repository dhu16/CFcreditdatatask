#
# usage: to run with 10 minutes timer
#
# python3 timer_simple_parser.py --min 10 --url https://raw.githubusercontent.com/caminofinancial/data-eng-take-home/master/prequalresult.json
#
# to run parser task in background with 10 minutes timer
#
# python3 timer_simple_parser.py --min 10 --url https://raw.githubusercontent.com/caminofinancial/data-eng-take-home/master/prequalresult.json &
#
# or
#
# nohup python3 timer_simple_parser.py --min 10 --url https://raw.githubusercontent.com/caminofinancial/data-eng-take-home/master/prequalresult.json &
#
# to stop background running tasks - pid is the process id for process started above in back background
#
# kill pid
#

import os
import time
import argparse

default_minutes_to_run_timer=10
default_json_url = 'https://raw.githubusercontent.com/caminofinancial/data-eng-take-home/master/prequalresult.json'

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--min",
	help="minutes to run timer")
ap.add_argument("-u", "--url",
	help="path to the json file")

args = vars(ap.parse_args())

# check and read command argument --min
if not args.get("min", False):
    minutes_to_run_timer = default_minutes_to_run_timer

# otherwise, grab a reference to the default json url
else:
	minutes_to_run_timer = args["min"]
# if json file url was not supplied, grab the reference
# to the default json url
if not args.get("url", False):
    json_url = default_json_url

# otherwise, grab a reference to the default json url
else:
	json_url = args["url"]

while True:

	print("Parser Timer[" + str(minutes_to_run_timer) + " minutes] based task execution started @ " + time.ctime())

	os.system('python3 simple_parser.py --url ' + json_url)

	print("Parser Timer[" + str(minutes_to_run_timer) + " minutes] based task execution finished @ " + time.ctime())
	##time.sleep() takes seconds
	seconds_to_run_timer=int(minutes_to_run_timer)*60
	time.sleep(seconds_to_run_timer)
