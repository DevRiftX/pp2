import json

with open('Lab_4/sample-data.json', 'r') as fcc_file:
    fcc_data = json.load(fcc_file)

values = ['dn', 'descr', 'speed', 'mtu']

print("""Interface Status
================================================================================
DN                                                 Description           Speed    MTU  
-------------------------------------------------- --------------------  ------  ------""")

temp = []
for data in fcc_data["imdata"]:
    for i in range(4):
        temp.append(((data["l1PhysIf"])["attributes"])[values[i]])
    print(f"{temp[0]}            {temp[1]}                  {temp[2]}   {temp[3]}")