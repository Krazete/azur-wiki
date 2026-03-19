import json
import re
from argparse import ArgumentParser

shop_type = { # inconsistent (e.g. luoma_4 should be Summer, not RaceQueen; Bluray is unaccounted for)
    0: '_OTHER_0000',
    1: 'Christmas',
    2: 'New Year',
    3: 'Spring',
    4: 'School',
    6: 'Summer',
    7: 'Party',
    8: 'Halloween',
    9: 'Casual',
    10: 'Festival',
    11: 'Idol',
    12: 'Special Exercise',
    13: 'Sport',
    14: 'RaceQueen',
    15: 'Hospital',
    16: 'Bunny',
    17: 'Maid',
    18: 'Vampire',
    19: 'Fairy Tale',
    20: 'Home Relaxation',
    21: 'Dance',
    22: 'Hot Springs',
    23: 'Work',
    24: 'RPG',
    25: 'Wild West',
    26: 'Theme Park',
    27: 'Nile Colors',
    28: 'Ninja',
    9997: 'Kai',
    9998: 'Wedding',
    9999: '_OTHER_9999', # other
}
ship_class = { # from SharedCfg/ship_data_by_type.json and SharedCfg/enemy_data_by_type.json
    1: 'DD', # Destroyer
    2: 'CL', # Light Cruiser
    3: 'CA', # Heavy Cruiser
    4: 'BC', # Battlecruiser
    5: 'BB', # Battleship
    6: 'CVL', # Light Carrier
    7: 'CV', # Aircraft Carrier
    8: 'SS', # Submarine
    9: 'Aviation Cruiser',
    10: 'BBV', # Aviation Battleship
    11: 'Torpedo Cruiser',
    12: 'AR', # Repair Ship
    13: 'BM', # Monitor
    14: 'Torpedo Ship',
    15: 'Cargo Ship',
    16: 'Bombing Ship',
    17: 'SSV', # Aviation Submarine
    18: 'CB', # Large Cruiser
    19: 'AE', # Munition Ship
    20: 'DD', # Guided-Missile Destroyer (Vanguard)
    21: 'DDG', # Guided-Missile Destroyer (Main)
    22: 'IXs', # Sailing Frigate (Submarine)
    23: 'IXv', # Sailing Frigate (Vanguard)
    24: 'IXm', # Sailing Frigate (Main)
    25: 'Unknown',
}

fixes = {
    # painting: {'base': base name, 'type': suffix or shop type id}
    # base only
    'hdn101': {'base': 'Neptune (Neptunia)'},
    'xia_doa': {'base': 'Kasumi (Venus Vacation)'},
    'xuebugui': {'base': 'Fubuki (Senran Kagura)'},
    'tbniang_hei': {'base': 'TB'},
    'lingyangzhe32_3': {'base': 'Navi'},
    'unknown1': {'base': 'Tester'},
    'unknown1_xinshou': {'base': 'Tester'},
    'unknown2_memory': {'base': 'Observer'},
    'unknown5': {'base': 'Compiler'},
    'unknown5_shadow': {'base': 'Compiler'},
    'hierophant': {'base': 'Arbiter: The Hierophant V'},
    'moon': {'base': 'Arbiter: The Moon XVIII'},
    'unknownstar': {'base': 'Arbiter: The Star XVII'},
    'machinemagician': {'base': 'MECHArbiter: The Magician I'},
    'baolei1': {'base': 'MECHWar Protocol Fortress'},
    'leftchicheng_alter': {'base': 'Akagi META (Kaga)'},
    'rightchicheng_alter': {'base': 'Akagi META (Amagi)'},
    'midchicheng_alter': {'base': 'Akagi META (Akagi)'},
    'ryouko_shallow': {'base': 'Ryouko Amahara'},
    'gaoxiong_dark': {'base': 'Takao META'},
    'gaoxiong_dark_shadow': {'base': 'Takao META'},
    # type only
    'gin_2': {'type': 'Event'},
    'kin_2': {'type': 'Event'},
    'buli_super_2': {'type': 'Event'},
    'suweiaitongmeng': {'type': 'Original2'},
    'dahuangfeng_dark_shadow': {'type': 'OriginalShadow'},
    'luoma_4': {'type': 6},
    'gangute_2': {'type': 'Prison'},
    'gangute_3': {'type': 9},
    'linghangyuan1_1': {'type': 'Baby'},
    'npcaersasi_3': {'type': 28},
    'xufulun_3': {'type': 7},
    'gaoxiong_6': {'type': 28},
    'weixi_5': {'type': 17},
    'shuixingjinian_6': {'type': 'Event'},
    'bulvxieer_4': {'type': 4},
    'missr': {'type': 4},
    'i404_3': {'type': 'NinjaEX'},
    'luoen_3': {'type': 'Crosswave'},
    'aijiang': {'type': 'WithoutRigging'},
    'npcchuyue_3': {'type': 'Travel'}, # Hatsuzuki
    'npcfeiteliekaer_3': {'type': 6}, # Friedrich Carl
    'npcjunzhu_5': {'type': 6}, # Monarch
    'npckewei_6': {'type': 'Party2'}, # Formidable
    'npcmalilan_3': {'type': 6}, # Maryland
    'npcaersasi_3': {'type': 28}, # Alsace
    'npcbulunnusi_3': {'type': 10}, # Brennus
    'npcguandao_3': {'type': 28}, # Guam
    'npcjiasikenie_3': {'type': 10}, # Gascogne
    'npclafeiii_4': {'type': 10}, # Laffey II
    'npcyanzhan_4': {'type': 28}, # Warspite
    'npcyunxian_3': {'type': 28}, # Unzen
    # base and type
    'linghangyuan1_5': {'base': 'TB', 'type': 'BabyPlushie'},
    'lingyangzhe1_1': {'base': 'Navi', 'type': 'Baby'},
    'lingyangzhe1_2': {'base': 'Navi', 'type': 'BabySchool'},
    'lingyangzhe21_1': {'base': 'Navi', 'type': 'MildTeen'},
    'lingyangzhe22_1': {'base': 'Navi', 'type': 'RebelliousTeen'},
    'lingyangzhe22_2': {'base': 'Navi', 'type': 'Teen'},
    'lingyangzhe31_1': {'base': 'Navi', 'type': 'Mild'},
    'lingyangzhe31_2': {'base': 'Navi', 'type': 'MildCasual'},
    'lingyangzhe32_1': {'base': 'Navi', 'type': 'Rebellious'},
    'lingyangzhe32_2': {'base': 'Navi', 'type': 'RebelliousCasual'},
    'lingyangzhe3_2': {'base': 'Navi', 'type': 20},
    'npclingyangzhe3_2': {'base': 'Navi', 'type': 'Home RelaxationWithoutBG'},
    # shadows
    'qiye_dark': {'base': 'Enterprise META'}, # not shadow
    'qiye_dark_shadow': {'base': 'Enterprise META'},
    'dadouquan_dark_shadow': {'base': 'Bulldog'},
    'abeikelongbi_2_dark_shadow': {'base': 'Abercrombie', 'type': 'HalloweenShadow'},
    'aerjiliya_hei': {'base': 'Algérie'},
    'ailunsamuna_hei': {'base': 'Allen M. Sumner'},
    'suweiaibeilaluosi_hei': {'base': 'Sovetskaya Belorussiya'},
    'yuekecheng_alter_hei': {'base': 'Yorktown META'},
    'gangute_dark': {'base': 'Gangut', 'type': 'Shadow'},
    'qiabayefu_dark': {'base': 'Chapayev', 'type': 'Shadow'},
    'shuixingjinian_dark': {'base': 'Pamiat\' Merkuria', 'type': 'Shadow'},
    'suweiailuoxiya_dark': {'base': 'Sovetskaya Rossiya', 'type': 'Shadow'},
    'suweiaitongmeng_dark': {'base': 'Sovetsky Soyuz', 'type': 'Shadow'},
    'tashigan_dark': {'base': 'Tashkent', 'type': 'Shadow'},
    'weiyan_dark': {'base': 'Grozny', 'type': 'Shadow'},
}

book = {}

def init_book():
    '''Initializes `child` object with JSON files downloaded from AzurLaneData repo.'''
    files = {
        'ShareCfg/ship_skin_template': 'skin',
        'ShareCfg/name_code': 'code',
        'sharecfgdata/ship_data_statistics': 'stat',
        'sharecfgdata/shop_template': 'shop',
        'sharecfgdata/gametip': 'tip'
    }
    for file in files:
        path = 'EN/{}.json'.format(file)
        with open(path, 'r', encoding='utf-8') as fp:
            cat = files[file]
            book[cat] = json.load(fp)

def get_decoded_name(skin):
    if 'namecode' in skin['name']:
        matches = re.match('{namecode:(\d+)}', skin['name'])
        cid = matches[1]
        return book['code'][cid]['name'].strip()
    name = re.sub(r'\s+', ' ', skin['name']) # only affects Reisalin Stout
    return name.strip()

def get_painting_lower(skin):
    return skin['painting'].lower()

def build_skinnames():
    txtfile = ['{:>8s} {:>4s} {:>4s} {:>4s} {:32s} {}'.format('SkinID', 'Shop', 'BG', 'NPC', 'Painting', 'Filename / Title')]
    jsonfile = {}
    wikifile = []

    suffix_incrementor = {}
    for skid in book['skin']:
        skin = book['skin'][skid]
        paint = get_painting_lower(skin)
        tyid = skin['shop_type_id']
        bg = skin['bg'] or 0

        skinname = get_decoded_name(skin)
        basename = skinname
        suffix = ''
        npc = False

        dual = False
        l2d = skin['ship_l2d_id']
        dyn = skin['spine_offset']

        soup = skin['ship_group']
        base = book['skin'].get(str(soup * 10))
        if base:
            basename = get_decoded_name(base)
            basepaint = get_painting_lower(base)
            if basepaint in fixes and fixes[basepaint].get('base'):
                basename = fixes[basepaint]['base']
            if skin['skin_type'] < 0: # default
                if skin != base:
                    print('WARNING: Skin "{}" incorrectly detected as {}\'s default.'.format(skin['name'], base['name']))
            else:
                suffix = shop_type[tyid]
                for tid in book['tip']: # detect if skin is in Cruise Pass
                    if 'battlepass_main_help' in tid:
                        for tip in book['tip'][tid].get('tip', []):
                            if '_' in paint and '"' + skin['name'] in tip['info']:
                                suffix = 'Travel'
            if isinstance(skin['change_skin'], dict): # detect if skin is dual-form or asmr
                form = skin['change_skin']['index']
                if skin['change_skin'].get('asmr'):
                    suffix += 'ASMR' # so far, asmr skins have the same sprite as default
                elif form > 1:
                    suffix += 'Form{}'.format(form)
                    dual = True
                elif skin['change_skin'].get('action') != 'changeAsmr':
                    dual = True
        else: # likely an enemy or npc
            npc = True
            if paint in fixes and fixes[paint].get('base'):
                basename = fixes[paint]['base']

        miscat = []
        extra_fixes = {
            r'^\w+?_alter$': ('META', 0),
            r'^\w+?_hei$': ('Shadow', 1),
            r'^\w+?_shadow$': ('Shadow', 1),
            r'^\w+?_shallow$': ('Shadow', 1),
            r'^\w+?_memory$': ('Memory', 1),
            r'^\w+?_ghost$': ('Ghost', 1),
            r'^\w+?-ui$': ('UI', 1),
            r'^\w+?_xinshou$': ('CN', 1),
            r'^\w+?_wjz$': ('WithoutRigging', 1),
            r'^\w+?_idolns$': ('WithoutRigging', 1),
            r'^\w+?_s$': ('WithoutRigging', 1),
            r'^\w+?_n$': ('WithoutBG', 1),
        }
        for cat in extra_fixes:
            if re.match(cat, paint) and not basename.endswith(extra_fixes[cat][0]):
                miscat.append(extra_fixes[cat])
        for cat in miscat:
            if cat[1] == 0:
                basename += ' ' + cat[0]
            elif cat[1] == 1:
                suffix = cat[0]
        # if len(miscat):
        #     print('WARNING: {} ({}) has been automatically amended: {}'.format(basename, paint, ', '.join([cat[0] for cat in miscat])))

        if paint in fixes and fixes[paint].get('type'):
            typefix = fixes[paint]['type']
            if isinstance(typefix, int):
                suffix = shop_type[typefix]
            else:
                suffix = typefix
        if 'npc' in paint:
            suffix += ' NPC'

        if not npc:
            suffix_incrementor.setdefault(basename + suffix, 0)
            suffix_incrementor[basename + suffix] += 1
        n = suffix_incrementor.get(basename + suffix, 0)
        suffix_n = '{}{}'.format(suffix, n) if n > 1 else suffix
        wikiname = '{}{}'.format(basename, suffix_n)

        classification = ''
        rarities = {} # histogram of rarities; lower count = npc (usually)
        for stid in book['stat']:
            stskid = book['stat'][stid]['skin_id']
            if stskid == int(skid) or stskid // 10 == soup:
                classification = ship_class[book['stat'][stid]['type']]
                r = str(book['stat'][stid]['rarity'])
                rarities.setdefault(r, 0)
                rarities[r] += 1
        rarity = ''
        if not npc and len(rarities) > 0:
            maxrcount = max(rarities.values())
            maxr = [r for r in rarities if rarities[r] == maxrcount] # prefers first recorded rarity
            rarity = maxr[0]
            # if len(maxr) > 1: # note if tiebreaker was used
            #     print('WARNING: Skin {} ({}) has multiple rarities ({})'.format(skid, wikiname, ', '.join(maxr)))

        listing = book['shop'].get(str(skin['shop_id']), {})
        price = listing.get('resource_num', 0)

        txtfile.append('{:8d} {:4d} {:4d} {:4s} {:32s} {}'.format(
            int(skid),
            int(tyid),
            int(bg),
            'NPC' if npc else '',
            paint,
            wikiname # + ('' if wikiname == skinname else ' / {}'.format(skinname))
        ))
        if paint in jsonfile:
            if jsonfile[paint][0]:
                jsonfile[paint] = (npc, wikiname)
            elif jsonfile[paint][1] != wikiname and not npc:
                print('WARNING: Skin {} ({}) has extra name ({})'.format(skid, jsonfile[paint][1], wikiname))
        else:
            jsonfile[paint] = (npc, wikiname)
        if suffix == '' and basename == skinname:
            wikifile.append('{{{{{}}}}}'.format('|'.join([
                'ShipDisplay',
                rarity,
                basename,
                classification,
                suffix,
                '' if npc else '\'\'\'Construction\'\'\''
            ])))
        else:
            wikifile.append('{{{{{}}}}}'.format('|'.join([
                'ShipDisplay',
                rarity,
                basename,
                classification,
                suffix_n,
                skinname,
                '{{{{Gem}}}} {}'.format(price) if price else '', # notes
                '' if listing.get('time') == 'always' else '1', # limited
                'DUAL' if dual else 'L2D' if l2d else 'DYN' if dyn else '', # live2d
                str(bg) if bg else ''
            ])))
        wikifile[-1] = re.sub(r'\|+?\}\}$', '}}', wikifile[-1]) # strip end
    with open('output/skinname.txt', 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(txtfile))
    with open('output/skinname.json', 'w', encoding='utf-8') as fp:
        json.dump({x: jsonfile[x][1] for x in jsonfile}, fp, ensure_ascii=False, indent=4)
    with open('output/skintemplate.wiki', 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(wikifile))

    # detect duplicates; overwrites could happen otherwise
    dump = {x: jsonfile[x][1] for x in jsonfile}
    dupes = set()
    for id in dump:
        dump[id] = re.sub(r'[<>:"/\\|?*]+', '', dump[id])
        shipname = dump[id]
        if shipname in dupes:
            print('WARNING: Duplicate ship name: {}'.format(shipname))
        dupes.add(shipname)

def main(dl):
    if dl:
        from downloader import update
        update(['EN'], [
            'ShareCfg/ship_skin_template',
            'ShareCfg/name_code',
            'sharecfgdata/ship_data_statistics',
            'sharecfgdata/shop_template',
            'sharecfgdata/gametip'
        ])
    init_book()
    build_skinnames()

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    main(args.download)
