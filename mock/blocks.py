import json

def mock():
    mockchain_file = open("mockchain.json", "r")
    return json.load(mockchain_file)
