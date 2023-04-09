import base64, json


def bytesToJSON(data):
    data = base64.b64decode(data)
    data = json.loads(data)
    
    return data

def JSONToBytes(data):
    data = json.dumps(data, indent=4) 
    data = data.encode('utf-8')
    
    return data