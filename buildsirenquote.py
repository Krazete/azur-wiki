import os
import json
import re
from argparse import ArgumentParser

langs = {
    'EN': 'English',
    'CN': 'Chinese',
    'JP': 'Japanese'
}

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

skin = {
    'tb': {
        1000: {
            'skin': '',
            'EN': 'Normal Personality',
            'CN': '',
            'JP': ''
        },
        1100: {
            'skin': 'Kind',
            'EN': 'Kind Personality',
            'CN': '温柔',
            'JP': '優しい'
        },
        1200: {
            'skin': 'Quiet',
            'EN': 'Quiet Personality',
            'CN': '安静',
            'JP': 'クール'
        },
        1300: {
            'skin': 'Peppy',
            'EN': 'Peppy Personality',
            'CN': '开朗',
            'JP': '元気'
        }
    },
    'navi': {
        2000: {
            'skin': '',
            'EN': 'Normal Personality',
            'CN': '',
            'JP': ''
        },
        2100: {
            'skin': 'Mild',
            'EN': 'Mild Personality',
            'CN': '乖巧',
            'JP': '大人しい'
        },
        2200: {
            'skin': 'Rebellious',
            'EN': 'Rebellious Personality',
            'CN': '叛逆',
            'JP': 'ワガママ'
        },
        2300: {
            'skin': 'Skin1',
            'EN': 'Imp of the Bathtub',
            'CN': '入浴的小恶魔',
            'JP': '小悪魔inバスタブ'
        }
    }
}

def init_data():
    for lang in langs:
        with open('{}/ShareCfg/secretary_special_ship.json'.format(lang), 'r', encoding='utf-8') as fp:
            data.setdefault(lang, json.load(fp))

def buildshipquote(siren, id, region):
    title = skin[siren][id][region]
    if title == '':
        title = skin[siren][id]['EN']
    elif region != 'EN':
        title += ' / ' + skin[siren][id]['EN']
    shipquote = [
        '==={}==='.format(title),
        '{{ShipQuote',
        '| Region = {}'.format(region),
        '| Skin = {}'.format(skin[siren][id]['skin'])
    ]
    for key in parametermap:
        if data[region][str(id)][key] == '':
            continue
        if key == 'chime_0':
            shipquote += [
                '}}',
                '===Hourly Notifications===',
                '{{ShipQuote',
                '| Region = {}'.format(region),
                '| Skin = '
            ]
        if key == 'main':
            mainsplit = data[region][str(id)][key].split('|')
            for i, part in enumerate(mainsplit, 1):
                shipquote += [
                    '',
                    '| {}{} = {}'.format(parametermap[key], i, part),
                    '| {}{}Note = '.format(parametermap[key], i)
                ]
        else:
            shipquote += [
                '',
                '| {} = {}'.format(parametermap[key], data[region][str(id)][key]),
                '| {}Note = '.format(parametermap[key])
            ]
    shipquote.append('}}')
    return shipquote

def doit():
    os.makedirs('output/quote', exist_ok=True)
    for siren in skin:
        page = [
            '{{ShipTabber}}',
            '<tabber>'
        ]
        for region in langs:
            if region != 'EN':
                page.append('|-|')
            page.append('{} Server='.format(langs[region]))
            for id in skin[siren]:
                page += buildshipquote(siren, id, region)
        page.append('</tabber>')
        with open('output/quote/{}.wiki'.format(siren), 'w', encoding='utf-8') as fp:
            fp.write('\n'.join(page))

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
