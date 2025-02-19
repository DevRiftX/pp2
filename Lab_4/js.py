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
    for element in data["imdata"]:
        temp = (element["l1PhysIf"])["attributes"]
        yield f"{temp['dn']:50} {temp['descr']:20} {temp['speed']:6}   {temp['mtu']:6}"

print("\n" * 8 + """Interface Status
================================================================================
DN                                                 Description           Speed    MTU  
-------------------------------------------------- --------------------  ------  ------""")

for x in fetch(fcc_data):
    print(x)