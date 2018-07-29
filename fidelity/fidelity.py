# -*- coding: utf-8 -*-

import requests
import subprocess
import os
import json

class Fidelity:
    walletPassword = ""
    url = "http://127.0.0.1:8888/v1/chain/get_table_rows"

    def unlock(self):
        subprocess.Popen(["cleos", "wallet", "unlock", "--password", self.walletPassword])

    def __init__(self, _walletPassword = "PW5KY9f968EERGZ6rRKjgp4B4FUbP2AMNYqExbxkoJNUV4QejTCkb"):
        self.walletPassword = _walletPassword

    def createAccount(self, id):
        keys = subprocess.check_output(["cleos", "create", "key"]).split()
        privateKey = keys[2].decode('utf-8')
        publicKey = keys[5].decode('utf-8')
        self.unlock()
        subprocess.Popen(["cleos", "wallet", "import", "--private-key", privateKey])
        subprocess.Popen(["cleos", "create", "account", "eosio", "user" + str(id), publicKey])

        return (privateKey, publicKey, "user" + str(id))

    # Actions

    def setWorker(self, account, name):
        self.unlock()
        account = account
        name = name
        #os.system("cleos push action contract setworker '[\"" + account + "\", \"" + name + "\"]' -p " + account + "@active")
        subprocess.Popen(["cleos", "push", "action", "contract", "setworker", "[\'" + account.encode('utf-16') + "\', \'" + name.encode('utf-16') + "\']",
        '-p', account + "@active"])


    def addInfo(self, account, content):
        self.unlock()
        #os.system("cleos push action contract addinfo '[\"" + account + "\", \"" + content + "\"]' -p " + account + "@active")
        str1 = "push action contract addinfo '[\"" + account + "\", \"" + content + "\"]' -p " + account + "@active"
        subprocess.Popen(["cleos", str1])

    def setCustomer(self, account, name, info):
        self.unlock()
        #os.system("cleos push action contract setcustomer '[\"" + account + "\", \"" + name + "\", \"" + info + "\"]' -p " + account + "@active")
        str1 = "push action contract setcustomer '[\"" + account + "\", \"" + name + "\", \"" + info + "\"]' -p " + account + "@active"
        subprocess.Popen(["cleos", str1])

    def initAgreement(self, account, target, content, due):
        self.unlock()
        #os.system("cleos push action contract initagr '[\"" + account + "\", \"" + target + "\", \"" + content + "\", " + str(due) + "]' -p " + account + "@active")
        str1 = "push action contract initagr '[\"" + account + "\", \"" + target + "\", \"" + content + "\", " + str(due) + "]' -p " + account + "@active"
        subprocess.Popen(["cleos", str1])

    def acceptAgreement(self, account, id):
        self.unlock()
        #os.system("cleos push action contract acceptagr '[\"" + account + "\", " + str(id) + "]' -p " + account + "@active")
        str1 = "push action contract acceptagr '[\"" + account + "\", " + str(id) + "]' -p " + account + "@active"
        subprocess.Popen(["cleos", str1])

    def rejectAgreement(self, account, id):
        self.unlock()
        #os.system("cleos push action contract rejectagr '[\"" + account + "\", " + str(id) + "]' -p " + account + "@active")
        str1 = "push action contract rejectagr '[\"" + account + "\", " + str(id) + "]' -p " + account + "@active"
        subprocess.Popen(["cleos", str1])

    def putRecord(self, account, id, rating, comment):
        self.unlock()
        #os.system("cleos push action contract putrecord '[\"" + account + "\", " + str(id) + ", " + str(rating) + ", \"" + comment + "\"]' -p " + account + "@active")
        str1 = "push action contract putrecord '[\"" + account + "\", " + str(id) + ", " + str(rating) + ", \"" + comment + "\"]' -p " + account + "@active"
        subprocess.Popen(["cleos", str1])

    # Data calls

    def getWorker(self, account):
        payload = "{\"scope\":\"contract\",\"code\":\"contract\",\"table\":\"workers\",\"json\":\"true\",\"lower_bound\":\"" + account + "\", \"upper_bound\":\"" + account + "1" + "\"}"
        response = requests.request("POST", self.url, data=payload)
        responsejson = json.loads(response.text)
        print(responsejson)
        return responsejson["rows"][0]

    def getCustomer(self, account):
        payload = "{\"scope\":\"contract\",\"code\":\"contract\",\"table\":\"customers\",\"json\":\"true\",\"lower_bound\":\"" + account + "\", \"upper_bound\":\"" + account + "1" + "\"}"
        response = requests.request("POST", self.url, data=payload)
        responsejson = json.loads(response.text)
        return responsejson[u"rows"][0]

    def getAgreement(self, id):
        payload = "{\"scope\":\"contract\",\"code\":\"contract\",\"table\":\"agreements\",\"json\":\"true\",\"lower_bound\":\"" + str(id) + "\", \"upper_bound\":\"" + str(id + 1) + "1" + "\"}"
        response = requests.request("POST", self.url, data=payload)
        responsejson = json.loads(response.text)
        return responsejson["rows"][0]

    def getRecord(self, id):
        payload = "{\"scope\":\"contract\",\"code\":\"contract\",\"table\":\"records\",\"json\":\"true\",\"lower_bound\":\"" + str(id) + "\", \"upper_bound\":\"" + str(id + 1) + "1" + "\"}"
        response = requests.request("POST", self.url, data=payload)
        responsejson = json.loads(response.text)
        return responsejson["rows"][0]
