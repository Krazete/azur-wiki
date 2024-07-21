import os
import json
import re
from argparse import ArgumentParser

skinbox = {}

def init_skin():
    '''Initializes `skinbox` object with JSON files downloaded from AzurLaneData repo.'''
    with open('EN/ShareCfg/equip_skin_theme_template.json', 'r', encoding='utf-8') as fp:
        skinbox['theme'] = json.load(fp)
    with open('EN/ShareCfg/equip_skin_template.json', 'r', encoding='utf-8') as fp:
        skinbox['item'] = json.load(fp)

def get_themeid(name):
    '''Get theme id by set name or name fragment.'''
    for tid in skinbox['theme']:
        if tid != 'all' and name in skinbox['theme'][tid]['name']:
            return tid
    return '0'

equiptype = {
    (1, 2, 3): 'DD/CL/CA',
    (4, 11): 'BB',
    (5, 13): 'Trp/SS',
    (7,): 'Ftr',
    (8,): 'TB',
    (9,): 'DB',
    (10,): 'Aux'
}

def build_skinbox(tid=None):
    '''Build a wikitable from AzurLaneData files.'''
    theme = skinbox['theme'].get(tid, {'name': 'NO THEME', 'ids': []})
    lines = [
        '{{{{EquipSkinTable|ThemeIcon={}_GearSkinBox.png|Theme={}'.format(
            theme['name'].strip().replace(' ', '_'),
            theme['name'].strip()
        )
    ]

    themeids = [str(iid) for iid in theme['ids']]
    iids = themeids + list(skinbox['item'])
    visited = {'all'}
    for iid in iids:
        if iid in visited:
            continue
        visited.add(iid)
        item = skinbox['item'][iid]
        if str(item['themeid']) == tid or tid == None:
            line = build_skinitem(item)
            if iid not in themeids and tid != None:
                print('SPECIAL/WRONG:', item['name'])
            lines.append(line)
    lines.append('}}')

    os.makedirs('output', exist_ok=True)
    page = '\n'.join(lines) + '\n'
    with open('output/skinbox.txt', 'w', encoding='utf-8') as fp:
        fp.write(page)

def build_skinitem(item):
    '''Build a wikitable item entry line.'''
    iid = str(item['id'])
    itype = tuple(item['equip_type'])
    details = [
        re.sub('(\S)\(', '\g<1> (', item['name']).strip(),
        item['icon'],
        re.sub('\s+', ' ', re.sub('<.+?>', ' ', item['desc'])).strip(),
        equiptype.get(itype, '<EQUIP_TYPE_{}>'.format(itype))
    ]
    return '|' + '|'.join(details)

# {{EquipSkinHeader|ThemeIcon=SET_ICON_GearSkinBox.png|Theme=SET_NAME
# |NAME|ICON|DESCRIPTION|{{TYPE_ID}} TYPE<br>{{TYPE2_ID}} TYPE2
# }}
# set name may not be the same as subpage title (e.g. set Port Café is on page Equipment_Skins/Café)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    parser.add_argument('-s', '--setname', help='build equip skin table by name')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_skin
        dl_skin()
    if args.setname:
        init_skin()
        tid = get_themeid(args.setname)
        build_skinbox(tid)
    else:
        init_skin()
        build_skinbox()
