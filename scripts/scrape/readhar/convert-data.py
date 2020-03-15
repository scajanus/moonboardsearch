import zlib
import json
import base64
import sys
from pprint import pprint as pp
from collections import Counter

#har2016 = json.loads(open("www.moonboard.com.2016.har").read())
har2017 = json.loads(open("www.moonboard.com.2017.har").read())
#har2019 = json.loads(open("www.moonboard.com.2019.har").read())

allproblems = []
allsetters = []
allholdsets = []
allgrades = []

#for har in [har2017]:
for har in [har2017]:

    for n,h in enumerate(har['log']['entries']):
        if 'POST' in  h['request']['method']:
            content = h['response']['content']
            t = content['text']
            if content.get('encoding') == 'base64':
                json_text = base64.b64decode(t)
            else:
                json_text = t
            if 'GetProblems' in h['request']['url']:
                allproblems.extend(json.loads(json_text)['Data'])
            if 'GetSetters' in h['request']['url']:
                allsetters.extend(json.loads(json_text)['Data'])


        if 'GET' in h['request']['method'] and h['response']['content']['mimeType'] == 'application/json':
            content = h['response']['content']
            requrl = h['request']['url']

            if 'GetGrades' in h['request']['url']:
                allgrades.extend(json.loads(content['text']))
            if 'GetHoldsets' in h['request']['url']:
                pp(requrl)
                data = json.loads(content['text'])
                for l in data:
                    pp(l['Description'])
                    for h in l['Holds']:
                        pp(h['Location']['Description'])
                allholdsets.extend(json.loads(content['text']))

sys.exit()
flatlist =  []
for p in allproblems:
    flat = dict()
    flat['Method'] = p['Method']
    flat['Name'] = p['Name']
    flat['Grade'] = p['Grade']
    flat['FirstName'] = p['Setter']['Firstname']
    flat['LastName'] = p['Setter']['Lastname']
    flat['IsBenchmark'] = p['IsBenchmark']
    flat['IsMaster'] = p['IsMaster']
    flat['IsAssessmentProblem'] = p['IsAssessmentProblem']
    flat['MoonBoardHoldSetup'] = p['Holdsetup']['Description']
    if p.get('MoonBoardConfiguration'):
        flat['MoonboardConfiguration'] = p['MoonBoardConfiguration'].get('Description','')
    flat['RepeatText'] =  p['RepeatText']
    flat['DateInserted'] = p['DateInserted']
    flat['DateTimeString'] = p['DateTimeString']
    flat['NameForUrl'] = p['NameForUrl']
    flat['Moves'] = []
    for m in p['Moves']:
        temp = {'Position': m['Description'], 'IsStart': m['IsStart'],'IsEnd': m['IsEnd']}
        flat['Moves'].append(temp)
    flatlist.append(flat)

with open('flat.json','w') as outfile:
    json.dump(flatlist, outfile)
