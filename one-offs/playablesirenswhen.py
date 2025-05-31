import json
from argparse import ArgumentParser

with open('EN\GameCfg\dungeon.json', 'rb') as fp:
    battlesims = json.load(fp)
with open('EN\ShareCfg\memory_template.json', 'rb') as fp:
    chapters = json.load(fp)
with open('EN\ShareCfg\memory_group.json', 'rb') as fp:
    memories = json.load(fp)
with open('EN\ShareCfg\ship_skin_template.json', 'rb') as fp:
    skins = json.load(fp)

special_paintings = [
    'npcchicheng',
    'chicheng_alter',
    'leftchicheng_alter',
    'rightchicheng_alter',
    'midchicheng_alter',
    'npctiancheng',
    'missd',
    'strength',
    'temperance',
    'chariot',
    'shenpanjizhanche',
    'devil',
    'empress',
    'hermit',
    'hermit_alter',
    'hierophant',
    'lovers',
    'magician',
    'machinemagician',
    'moon',
    'yulun',
    'unknownstar',
    'starbeast',
    'tower',
    'sairenboss14_jz',
    'missr',
    'haorenlichade_alter',
    'kelei',
    'unknown5',
    'unknown5',
    'unknown5',
    'unknown5_shadow',
    'anjie',
    'anjie_hei',
    'aosita',
    'aosita_hei',
    'qiye_dark',
    'qiye_dark',
    'qiye_dark_shadow',
    'qiye_dark_shadow',
    'aisaikesi_alter',
    'youtuobiya',
    'npcjiahe',
    'enpuleisi',
    'madamm',
    'lingyangzhe3_2',
    'unknown2',
    'unknown2',
    'qiye_dark_memory',
    'unknown2_memory',
    'unknown4',
    'qingchuzhe',
    'unknown3',
    'unknown3',
    'unknown3_shadow',
    'silverfox',
    'silverfox_shadow',
    'suweiaitongmeng_dark',
    'suweiaitongmeng_wjz',
    'suweiaitongmeng',
    'safuke_xinshou',
    'gaoxiong_dark',
    'gaoxiong_dark_shadow',
    'tbniang',
    'linghangyuan1_5',
    'linghangyuan1_5',
    'linghangyuan1_1',
    'tbniang_hei',
    'unknown1',
    'unknown1_xinshou',
    'ligen',
    'baolei2',
    'baolei1',
    'unknown6',
    'lianren',
    'yuekecheng_alter',
    'yuekecheng_alter_hei'
]

special_prefabs = [
    'sairenboss11'
]

parser = ArgumentParser()
parser.add_argument('-s', '--skin', help='skin painting or prefab to search for')
args = parser.parse_args()
if args.skin:
    special_paintings.append(args.skin)
    special_prefabs.append(args.skin)

template = '{:12}{:12}{:12}{:24}{:24}{:36}{:48}{:12}'

print(template.format(
    'Dungeon ID',
    'Position',
    'Skin ID',
    'Painting',
    'Prefab',
    'Name',
    'Memory',
    'Chapter'
))

for bsid in battlesims:
    fleet = battlesims[bsid]['fleet_prefab']
    if fleet:
        for position in ['main', 'vanguard']:
            fpid = '{}_unitList'.format(position)
            if fpid in fleet:
                for unit in fleet[fpid]:
                    skid = str(unit['skinId'])
                    yay1 = [bsid, position[0].upper() + position[1:], skid]
                    if skid in skins:
                        skin = skins[skid]
                        if skin['painting'] in special_paintings or skin['prefab'] in special_prefabs:
                            yay2 = yay1 + [skin['painting'], skin['prefab'], skin['name']]
                            nochapters = True
                            for chid in chapters:
                                if bsid in chapters[chid]['story']:
                                    for mid in memories:
                                        memory = memories[mid]
                                        if int(chid) in memory['memories']:
                                            yay3 = yay2 + [memory['title'], str(memory['memories'].index(int(chid)) + 1)]
                                            print(template.format(*yay3))
                                            nochapters = False
                            if nochapters:
                                print(template.format(*(yay2 + ['NOT FOUND', '-'])))
                    else:
                        print(template.format(*(yay1 + ['NOT FOUND', '-', '-', '-', '-'])))
