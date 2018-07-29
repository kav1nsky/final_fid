from fidelity import Fidelity

one = int(input())

failed = []

f = Fidelity()

priv, pub, acc = f.createAccount(one)

f.setWorker(acc, "Worker Fidelity")
resp = f.getWorker(acc)
if (resp["account"] != "user1"):
    failed.append("setWorker failed")

priv2, pub2, acc2 = f.createAccount(one + 1)

'''f.setCustomer(acc2, "Customer Fidelity", "First Fidelity customer")
resp = f.getCustomer(acc2)
if (resp["account"] != "user2"):
    failed.append("setCustomer failed")

f.initAgreement(acc2, acc, "Agreement content", 1000)
resp = f.getCustomer(acc2)
id = int(resp["agreementIds"][0])
resp = f.getAgreement(id)
if (resp["customerName"] != "user2"):
    failed.append("initAgreement failed")

f.acceptAgreement(acc, id)
resp = f.getAgreement(id)
if (resp["state"] != 1):
    failed.append("acceptAgreement failed")

f.putRecord(acc2, id, 7, "Good")
resp = f.getWorker(acc)
if len(resp["recordIds"]) == 0:
    recordId = 0
else:
    recordId = resp["recordIds"][0]
resp = f.getRecord(recordId)
if (resp["comment"] != "Good"):
    failed.append("putRecord failed")'''

if len(failed) == 0:
    print("All checks passed")
else:
    print (str(len(failed)) + " checks failed:")
    for fail in failed:
        print(failed)
