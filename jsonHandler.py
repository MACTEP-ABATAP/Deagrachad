import json
def jsonHand(File_name):
    with open(File_name) as File_data:
        jsondata = json.load(File_data)
    return jsondata

