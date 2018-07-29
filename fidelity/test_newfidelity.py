from newfidelity import Fidelity

f = Fidelity()

# Create worker

username = input()
priv, pub = f.createAccount(username)

f.setWorker(username, "Egor Polyakov")
resp = f.getWorker(username)
print('-------------------------------------------------------------------------')
print(pub)
print(resp)
print('-------------------------------------------------------------------------')

f.addInfo(username, "Some education info")

f.setWorker(username, "Aleksey Ponomarev")
resp = f.getWorker(username)
print('-------------------------------------------------------------------------')
print(resp)
print('-------------------------------------------------------------------------')

# Create customer

username2 = input()
priv2, pub2 = f.createAccount(username2)

f.setCustomer(username2, "Vladimir Putin", "Our beloved president")
resp = f.getCustomer(username2)
print('-------------------------------------------------------------------------')
print(pub2)
print(resp)
print('-------------------------------------------------------------------------')

# Create agreement

f.initAgreement(username2, username, "Some agreement", "100")
resp = f.getWorker(username);
print('-------------------------------------------------------------------------')
print(resp)
id = 0
try:
    id = resp['agreementIds'][0]
except:
    id = 0
print(id)
print('-------------------------------------------------------------------------')

resp = f.getAgreement(username, str(id))
print('-------------------------------------------------------------------------')
print(resp)
print('-------------------------------------------------------------------------')

# Accept agreement

f.acceptAgreement(username, str(id))
resp = f.getAgreement(username, str(id))
print('-------------------------------------------------------------------------')
print(resp)
print('-------------------------------------------------------------------------')

# Put record

f.putRecord(username2, str(id), "7", "Good job")
resp = f.getWorker(username);
print('-------------------------------------------------------------------------')
print(resp)
id2 = 0
try:
    id2 = resp['recordIds'][0]
except:
    id2 = 0
print(id2)
print('-------------------------------------------------------------------------')

resp = f.getRecord(username, str(id2))
print('-------------------------------------------------------------------------')
print(resp)
print('-------------------------------------------------------------------------')

resp = f.getAgreement(username, str(id))
print('-------------------------------------------------------------------------')
print(resp)
print('-------------------------------------------------------------------------')
