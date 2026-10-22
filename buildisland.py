import json
import os
import re
from argparse import ArgumentParser
from root import root

with open('output/skindata.json', 'r', encoding='utf-8') as fp:
    skindata = json.load(fp)
with open('output/namecode.json', 'r', encoding='utf-8') as fp:
    namecode = json.load(fp)

# project identity fixes
skindata.append(['9900010', 0, 0, 0, 0, 'Navi'])
skindata.append(['9900020', 0, 0, 0, 0, 'TB'])
skindata.append(['9900030', 0, 0, 0, 0, 'Lora'])
iconfixes = {
    'Oceana': 'Navi',
    'Explorer': 'Lora',
    'Workerjuu': 'Unknown',
}

book = {}

def init_book(lang='EN'):
    files = {
        'ShareCfg/island_npc_hud': 'npc',
        'ShareCfg/island_chara_template': 'char',
        'ShareCfg/island_skin_template': 'skin',
        'ShareCfg/island_unit_character': 'desc',
        'ShareCfg/island_chara_skill': 'skill',
    }
    for file in files:
        path = '{}/{}.json'.format(lang, file)
        with open(root + path, 'r', encoding='utf-8') as fp:
            cat = files[file]
            book[cat] = json.load(fp)

def rename_files():
    for root, dirs, files in os.walk('Texture2D'):
        for file in files:
            if 'islandcharicon' in root:
                unnamed = True
                for datum in skindata:
                    if str(datum[0]) + '0' == file[:-4]:
                        print('{}Island'.format(datum[5]), 'SHIPGIRL')
                        unnamed = False
                if unnamed:
                    for chid in book['npc']:
                        if chid + '00' == file[:-4]:
                            print('{}Island'.format(book['npc'][chid]['name']), 'NPC')
                            unnamed = False
                if unnamed:
                    print(file, 'NOT FOUND')
            if 'islanddressicon' in root:
                print(file)                
            if 'islandinvitation' in root:
                print(file)                
            if 'islandshipicon' in root:
                print(file)                

def format_charname(charname):
    if 'namecode' in charname:
        ncid = re.findall(r'\d+', charname)
        charname = namecode[ncid[0]]
    iconname = charname
    if charname in iconfixes:
        iconname = iconfixes[charname]
    return '{{{{Display|{}Icon||{}}}}}'.format(iconname, charname)

def main():
    sects = {}
    for chid in book['char']:
        if not chid.isdigit():
            continue
        char = book['char'][chid]
        if char['skill_id'] in sects:
            sects[char['skill_id']][-1] += format_charname(char['name'])
            continue
        
        sect = []
        for skid in book['skill']:
            if not skid.isdigit():
                continue
            skill = book['skill'][skid]
            if char['skill_id'] == skill['id']:
                sect.append('data-sort-value={}|{{{{Display|{}}}}}'.format(
                    re.sub('chara_all_skill_', '', skill['icon']),
                    re.sub('chara_all_skill_', 'IslandSkill ', skill['icon'])
                ))
                sect.append(skill['name'])
                desc = skill['desc']
                for i, da in enumerate(skill['desc_add']):
                    desc = re.sub(
                        '(\${}%)'.format(i + 1),
                        '{}% ({}%)'.format(da[0][0], da[-1][0]),
                        desc
                    )
                    desc = re.sub(
                        '(\${})'.format(i + 1),
                        '{} ({})'.format(da[0][0], da[-1][0]),
                        desc
                    )
                sect.append(desc)
        sect.append(format_charname(char['name']))
        sects[char['skill_id']] = sect

    lines = []
    for sid in sects:
        lines += sects[sid] + ['-']
    with open('output/island.wiki', 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(['|{}'.format(line) for line in lines]))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    parser.add_argument('-l', '--lang', default='EN', help='language code: EN, CN, JP')
    parser.add_argument('-r', '--rename', action='store_true', help='rename images with shipgirl names')
    args = parser.parse_args()

    if args.download:
        import buildskinname
        from downloader import update
        buildskinname.main(True)
        update([args.lang], [
            'ShareCfg/island_npc_hud',
            'ShareCfg/island_chara_template',
            'ShareCfg/island_skin_template',
            'ShareCfg/island_unit_character',
            'ShareCfg/island_chara_skill',
        ])
    init_book(args.lang)
    if args.rename:
        rename_files()
    main()
