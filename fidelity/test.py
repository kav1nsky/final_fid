# -*- coding: utf-8 -*-

import requests
import os;

url = "http://127.0.0.1:8888/v1/chain/get_account"
payload = "{\"account_name\":\"contract\"}"
response = requests.request("POST", url, data=payload)
print(response.text)

url = "http://127.0.0.1:8888/v1/chain/get_table_rows"
payload = "{\"scope\":\"contract\",\"code\":\"contract\",\"table\":\"workers\",\"json\":\"true\",\"lower_bound\":\"test2\",\"upper_bound\":\"test3\"}"
response = requests.request("POST", url, data=payload)
print(response.text)

command = "cleos wallet unlock --password PW5KY9f968EERGZ6rRKjgp4B4FUbP2AMNYqExbxkoJNUV4QejTCkb"
os.system(command)

id = 2
command = "cleos create account eosio zaluper" + str(id) + " EOS8gXKHtvWLTpcDvYv9qSdPAPZKtGE9K4RAUkqjgdmwqhgCNZez4"
os.system(command)

command = "cleos push action contract setworker '[\"zaluper" + str(id) + "\", \"Random Username\"]' -p zaluper" + str(id) + "@active"
os.system(command)

url = "http://127.0.0.1:8888/v1/chain/get_table_rows"
payload = "{\"scope\":\"contract\",\"code\":\"contract\",\"table\":\"workers\",\"json\":\"true\",\"lower_bound\":\"zaluper" + str(id) + "\",\"upper_bound\":\"zaluper" + str(id + 1) + "\"}"
response = requests.request("POST", url, data=payload)
print(response.text)
