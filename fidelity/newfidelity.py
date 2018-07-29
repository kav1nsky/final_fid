import requests
import subprocess
import os
import json

class Fidelity:
    walletPassword = ""
    url = "http://127.0.0.1:8888/v1/chain/get_table_rows"

    def __init__(self, passw = "PW5KY9f968EERGZ6rRKjgp4B4FUbP2AMNYqExbxkoJNUV4QejTCkb"):
        self.walletPassword = passw

    def unlock(self):
        os.system("cleos wallet unlock --password " + self.walletPassword)

    def createAccount(self, account):
        keys = subprocess.check_output(["cleos", "create", "key"]).split()
        privateKey = keys[2].decode('utf-8')
        publicKey = keys[5].decode('utf-8')

        self.unlock()

        os.system("cleos wallet import --private-key " + privateKey)
        os.system("cleos create account eosio " + account + " " + publicKey)

        return privateKey, publicKey

    def setWorker(self, account, name):
        self.unlock()
        os.system("cleos push action contract setworker '[\"" + account + "\", \"" + name + "\"]' -p " + account + "@active")

    def addInfo(self, account, info):
        self.unlock()
        os.system("cleos push action contract addinfo '[\"" + account + "\", \"" + info + "\"]' -p " + account + "@active")

    def getWorker(self, account):
        payload = "{\"scope\":\"contract\",\"code\":\"contract\",\"table\":\"workers\",\"json\":\"true\",\"lower_bound\":\"" + account + "\", \"upper_bound\":\"" + account + "1" + "\"}"
        response = requests.request("POST", self.url, data=payload)
        responsejson = json.loads(response.text)
        try:
            return responsejson['rows'][0]
        except:
            return "failed"

    def setCustomer(self, account, name, info):
        self.unlock()
        os.system("cleos push action contract setcustomer '[\"" + account + "\", \"" + name + "\", \"" + info + "\"]' -p " + account + "@active")

    def getCustomer(self, account):
        payload = "{\"scope\":\"contract\",\"code\":\"contract\",\"table\":\"customers\",\"json\":\"true\",\"lower_bound\":\"" + account + "\", \"upper_bound\":\"" + account + "1" + "\"}"
        response = requests.request("POST", self.url, data=payload)
        responsejson = json.loads(response.text)
        try:
            return responsejson['rows'][0]
        except:
            return "failed"

    def initAgreement(self, account, target, content, due):
        self.unlock()
        os.system("cleos push action contract initagr '[\"" + account + "\", \"" + target + "\", \"" + content + "\", \"" + due + "\"]' -p " + account + "@active")

    def getAgreement(self, account, id):
        payload = "{\"scope\":\"contract\",\"code\":\"contract\",\"table\":\"agreements\",\"json\":\"true\",\"lower_bound\":\"" + id + "\", \"upper_bound\":\"" + id + "1" + "\"}"
        response = requests.request("POST", self.url, data=payload)
        responsejson = json.loads(response.text)
        try:
            return responsejson['rows'][0]
        except:
            return "failed"

    def acceptAgreement(self, account, id):
        self.unlock()
        os.system("cleos push action contract acceptagr '[\"" + account + "\", \"" + id + "\"]' -p " + account + "@active")

    def rejectAgreement(self, account, id):
        self.unlock()
        os.system("cleos push action contract rejectagr '[\"" + account + "\", \"" + id + "\"]' -p " + account + "@active")

    def putRecord(self, account, id, rating, comment):
        self.unlock()
        print("Calling command: ", "cleos push action contract putrecord '[\"" + account + "\", " + id + ", " + rating + ", \"" + comment + "\"]' -p " + account + "@active")
        os.system("cleos push action contract putrecord '[\"" + account + "\", " + id + ", " + rating + ", \"" + comment + "\"]' -p " + account + "@active")

    def getRecord(self, account, id):
        payload = "{\"scope\":\"contract\",\"code\":\"contract\",\"table\":\"records\",\"json\":\"true\",\"lower_bound\":\"" + id + "\", \"upper_bound\":\"" + id + "1" + "\"}"
        response = requests.request("POST", self.url, data=payload)
        responsejson = json.loads(response.text)
        try:
            return responsejson['rows'][0]
        except:
            return "failed"
