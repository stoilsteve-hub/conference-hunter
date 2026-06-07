import urllib.request
import json
import time

urls = [
    "https://mrnabased-therapeutics.com/speaker/yun-gong/",
    "https://in-vivo-engineering.com/speaker/cecile-bauche/",
    "https://in-vivo-engineering.com/speaker/george-diaz/",
    "https://in-vivo-engineering.com/speaker/zach-zhu/",
    "https://in-vivo-engineering.com/speaker/arpita-maiti/"
]

print("Here are the Wayback Machine archives for the missing speakers:\n")
for u in urls:
    try:
        wayback_api = f"https://archive.org/wayback/available?url={u}"
        req = urllib.request.Request(wayback_api, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            if 'archived_snapshots' in data and 'closest' in data['archived_snapshots']:
                archive_url = data['archived_snapshots']['closest']['url']
                print(f"Original URL: {u}")
                print(f"Archived URL: {archive_url}\n")
            else:
                print(f"Original URL: {u}")
                print(f"No archive found.\n")
    except Exception as e:
        print(f"Error fetching {u}: {e}")
    time.sleep(1)

