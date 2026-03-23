import json

# Python -> JSON
data = {"name": "Dimash", "age": 18}
json_str = json.dumps(data)
print(json_str)

# JSON -> Python
parsed = json.loads(json_str)
print(parsed["name"])

# write to file
with open("data.json", "w") as f:
    json.dump(data, f)

# read from file
with open("data.json", "r") as f:
    loaded = json.load(f)
    print(loaded)