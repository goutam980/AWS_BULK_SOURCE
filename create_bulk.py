import csv
import requests
import check_user_prem
import os
import json
from requests.auth import HTTPBasicAuth
import enum
import argparse
import confirm
# not used in the code, just in case required
# but it is being refered in the request.json.tmpl


parser = argparse.ArgumentParser(
    description='Create bulk data from a CSV file.')
parser.add_argument('--user', required=True,
                    help='The Sources RedHat username.')
parser.add_argument('--password', required=True,
                    help='The Sources RedHat password.')
parser.add_argument('--input_file', required=True, help='The input CSV file.')
args = parser.parse_args()


class APPLICATION_TYPE_ID(enum.Enum):
    COST_MANAGEMENT = 2
    RHEL_MANAGEMENT = 5
    LAUNCH_IMAGES = 8


# URLs
CREATE_REQUEST_URL = "https://console.redhat.com/api/sources/v3.1/bulk_create"
HEALTH_CHECK_URL = "https://console.redhat.com/api/sources/v3.1/"


def do_create_request(url, auth_obj, request_body):
    '''
        given auth obj and request obj, creates the source in sources.redhat.com
    '''
    response = requests.post(url, auth=auth_obj, json=request_body)
    print(response.json())
    if response.status_code != 201:
        return False
    else:
        return True


def do_healthcheck_request(url, auth_obj):
    '''
        given auth obj does the healthcheck in sources.redhat.com
    '''
    check_user_prem
    response = requests.get(
        url, auth=auth_obj)
    if not response.ok:
        return False
    else:
        return True


def convert_row_to_json(request_template, row):
    '''
        given request template , and the data in a list format returns the request as dict 
    '''
    return json.loads(request_template.replace("{source_name}", row[0]).replace("{access_key_id}", row[1]).replace("{access_secret_key_id}", row[2]))


def usage():
    '''
        provides the usage of the program
    '''
    print("Make sure to provide add the acconts details with appropiate permission in order to create the source")

    print("INPUT=<INPUT_CSV_FILE> USER=<YOUR_SOURCES_REDHAT_USERNAME> PASSWORD=<YOUR_SOURCES_REDHAT_PASSWORD> python3 create_bulk.py")


def confirm_gold_image():
    confirm.All_redhat()




if __name__ == "__main__":

    # get/prepare all the  variables
    try:
        USER = args.user
        PASSWORD = args.password
        INPUT = args.input_file
    except KeyError as e:
        usage()
        exit(1)

    # basic authentication
    auth_obj = HTTPBasicAuth(USER, PASSWORD)

    with open('files/request.json.tmpl') as template_file:
        request_template = json.dumps(json.load(template_file))

    # perform the healthcheck
    if do_healthcheck_request(HEALTH_CHECK_URL, auth_obj):
        print("Request failed with status code")
        exit(1)
    else:
        print("Sucess Health check")

    # read the csv file
    try:
        with open(INPUT, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip the header
            requests_body = {row[0]: convert_row_to_json(request_template, row)
                            for row in reader if len(row) >= 3}
    except FileNotFoundError:
        print(f"{INPUT} not found")
        exit(1)

    # for each row, do a create request
    for name, body in requests_body.items():
        if do_create_request(CREATE_REQUEST_URL, auth_obj, body):
            print(f"Source created for {name}")
        else:
            print(f"Failed to create source for {name}")
            a = input("To check the user permission press enter 1")
            if a == str(1):
                url_b = "https://console.redhat.com/api/rbac/v1/principals/"
                print(check_user_prem(url_b, auth_obj))
