import os
import json
import re
from argparse import ArgumentParser

decorset = {}
ignorelist = []

def init_decorset(lang):
    '''Initializes `decor` and `decoritem` objects with JSON files downloaded from AzurLaneData repo.'''
    with open('{}/ShareCfg/backyard_theme_template.json'.format(lang), 'r', encoding='utf-8') as fp:
        decorset['theme'] = json.load(fp)
    with open('{}/ShareCfg/furniture_data_template.json'.format(lang), 'r', encoding='utf-8') as fp:
        decorset['item'] = json.load(fp)
    with open('{}/ShareCfg/furniture_shop_template.json'.format(lang), 'r', encoding='utf-8') as fp:
        decorset['shop'] = json.load(fp)
    with open('{}/ShareCfg/shop_furniture_relation.json'.format(lang), 'r', encoding='utf-8') as fp:
        decorset['rel'] = json.load(fp)

def get_themeid(name):
    '''Get theme id by set name or name fragment.'''
    for tid in decorset['theme']:
        if name in decorset['theme'][tid]['name']:
            return tid

def get_items(name):
    '''Get item objects by name or name fragment.'''
    for iid in decorset['item']:
        item = decorset['item'][iid]
        if name in item['name']:
            yield item

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
    3: 'Decoration', # in Misc
    4: 'Floor',
    5: 'Floor Item', # like rugs, roads, carpets; can place decor on top
    6: 'Wall Decoration',
    7: 'Special', # Models, Medals, Monthly Rewards
    8: 'Special', # Tatami Stage only; elevated floor (walkable)
    9: 'Arch',
    10: 'Wallpaper Item', # can place wall decor on top; can overlap
    11: 'Moving Object', # Mount
    12: 'Special', # Teleporter Gate only
    13: 'Special', # Interactive, in Collection
    14: 'Following',
    15: 'Special' # Antique Pipa only; can play music (both audio and an instrument sim)
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

def build_decorset(tid, endbar):
    '''Build a wikitable from AzurLaneData files.'''
    theme = decorset['theme'].get(tid, {
        'name': 'NO THEME',
        'desc': 'NO THEME',
        'icon': 'NO THEME',
        'ids': []
    })
    lines = [
        '{{{{FurnitureTable|ThemeIcon=FurnIcon_{}.png|Theme={}|ThemeDesc={}'.format(
            theme['icon'].replace(' ', '_'),
            theme['name'].strip(),
            theme['desc'].strip()
        )
    ]

    themeids = [str(iid) for iid in theme['ids']]
    iids = themeids + list(decorset['item'])
    visited = set()
    for iid in iids:
        if iid in visited:
            continue
        visited.add(iid)
        item = decorset['item'][iid]
        if str(item['themeId']) == tid:
            if iid not in themeids:
                print('SPECIAL:', item['name'])
            line = build_decoritem(item, endbar)
            if item['rarity'] > 0:
                lines.append(line)
            else:
                lines.append('|UNOBTAINABLE?' + line)
                print('UNOBTAINABLE?:', line)
    lines.append('}}')

    os.makedirs('output', exist_ok=True)
    page = '\n'.join(lines) + '\n'
    with open('output/decorset.wiki', 'w', encoding='utf-8') as fp:
        fp.write(page)

def get_action(action):
    replacements = {
        'attack': 'stand', # Miniature Public Park only
        'tuozhuai': 'float', # drag, hang
        'wash': 'bath',
        'yun': 'stand' # dizzy
    }
    action = re.sub('\d+', '', action)
    for aid in replacements:
        action = action.replace(aid, replacements[aid])
    return action

def walk(x):
    if isinstance(x, list):
        for y in x:
            for z in walk(y):
                yield z
    elif isinstance(x, dict):
        for key in x:
            for y in walk(x[key]):
                yield walk(y)
    else:
        yield x

def build_decoritem(item, endbar):
    '''Build a wikitable item entry line.'''
    iid = str(item['id'])
    details = [
        item['name'].strip(),
        item['icon'],
        re.sub('\s+', ' ', re.sub('<.+?>', ' ', item['describe'])).strip(),
        itemrarity[item['rarity']],
        itemtype.get(item['type'], '<TYPE_{}>'.format(item['type'])),
        decorset['shop'].get(iid, {}).get('dorm_icon_price', ''),
        decorset['shop'].get(iid, {}).get('gem_price', ''),
        item['comfortable'],
        '{}x{}'.format(*item['size']) if item['size'] else '',
        item['count']
    ]

    notes = []

    for rid in decorset['rel']:
        rel = decorset['rel'][rid]
        if rel['fur_id'] == item['id']:
            matches = re.match('(.+)——(.+)', rel['desc'])
            if matches:
                notes.append('[[{0}]] - [[{0}/Gallery#{1}-0|{1}]] Motif'.format(matches[1].strip(), matches[2].strip()))

    if item['gain_by']:
        notes.append('Obtained in [[{}]].'.format(item['gain_by'].strip()))

    if 'interAction' in item:
        actions = {}
        for action in item['interAction']:
            if isinstance(action, list):
                act = action[0]
            elif isinstance(action, dict): # Colorful Armor only
                act = action[list(action)[0]]
            actions.setdefault(act, 0)
            actions[act] += 1
        for action in actions:
            notes.append('{} can {} here.'.format(strint[actions[action]], get_action(action)))

    actions = set()
    if 'spine' in item:
        for actionN in walk(item['spine']):
            if isinstance(actionN, str):
                action = get_action(actionN)
                if action in ['attack', 'dance', 'sit', 'sleep', 'tuozhuai', 'stand', 'walk', 'yun']:
                    actions.add(action)
    if len(actions) == 1:
        notes.append('{} can {} here.'.format(strint[1 + len(item['spine_extra'])], actions.pop())) # todo: detect different types of stand (edit get_action method)
    elif len(actions) > 1:
        notes.append('Special interaction.') # must edit; clarify what the action is (bungee, magic trick, etc) and if it's on tap or on shipgirl interaction
        print('MUST EDIT ACTION:', item['name'], actions)

    trigger = item['can_trigger'] # has message window if trigger[0] > 0
    if trigger[0] > 0:
        notes.append('TROPHY') # must edit out; just for detecting items with popup windows
    if len(trigger) > 1: # plays audio from window
        notes.append('Includes audio:')
        for action in trigger[1:]: # must edit; delete non-audio actions
            if isinstance(action, str):
                notes.append(action)
            elif isinstance(action, list):
                notes.append('|'.join(action))
        print('MUST EDIT AUDIO:', item['name'])

    if 'interaction_bgm' in item: # Super Stage, AzuNavi! Radio Booth, and Holostage only
        notes.append('Plays audio on shipgirl interaction:')
        notes.append(item['interaction_bgm'][1])

    matches = re.findall('\'event:(.+?)\'', str(item.get('spine'))) # plays audio on tap
    if matches:
        notes.append('Plays audio when tapped:')
    for match in matches:
        event = match.replace('/', ' ').strip().replace(' ', '-')
        notes.append('{{{{Audio|file=FurnLine {0}.ogg}}}} [[Media:FurnLine {0}.ogg|{0}]]'.format(event)) # must edit; file name will be incorrect
        print('MUST EDIT AUDIO:', item['name'])

    note = '<br>'.join(notes)
    if note or endbar:
        details.append(note)

    start = '|IGNORE|' if item['name'].strip() in ignorelist else '|'
    return start + '|'.join(str(detail) for detail in details)

# {{FurnitureTable|ThemeIcon=FurnIcon_SET_ICON.png|Theme=SET_NAME|ThemeDesc=SET_DESCRIPTION
# |NAME|ICON|DESCRIPTION|RARITY|TYPE|COINS|GEMS|HAPPINESS|SIZE|QUANTITY(|NOTES)?
# }}

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    parser.add_argument('-l', '--lang', default='EN', help='language')
    parser.add_argument('-s', '--setname', help='build decor set table by name')
    parser.add_argument('-e', '--endbar', action='store_true', help='include last `|` in lines with no note')
    parser.add_argument('-i', '--itemname', help='build decor item entries by name')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_sharecfg
        dl_sharecfg('decorset', ['EN', 'CN', 'JP'], [
            'backyard_theme_template',
            'furniture_data_template',
            'furniture_shop_template',
            'shop_furniture_relation'
        ])
    init_decorset(args.lang)
    if args.setname:
        tid = get_themeid(args.setname)
        build_decorset(tid, args.endbar)
    elif args.itemname:
        items = get_items(args.itemname)
        lines = [build_decoritem(item, args.endbar) for item in items]
        with open('output/decoritem.wiki', 'w', encoding='utf-8') as fp:
            fp.write('\n'.join(lines) + '\n')
    else:
        from urllib.request import urlopen
        html = urlopen('https://azurlane.koumakan.jp/wiki/Decorations?action=raw')
        whole = html.read().decode()
        section = whole.split('== Furniture without Set ==')[1].split('== List of Furniture Sets ==')[0]
        ignorelist = re.findall('\n\|\s*(.+?)\s*\|', section)
        build_decorset('0', args.endbar)
