import os
import json
import re
from argparse import ArgumentParser

decorset = {}

def init_decorset():
    '''Initializes `decor` and `decoritem` objects with JSON files downloaded from AzurLaneData repo.'''
    with open('EN/ShareCfg/backyard_theme_template.json', 'r', encoding='utf-8') as fp:
        decorset['theme'] = json.load(fp)
    with open('EN/ShareCfg/furniture_data_template.json', 'r', encoding='utf-8') as fp:
        decorset['item'] = json.load(fp)
    with open('EN/ShareCfg/furniture_shop_template.json', 'r', encoding='utf-8') as fp:
        decorset['shop'] = json.load(fp)

def get_themeid(name):
    '''Get theme id by set name or name fragment.'''
    for tid in decorset['theme']:
        if name in decorset['theme'][tid]['name']:
            return tid

itemrarity = [
    'Unobtainable',
    'Normal',
    'Rare',
    'Elite',
    'Super Rare',
    'Ultra Rare'
]

itemtype = {
    1: 'Wallpaper',
    2: 'Furniture',
    3: 'Decoration',
    4: 'Floor',
    5: 'Floor Item',
    6: 'Wall Decoration',
    14: 'Following'
}

strint = [
    'Zero shipgirls',
    'One shipgirl',
    'Two shipgirls',
    'Three shipgirls',
    'Four shipgirls',
    'Five shipgirls',
    'Six shipgirls',
    'Seven shipgirls',
    'Eight shipgirls',
    'Nine shipgirls',
    'Ten shipgirls'
]

def build_decorset(tid):
    theme = decorset['theme'][tid]
    lines = [
        '*\'\'\'Description:\'\'\' \'\'{}\'\''.format(theme['desc']),
        '{{{{FurnitureTable|ThemeIcon=FurnIcon_{}.png|Theme={}'.format(theme['icon'].replace(' ', '_'), theme['name'])
    ]

    iids = [str(iid) for iid in theme['ids']] + list(decorset['item'])
    visited = set()
    for iid in iids:
        if iid in visited:
            continue
        visited.add(iid)

        item = decorset['item'][iid]
        if str(item['themeId']) == tid and item['rarity'] > 0:
            details = [
                item['name'],
                item['icon'],
                item['describe'],
                itemrarity[item['rarity']],
                itemtype.get(item['type'], '<TYPE_{}>'.format(item['type'])),
                decorset['shop'].get(iid, {}).get('dorm_icon_price', ''),
                decorset['shop'].get(iid, {}).get('gem_price', ''),
                item['comfortable'],
                '{}x{}'.format(*item['size']) if item['size'] else '',
                item['count']
            ]

            notes = []
            if 'interAction' in item:
                action = item['interAction']
                notes.append('{} can {} here.'.format(strint[len(action)], action[0][0].replace('wash', 'bath')))
            matches = re.findall('\'event:(.+?)\'', str(item)) # plays audio
            if matches:
                notes.append('Plays audio when tapped:')
            for match in matches:
                event = match.replace('/', ' ').strip().replace(' ', '-')
                notes.append('{{{{Audio|file=FurnLine {}.ogg}}}} {}'.format(event, event)) # must edit; file name will be incorrect
            note = '<br>'.join(notes)
            details.append(note)
            
            line = '|' + '|'.join(str(detail) for detail in details)
            lines.append(line)
    lines.append('}}')

    os.makedirs('output', exist_ok=True)
    page = '\n'.join(lines) + '\n'
    with open('output/decorsetchart.txt', 'w', encoding='utf-8') as fp:
        fp.write(page)

# *'''Description:''' ''SET_DESCRIPTION''
# {{FurnitureTable|ThemeIcon=FurnIcon_SET_ICON.png|Theme=SET_NAME
# |NAME|ICON|DESCRIPTION|RARITY|TYPE|COINS|GEMS|HAPPINESS|SIZE|QUANTITY(|NOTES)?
# }}

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    parser.add_argument('-n', '--name', help='build decor set by name')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_decorset
        dl_decorset()
    if args.name:
        init_decorset()
        tid = get_themeid(args.name)
        build_decorset(tid)
