import urllib.request
import json
req = urllib.request.Request('https://app.starscholars.org/api/v1/groups/list/?group_type=circle&circle_status=1,4')
response = urllib.request.urlopen(req)
js = json.loads(response.read().decode('utf-8'))
for r in (js.get('results') or js.get('data') or [])[:3]:
    print("NAME", r.get('name'))
    print("START", repr(r.get('start_date')))
    print("END", repr(r.get('end_date')))
    print("---")
