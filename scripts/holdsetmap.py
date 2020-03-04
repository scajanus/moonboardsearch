from pprint import pprint as pp
from  pathlib import Path
import json

x = 'scrape/readhar/'
holdsets2016 = Path('%s/2016/holdsets.json'%x)
holdsets2017 = Path('%s/2017/holdsets.json'%x)
holdsets2019 = Path('%s/2019/holdsets.json'%x)

holdsetmapping  = {}

namemapping = {
'Hold Set A': 'A',
'Hold Set B': 'B',
'Hold Set C': 'C',
'Wooden Holds': 'wood',
'Original School Holds': 'school',
'Wooden Holds B': 'woodB',
'Wooden Holds C': 'woodC'
}

holdsets = {'2016':holdsets2016,'2017':holdsets2017,'2019':holdsets2019}

for year, holdset in holdsets.items():
    with holdset.open("r+") as f:
        holdsetinfos = json.load(f)
        for holdsetinfo in holdsetinfos:
            #pp(holdsetinfo['Description'])
            for h in holdsetinfo['Holds']:
                #pp("print h['Id'], h['Number'], h['HoldType'], h['Location'], h['HoldSetDescription']")
                pp(h['Location']['Description'])
                if year not in holdsetmapping:
                    holdsetmapping[year] = {}
                if h['Location']['Description'] not in holdsetmapping[year].keys():
                    holdsetmapping[year][h['Location']['Description']] = []


                holdsetmapping[year][h['Location']['Description']].append(namemapping[holdsetinfo['Description']])

pp(holdsetmapping)
