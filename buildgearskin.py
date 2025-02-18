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
    with open('EN/sharecfgdata/item_data_statistics.json', 'r', encoding='utf-8') as fp:
        skinbox['box'] = json.load(fp)

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
    if tid == None: # then get item ids from all themes
        for thid in skinbox['theme']:
            if thid not in ['all', '199']: # 199 is Misc
                themeids += [str(iid) for iid in skinbox['theme'][thid]['ids']]
    iids = themeids + list(skinbox['item'])
    visited = {'all'}
    for iid in iids:
        if iid in visited:
            continue
        visited.add(iid)
        item = skinbox['item'].get(iid)
        if not item:
            print('Item {} does not exist in EN.'.format(iid))
        elif str(item['themeid']) == tid or tid == None:
            line = build_skinitem(item)
            if tid == None:
                for thid in skinbox['theme']:
                    if 'ids' in skinbox['theme'][thid] and int(iid) in skinbox['theme'][thid]['ids']:
                        line += '|THEME={}'.format(skinbox['theme'][thid]['name'])
                for bid in skinbox['box']:
                    if 'display_icon' in skinbox['box'][bid]:
                        for display in skinbox['box'][bid]['display_icon']:
                            if int(iid) == display[1]:
                                line += '|ICON={}'.format(skinbox['box'][bid]['icon'])
            if iid not in themeids:
                # print('SPECIAL/WRONG:', item['name'])
                line = '|SPECIAL/WRONG=' + iid + line
            lines.append(line)
    lines.append('}}')

    os.makedirs('output', exist_ok=True)
    page = '\n'.join(lines) + '\n'
    with open('output/skinbox.wiki', 'w', encoding='utf-8') as fp:
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
        from downloader import dl_from, dl_sharecfg
        dl_sharecfg('gearskin', ['EN'], [
            'equip_skin_theme_template',
            'equip_skin_template'
        ])
        dl_from('gearskin2', ['EN'], 'sharecfgdata', [
            'item_data_statistics'
        ])
    if args.setname:
        init_skin()
        tid = get_themeid(args.setname)
        build_skinbox(tid)
    else:
        init_skin()
        build_skinbox()
