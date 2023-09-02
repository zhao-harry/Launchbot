import copy
import json
import re
import requests
import urllib.request
from datetime import datetime

# Import webhook URL (sensitive)
import credentials

# Open generic rich message blocks from JSON
with open("blocks.json", "r") as f:
    payload = json.load(f)

with open("mrkdwn.json", "r") as f:
    mrkdwn = json.load(f)

# This function reads a generic mrkdwn block for JSON and returns it with added text
def make_launch_block(name, provider, vehicle, pad, location, country, link, time):
    launch_block = copy.deepcopy(mrkdwn)
    text = f"*{name} | {provider} | {vehicle}* \n {pad}, {location}, {country} \n <{link}|{time}>"
    launch_block['text']['text'] = text
    return launch_block

# GET upcoming launches from RocketLaunch.Live API
rocketlaunch_url = "https://fdo.rocketlaunch.live/json/launches/next/5"
with urllib.request.urlopen(rocketlaunch_url) as url:
    data = json.load(url)

launches = data['result']
for launch in launches:
    name = launch['name']
    provider = launch['provider']['name']
    vehicle = launch['vehicle']['name']
    pad = launch['pad']['name']
    location = launch['pad']['location']['name']
    country = launch['pad']['location']['country']
    link = re.search("(?P<url>https?://[^\s'\"]+)", launch['quicktext']).group("url")
    sort_date = int(launch['sort_date'])
    t0 = launch['t0']
    time = datetime.utcfromtimestamp(sort_date).strftime('%Y-%m-%d %H:%M:%S UTC' if t0 else '%Y-%m-%d')
    payload['blocks'].append(make_launch_block(name, provider, vehicle, pad, location, country, link, time))

# POST formatted rich message JSON to Slack webhook
requests.post(credentials.webhook, json=payload)
