from config import BASE_DIR
import json, os


def updateLog():
    # Path to log.json file
    filename = f'{BASE_DIR}/models/persistence/files/log.json'
    
    # If file doesn't exist, create it and add 1 to count
    if not os.path.exists(filename):
        data = {"count" : 1}
        with open(filename, "w") as f:
            json.dump(data, f)
            
        return
    
    # If file exists, read the count and add 1 to it
    with open(filename, "r+") as f:
        data = json.load(f)
        data["count"] += 1
        f.seek(0)
        json.dump(data, f, indent=4)