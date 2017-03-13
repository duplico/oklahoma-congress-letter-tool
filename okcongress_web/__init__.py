from flask import Flask
import json

app = Flask(__name__)
app.secret_key = 'NpaAAAAAA<;f;i(:T>3tn~dsOue5Vy)'

with open('okcongress/house.json') as house:
    house_data = json.load(house)
    
with open('okcongress/senate.json') as senate:
    senate_data = json.load(senate)

house_committees = dict()
senate_committees = dict()
all_committees = dict()

for member in house_data:
    for committee in member['committees']:
        cmte_name = 'House %s' % committee
        all_committees.setdefault(cmte_name, [])
        all_committees[cmte_name].append(member)
        house_committees.setdefault(committee, [])
        house_committees[committee].append(member)

for member in senate_data:
    for committee in member['committees']:
        cmte_name = 'Senate %s' % committee
        all_committees.setdefault(cmte_name, [])
        all_committees[cmte_name].append(member)
        senate_committees.setdefault(committee, [])
        senate_committees[committee].append(member)


committee_names = all_committees.keys()
house_committee_names = house_committees.keys()
senate_committee_names = senate_committees.keys()
committee_names.sort()
house_committee_names.sort()
senate_committee_names.sort()

import okcongress_web.views
