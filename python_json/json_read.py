import json 
with open("sample-data.json", "r") as f:
    data = json.load(f)

l = data.get("imdata", data)



print("Interface status:")
print("=" * 100)
print("DN" + " " * 45 + "Description" + " " * 15 + "Speed" + " " * 10 + "MTU" + " " * 10) 
print("-" * 100)
for i in l:
    json_data = i.get("l1PhysIf", {}).get("attributes", i.get("attributes", {}))
    dn = json_data.get("dn", "-")
    descr = json_data.get("descr", " ")
    speed = json_data.get("speed", "inherit")
    mtu = json_data.get("mtu", "9150")
    print(dn + " " * 10 + descr + " " * 20 + speed + " " * 10 + mtu + " " * 10) 

print("=" * 100)