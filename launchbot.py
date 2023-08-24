import copy
import json
import requests
import urllib.request

# Import webhook URL (sensitive)
import credentials

# Open generic rich message blocks from JSON
with open("blocks.json", "r") as f:
    payload = json.load(f)

with open("plain_text.json", "r") as f:
    plain_text = json.load(f)

# This function reads a generic plain text block for JSON and returns it with added text
def make_plain_text_block(text):
    plain_text_block = copy.deepcopy(plain_text)
    plain_text_block['text']['text'] = text
    return plain_text_block

# GET upcoming launches from RocketLaunch.Live API
rocketlaunch_url = "https://fdo.rocketlaunch.live/json/launches/next/5"
with urllib.request.urlopen(rocketlaunch_url) as url:
    data = json.load(url)

launches = data['result']
for launch in launches:
    quicktext = launch['quicktext']
    payload['blocks'].append(make_plain_text_block(quicktext))

# POST formatted rich message JSON to Slack webhook
requests.post(credentials.webhook, json=payload)
