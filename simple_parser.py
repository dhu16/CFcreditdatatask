#
# usage:
#
# python3 simple_parser.py --url https://raw.githubusercontent.com/caminofinancial/data-eng-take-home/master/prequalresult.json
#
#
# xmltodict is the module to be installed by the following command
#
# pip3 install xmltodict
#
import xmltodict, json
from json import dumps

import os
import argparse

#
# requests is the module to be installed by the following command
#
# pip3 install requests
#
import requests

#
# utility module that contains
# class to search any attribute value from
# complex json objects.
#
from utility import DictQuery

formatted_records_dirname='files_formatted_records_in_json'
xml_data_dirname='files_xml_data_in_json'
default_json_url = 'https://raw.githubusercontent.com/caminofinancial/data-eng-take-home/master/prequalresult.json'

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-u", "--url",
	help="json file path")

args = vars(ap.parse_args())
# if json file url was not supplied, grab the reference
# to the default json url
if not args.get("url", False):
    json_url = default_json_url

# otherwise, grab a reference to the default json url
else:
	json_url = args["url"]

# creates the folders or states its existence
if not os.path.exists(formatted_records_dirname):
    os.mkdir(formatted_records_dirname)
    print("Directory " , formatted_records_dirname ,  " Created ")
else:
    print("Directory " , formatted_records_dirname ,  " already exists")

if not os.path.exists(xml_data_dirname):
    os.mkdir(xml_data_dirname)
    print("Directory " , xml_data_dirname ,  " Created ")
else:
    print("Directory " , xml_data_dirname ,  " already exists")
#
# requests.get to download json file
# build Python Dictionary
#
creditdata_listofdict = requests.get(json_url).json()

# read local json file
# build Python Dictionary
#with open('sample_credit_data.json', 'r') as f:
#    data_listofdict = json.load(f)

# loop through the built Python Dictionary
# and print out some attributes
#
print('looping - parse the content and print some key fields')
for item in creditdata_listofdict:
    if "model" in item:
        print('model: ', item['model'])
    if "pk" in item:
        print('pk: ', item['pk'])
    if "fields" in item:
        # read nested xml_data - the xml content
        # using utility class from self made utility
        xml_data_item=DictQuery(item).get('fields/xml_data')
        print('read xml_data')
        #print('xml_data: %s', xml_data_item)
        ## convert xml_data - xml content to json content
        xml_dict=xmltodict.parse(xml_data_item)
        print('convert xml_data to json')
        #print(json.dumps(xml_dict))
        #
        # write converted json content to a file
        with open(xml_data_dirname + '/xml_data_to_json.json', 'w+') as json_file:
            json.dump(xml_dict, json_file, ensure_ascii=False, indent=4, sort_keys=True)
        print('saved xml_data in formatted json in xml_data_to_json.json')
        # to do
        # write converted json content to MongoDB
        #
        # print some attributes
        print('print some fields level attributes')
        print('fields/loanapp_id: ', DictQuery(item).get('fields/loanapp_id'))
        print('fields/result: ', DictQuery(item).get('fields/result'))
        print('fields/fico_v2: ', DictQuery(item).get('fields/fico_v2'))
        print('fields/role: ' + DictQuery(item).get('fields/role'))
        print('fields/username: ' + DictQuery(item).get('fields/username'))
        print('fields/report_type: ' + DictQuery(item).get('fields/report_type'))
        print('fields/created_at: ' + DictQuery(item).get('fields/created_at'))
        print('fields/version: ' + DictQuery(item).get('fields/version'))

# Write python dictionary to JSON like so
# Use 'indent' and 'sort_keys' to make the JSON
# file look nice
#
with open(formatted_records_dirname + '/formatted_requests.json', 'w+') as json_file:
    json.dump(creditdata_listofdict, json_file, ensure_ascii=False, indent=4, sort_keys=True)
print('saved requests in formatted json in formatted_requests.json')
