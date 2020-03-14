import zlib
import json
import base64
import sys
<<<<<<< HEAD
from pprint import pprint as pp

years = ['2016','2017','2019']
hars = {}
for y in years:
    hars[y] = "www.moonboard.com.%s.har"%y
pp(hars)

def getdata(year, har):
    holdsetids = {'2016':'1', '2017':'15',  '2019':'17'}
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
                requrl = h['request']['url']
                if "/%s?"%holdsetids[year] in requrl:
                    pp((holdsetids[year],' in ',requrl))
                    allholdsets.extend(json.loads(content['text']))

    with open('%s/problems.json'%year,'w') as outfile:
        json.dump(allproblems, outfile)

    with open('%s/grades.json'%year,'w') as outfile:
        json.dump(allgrades, outfile)

    with open('%s/setters.json'%year,'w') as outfile:
        json.dump(allsetters, outfile)

    with open('%s/holdsets.json'%year,'w') as outfile:
        json.dump(allholdsets, outfile)

for year in years:
    har = hars[year]
    pp(har)
    hardata = json.loads(open(har).read())
    getdata(year, hardata)
