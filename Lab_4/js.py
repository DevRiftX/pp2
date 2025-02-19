import json

with open('Lab_4/sample-data.json', 'r') as fcc_file:
    fcc_data = json.load(fcc_file)

values = ['dn', 'descr', 'speed', 'mtu']

print("""Interface Status
================================================================================
DN                                                 Description           Speed    MTU  
-------------------------------------------------- --------------------  ------  ------""")


for data in fcc_data["imdata"]:
    temp = []
    for i in range(4):
        temp.append(((data["l1PhysIf"])["attributes"])[values[i]])
    print(f"{temp[0]:50} {temp[1]:20}  {temp[2]:6}  {temp[3]:6}")

def fetch(data):
    for i in data["imdata"]:
        file = (i["l1PhysIf"])["attributes"]
        yield f"{file['dn']:50} {file['descr']:20} {file['speed']:6}   {file['mtu']:6}"

print("""Interface Status
================================================================================
DN                                                 Description           Speed    MTU  
-------------------------------------------------- --------------------  ------  ------""")

for x in fetch(fcc_data):
    print(x)