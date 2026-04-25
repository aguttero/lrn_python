import json

def fetch_groups ():
    all_groups_list = []
    with open ("data/20260424_groups.json", "r") as file:
        all_groups_list = json.load(file)
    return all_groups_list

## TEST RUN

print (fetch_groups())
