import subprocess
def create_new_account(username):
    key = subprocess.check_output("cleos create key", shell=True)
    account = subprocess.check_output("cleos create account eosio ", shell=True)
    print(key)
