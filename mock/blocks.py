import json

def mock():
    mockchain_file = open("mock/mockchain.json", "r")
    return json.load(mockchain_file)
