import csv
import requests
import os
import json
from requests.auth import HTTPBasicAuth
import enum


# output_1=os.system("curl -s --fail -u USERNAME:PASSWORD https://console.redhat.com/api/rbac/v1/principals/?limit=0&offset=0&match_criteria=partial&usernames=XXXXX&sort_order=asc&status=all/data")
# url_a = "https://console.redhat.com/api/rbac/v1/principals/"


# auth_obj = HTTPBasicAuth(USER, PASSWORD)


# def check_user_prem(url_a, auth_obj):
#     response = requests.get(url=url_a, auth=auth_obj)
#     req_res = response.json()
#     print(type(req_res))
#     user_data = req_res.get('data')
#     a = 0
# # // source admin Permission check

#     for i in user_data:
#         print("==================================================")
#         b = i
#         if b['is_org_admin'] == True:
#             org_username = b['username']
#             print("org admin detected")
#             print(org_username)
# # // rbac source admin should be enabled
#     # if USER in user_data["Username"]:
#     #     print("availabel")
#     # else:
#     #     print("nothing is ther")


# check_user_prem(url_a, auth_obj)
