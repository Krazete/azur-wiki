import json
import re
from argparse import ArgumentParser

langs = ['CN', 'EN', 'JP']
uis = {}
shops = {}

months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

def init():
    for lang in langs:
        uis.setdefault(lang, {})
        with open('{}/ShareCfg/item_data_battleui.json'.format(lang), 'rb') as fp:
            uis[lang] = json.load(fp)
        shops.setdefault(lang, {})
        with open('{}/ShareCfg/pay_data_display.json'.format(lang), 'rb') as fp:
            shops[lang] = json.load(fp)

def getdates(uiid, lang):
    shop = shops[lang]
    for id in shop:
        if id == 'all':
            continue
        if 'display' in shop[id] and shop[id]['display']:
            if shop[id]['display'][0][1] == uiid:
                return '{} {}, {} - {} {}, {}'.format(
                    months[shop[id]['time'][0][0][1]],
                    shop[id]['time'][0][0][2],
                    shop[id]['time'][0][0][0],
                    months[shop[id]['time'][1][0][1]],
                    shop[id]['time'][1][0][2],
                    shop[id]['time'][1][0][0]
                )

def buildui():
    uikeys = {lang: set(uis[lang].keys()) for lang in uis}
    universalkeys = uikeys['EN'].intersection(uikeys['CN'], uikeys['JP'])

    lines = ['{{Image Gallery | width = 384']

    def addcell(id, lang):
        ui = uis[lang]
        if 'Buy' in ui[id]['unlock']:
            time = getdates(ui[id]['id'], lang)
            unlock = '[[Akashi\'s Shop]] ({})'.format(time)
        elif 'Cruise Mission' in ui[id]['unlock']:
            unlock = '[[Cruise Missions|{}]]'.format(ui[id]['unlock'])
        elif 'Black Friday Cruise Pass' in ui[id]['unlock']:
            unlock = re.sub(
                'Black Friday Cruise Pass',
                '[[Black Friday Akashi\'s Fire Sale#Black Friday Cruise Missions|{}]]'.format('Black Friday Cruise Pass'),
                ui[id]['unlock']
            )
        else:
            unlock = ui[id]['unlock']
        
        lines.append('| BattleUI {}.png | {}\'\'\'{}\'\'\'<br>\'\'{}\'\'<br>Unlock: {}'.format(
            ui[id]['icon'],
            '' if ui[id]['unlock'] == 'Default' else re.sub('^ui_(\d+)$', '[[File:BattleUIIcon \g<1>.png|50px]]', ui[id]['display_icon']),
            re.sub('Battle UI\W+', '', ui[id]['name']),
            ui[id]['desc'],
            unlock
        ))

    for id in sorted(universalkeys):
        if id == 'all':
            continue
        addcell(id, 'EN')
    lines.append('}}')

    regionalkeys = {
        'EN Only': uikeys['EN'].difference(uikeys['CN'].union(uikeys['JP'])),
        'EN/CN Only': uikeys['EN'].intersection(uikeys['CN']).difference(uikeys['JP']),
        'EN/JP Only': uikeys['EN'].intersection(uikeys['JP']).difference(uikeys['CN']),
        'CN Only': uikeys['CN'].difference(uikeys['EN'].union(uikeys['JP'])),
        'CN/JP Only': uikeys['CN'].intersection(uikeys['JP']).difference(uikeys['EN']),
        'JP Only': uikeys['JP'].difference(uikeys['EN'].union(uikeys['CN'])),
    }

    for region in regionalkeys:
        if len(regionalkeys[region]):
            lines.append('== {} =='.format(region))
            lines.append(lines[0])
            for id in regionalkeys[region]:
                ui = uis[region[:2]]
                if id == 'all':
                    continue
                addcell(id, region[:2])
            lines.append('}}')

    with open('output/ui.wiki', 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(lines))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import update
        update(langs, [
            'ShareCfg/item_data_battleui',
            'ShareCfg/pay_data_display'
        ])
    init()
    buildui()
