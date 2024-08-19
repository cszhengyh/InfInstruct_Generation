DATA_DIR = ""
MEGTRON_DATA_PATH = ""

import os
import json
import jsonlines
from collections import defaultdict

with jsonlines.open(MEGTRON_DATA_PATH, 'w') as megtron_data:
    id = 0
    for f in os.listdir(DATA_DIR):
        with open(os.path.join(DATA_DIR, f), 'r', encoding='utf-8') as json_file:
            json_data = json.load(json_file)
            data = defaultdict(lambda: -1)
            data["id"] = id
            conversations = []
            conversations.append({"from": "human", "value": json_data['problem']})
            conversations.append({"from": "gpt", "value": json_data['solution']})
            data["conversations"] = conversations
            megtron_data.write(data)
            id += 1
        # break
