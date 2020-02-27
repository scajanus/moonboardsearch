import zlib
import json
import base64
import sys

har = json.loads(open("www.moonboard.com.2016.har").read())

allproblems = dict()
allsetters = dict()
allholdsets = []
allgrades = []
for n,h in enumerate(har['log']['entries']):
    if 'POST' in  h['request']['method']:
        content = h['response']['content']
        t = content['text']
        if content.get('encoding') == 'base64':
            json_text = base64.b64decode(t)
        else:
            json_text = t
        if 'GetProblems' in h['request']['url']:
            for p in json.loads(json_text)['Data']:
                allproblems[p['Id']] = p
        if 'GetSetters' in h['request']['url']:
            for s in json.loads(json_text)['Data']:
                allsetters[s['Id']] = s


    if 'GET' in h['request']['method'] and h['response']['content']['mimeType'] == 'application/json':
        content = h['response']['content']
        if 'GetGrades' in h['request']['url']:
            allgrades.extend(json.loads(content['text']))
        if 'GetHoldsets' in h['request']['url']:
            allholdsets.extend(json.loads(content['text']))

with open('problems.json','w') as outfile:
    json.dump(allproblems, outfile)

with open('grades.json','w') as outfile:
    json.dump(allgrades, outfile)

with open('setters.json','w') as outfile:
    json.dump(allsetters, outfile)

with open('holdsets.json','w') as outfile:
    json.dump(allholdsets, outfile)
