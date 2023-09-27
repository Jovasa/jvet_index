import json
from pprint import pprint

import requests

from download_zips import get_meeting_links


out = dict()

meeting_links = get_meeting_links()
for x in meeting_links:
    print(x[0])
    data = requests.get(x[1]).text
    data = data.split("</tr>")
    rows = [x.split("</td>") for x in data if "current_document" in x]
    for row in rows:
        try:
            tag = row[0].split(">")[3].split("<")[0].strip()
            name = row[6].split(">")[1].split("<")[0].strip()
            link = row[8].split("href=\"")[1].split("\"")[0].strip()
        except IndexError:
            print("Error parsing", row)
            continue
        out[tag] = {"name": name, "link": link.replace("..", "https://jvet-experts.org")}

# json.dump(out, open("out.json", "w"))
