#!/usr/bin/python
""" uploadToEMRYS
PURPOSE: upload data to emrys

Read a newline delimited list of JSON objects and upload to emrys for analysis.

To determine your ingestion url, go to project emrys data services
(https://portal.projectemrys.com/data_services), select "Ingest", and use that url.
Or invoke the right click menu from "Ingest" and copy the link address.

To convert a csv file into json format for upload, use csvkit
    (http://csvkit.readthedocs.io)
$ csvjson --stream csv-file > json-file

"""

import os
import sys
import getopt
import requests

# script constants (hard codes)
HTTP_CREATION_SUCCESS = 201


def print_script_usage():
    """ Lists instructions for using this script
    """

    print "Usage: "
    print "{} -h | -f <filename> -u <url>".format(sys.argv[0])
    print "-h: lists script usage syntax"
    print "-f <filename> is the file of newline delimited JSON objects to load into emrys"
    print "-u <url> is the user-specific emrys load url"


def upload_json_data(json_list_file,emrys_load_url):
    """ Loads data into emrys

    Args: a file of newline delimited JSON objects

    Returns: none

    Raises:
        IOError: if input file is not found
        General: if record is not successfully created on emrys

    """
 
    # identify datafile & ensure it exits
    try:
        if not  (os.path.isfile(json_list_file)):
            raise IOError

    except IOError, arg:
        print "IOError: Cannot find datafile '{0}': {1}".format(json_list_file,str(arg))

    # load data
    try:
        headers = {}
        file_handle = open (json_list_file, 'r')

        for json_obj in file_handle:
            # remove trailing newline
            json_record = json_obj.rstrip()
            #load record
            result = requests.post(emrys_load_url,data=json_record,headers=headers, verify=False)
            if (result.status_code != HTTP_CREATION_SUCCESS):
                err = "data load failed with %d. JSON object was: %s" % result,json_record
                raise Exception(err)

    except :
        print("Exception: %s, %s" % sys.exc_info()[0],sys.exc_info()[1])


# MAIN
def main():

    file = None
    url = None

    # Read command line args
    myopts, args = getopt.getopt(sys.argv[1:], "f:u:")

    ###############################
    # o == option
    # a == argument passed to the o
    ###############################
    for o, a in myopts:
        if o == '-f':
            file = a
        elif o == '-u':
            url = a
        elif o == '-h':
            print_script_usage()
            return
        else:
            print_script_usage()
            return

    if (file != None and url != None):
        upload_json_data(file,url)
    else:
        print_script_usage()


if __name__ == "__main__":

    main()
    print ("Exiting emrys data load script")

# references:
# http://www.cyberciti.biz/faq/python-command-line-arguments-argv-example/