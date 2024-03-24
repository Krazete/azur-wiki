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

def get_item(name):
    '''Get item object by name or name fragment.'''
    for iid in decorset['item']:
        item = decorset['item'][iid]
        if name in item['name']:
            return item

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
    9: 'Arch',
    10: 'Special',
    11: 'Moving Object',
    13: 'Special',
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
    '''Build a wikitable from AzurLaneData files.'''
    theme = decorset['theme'][tid]
    lines = [
        '*\'\'\'Description:\'\'\' \'\'{}\'\''.format(theme['desc'].strip()),
        '{{{{FurnitureTable|ThemeIcon=FurnIcon_{}.png|Theme={}'.format(theme['icon'].replace(' ', '_'), theme['name'].strip())
    ]

    iids = [str(iid) for iid in theme['ids']] + list(decorset['item'])
    visited = set()
    for iid in iids:
        if iid in visited:
            continue
        visited.add(iid)
        item = decorset['item'][iid]
        if str(item['themeId']) == tid:
            line = build_decoritem(item)
            if item['rarity'] > 0:
                lines.append(line)
            else:
                print('UNOBTAINABLE:', line)
    lines.append('}}')

    os.makedirs('output', exist_ok=True)
    page = '\n'.join(lines) + '\n'
    with open('output/decorset.txt', 'w', encoding='utf-8') as fp:
        fp.write(page)

def get_action(action):
    replacements = {
        'attack': 'stand',
        'stand2': 'stand',
        'wash': 'bath',
        'yun': 'stand'
    }
    for aid in replacements:
        action = action.replace(aid, replacements[aid])
    return action

def build_decoritem(item):
    '''Build a wikitable item entry line.'''
    iid = str(item['id'])
    details = [
        item['name'].strip(),
        item['icon'],
        item['describe'].strip(),
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
        actions = {}
        for action in item['interAction']:
            actions.setdefault(action[0], 0)
            actions[action[0]] += 1
        for action in actions:
            notes.append('{} can {} here.'.format(strint[actions[action]], get_action(action)))
    matches = re.findall('\'event:(.+?)\'', str(item)) # plays audio
    if matches:
        notes.append('Plays audio when tapped:')
    for match in matches:
        event = match.replace('/', ' ').strip().replace(' ', '-')
        notes.append('{{{{Audio|file=FurnLine {}.ogg}}}} {}'.format(event, event)) # must edit; file name will be incorrect
    note = '<br>'.join(notes)
    if notes:
        details.append(note)

    return '|' + '|'.join(str(detail) for detail in details)

# *'''Description:''' ''SET_DESCRIPTION''
# {{FurnitureTable|ThemeIcon=FurnIcon_SET_ICON.png|Theme=SET_NAME
# |NAME|ICON|DESCRIPTION|RARITY|TYPE|COINS|GEMS|HAPPINESS|SIZE|QUANTITY(|NOTES)?
# }}

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    parser.add_argument('-s', '--setname', help='build decor set table by name')
    parser.add_argument('-i', '--itemname', help='build decor item entry by name')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_decorset
        dl_decorset()
    if args.setname:
        init_decorset()
        tid = get_themeid(args.setname)
        build_decorset(tid)
    if args.itemname:
        if len(decorset) <= 0:
            init_decorset()
        item = get_item(args.itemname)
        line = build_decoritem(item)
        with open('output/decoritem.txt', 'w', encoding='utf-8') as fp:
            fp.write(line)
