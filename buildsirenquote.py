import os
import json
import re
from argparse import ArgumentParser

langs = ['EN', 'CN', 'JP']

data = {}

parametermap = {
    'login': 'Login',
    'main': 'SecretaryIdle',
    'touch': 'SecretaryTouch',
    'mission': 'Task',
    'mission_complete': 'TaskComplete',
    'mail': 'Mail',
    'home': 'MissionFinished',
    'expedition': 'Commission',
    'chuxi': 'CNYE',
    'xinnian': 'CNY',
    'qingrenjie': 'Valentine',
    'zhongqiu': 'MidAutumn',
    'wansheng': 'Halloween',
    'shengdan': 'Christmas',
    'huodong': 'Event',
    'genghuan': 'ChangeModule',
    'chime_0': 'Chime0',
    'chime_1': 'Chime1',
    'chime_2': 'Chime2',
    'chime_3': 'Chime3',
    'chime_4': 'Chime4',
    'chime_5': 'Chime5',
    'chime_6': 'Chime6',
    'chime_7': 'Chime7',
    'chime_8': 'Chime8',
    'chime_9': 'Chime9',
    'chime_10': 'Chime10',
    'chime_11': 'Chime11',
    'chime_12': 'Chime12',
    'chime_13': 'Chime13',
    'chime_14': 'Chime14',
    'chime_15': 'Chime15',
    'chime_16': 'Chime16',
    'chime_17': 'Chime17',
    'chime_18': 'Chime18',
    'chime_19': 'Chime19',
    'chime_20': 'Chime20',
    'chime_21': 'Chime21',
    'chime_22': 'Chime22',
    'chime_23': 'Chime23'
}

skinids = {
    1000: '',
    1100: 'Kind',
    1200: 'Quiet',
    1300: 'Peppy',
    
    2000: '',
    2100: 'Mild',
    2200: 'Rebellious',
    2300: 'Imp of the Bathtub',
}

titles = {
    1000: 'Normal',
    1100: 'Kind',
    1200: 'Quiet',
    1300: 'Peppy',

    2000: 'Normal',
    2100: 'Mild',
    2200: 'Rebellious',
    2300: 'Imp of the Bathtub',
}

def init_data():
    for lang in langs:
        with open('{}/ShareCfg/secretary_special_ship.json'.format(lang), 'r', encoding='utf-8') as fp:
            data.setdefault(lang, json.load(fp))


def buildshipquote(id, region):
    shipquote = '==={2} Personality===\n{{{{ShipQuote\n| Region = {0}\n| Skin = {1}\n'.format(region, skinids[id], titles[id])
    for key in parametermap:
        if data[region][str(id)][key] == '':
            continue
        if key == 'chime_0':
            shipquote += '}}}}\n===Hourly Notifications===\n{{{{ShipQuote\n| Region = {0}\n| Skin = \n'.format(region)
        if key == 'main':
            mainsplit = data[region][str(id)][key].split('|')
            for i, part in enumerate(mainsplit, 1):
                shipquote += '\n| {0}{2} = {1}\n| {0}{2}Note = \n'.format(parametermap[key], part, i)
        else:
            shipquote += '\n| {0} = {1}\n| {0}Note = \n'.format(parametermap[key], data[region][str(id)][key])
    shipquote += '}}\n'
    return shipquote

def doit():
    for region in langs:
        page = ''
        for id in skinids:
            page += buildshipquote(id, region)
        with open('output/{}page.txt'.format(region), 'w', encoding='utf-8') as fp:
            fp.write(page)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_from, dl_sharecfg
        dl_sharecfg('sirenquote', ['EN', 'CN', 'JP'], [
            'secretary_special_ship'
        ])
    init_data()
    doit()
