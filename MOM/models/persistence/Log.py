from config import BASE_DIR
import json


def updateLog():
    # Path to log.json file
    filename = f'{BASE_DIR}/models/persistence/files/log.json'

    with open(filename, "r+") as f:
        data = json.load(f)
        data["count"] += 1
        f.seek(0)
        json.dump(data, f, indent=4)