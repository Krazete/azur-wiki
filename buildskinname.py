import json
import re

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
ship_class = {
    1: 'DD', # Destroyer
    2: 'CL', # Light Cruiser
    3: 'CA', # Heavy Cruiser
    4: 'BC', # Battlecruiser
    5: 'BB', # Battleship
    6: 'CVL', # Light Aircraft Carrier
    7: 'CV', # Aircraft Carrier
    8: 'SS', # Submarine
    10: 'BBV', # Aviation Battleship
    12: 'AR', # Repair Ship
    13: 'BM', # Monitor
    17: 'SSV', # Submarine Aircraft Carrier
    18: 'CB', # Large Cruiser
    19: 'AE', # Munition Ship
    20: 'DD', # Guided-Missile Destroyer (Vanguard)
    21: 'DDG', # Guided-Missile Destroyer (Main)
    22: 'IXs', # Sailing Frigate (Submarine)
    23: 'IXv', # Sailing Frigate (Vanguard)
    24: 'IXm', # Sailing Frigate (Main)
}

base_fixes = {
    'hierophant': 'Arbiter: The Hierophant V',
    'lingyangzhe3_2': 'Navi',
}
type_fixes = {
    # painting: base (if string)
    # painting: shop_type_id (if int)
    'gin_2': 'Event',
    'kin_2': 'Event',
    'buli_super_2': 'Event',
    'lingyangzhe3_2': 20,
    'luoma_4': 6,
    'yuekecheng_hei': 'Shadow',
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
    return skin['name'].strip()

def build_skinnames():
    txtfile = ['{:>8s} {:>4s} {:>4s} {:>4s} {:32s} {}'.format('SkinID', 'Shop', 'BG', 'NPC', 'Painting', 'Filename / Title')]
    jsonfile = {}
    wikifile = []

    suffix_incrementor = {}
    for skid in book['skin']:
        skin = book['skin'][skid]
        paint = skin['painting']
        tyid = skin['shop_type_id']
        bg = skin['bg'] or 0

        skinname = get_decoded_name(skin)
        basename = skinname
        suffix = ''
        npc = False

        dual = False
        l2d = skin['ship_l2d_id']
        dyn = skin['shop_dynamic_hx']

        base = book['skin'].get(str(skin['ship_group'] * 10))
        if base:
            basename = get_decoded_name(base)
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
        else: # likely an enemy or npc
            npc = True

        if paint in base_fixes:
            basename = base_fixes[paint]
        if paint in type_fixes:
            if isinstance(type_fixes[paint], int):
                suffix = shop_type[type_fixes[paint]]
            else:
                suffix = type_fixes[paint]

        if npc:
            wikiname = '{}{}'.format(basename, suffix)
        else:
            wikiname = '{}{}{}'.format(basename, suffix, suffix_incrementor.get(basename + suffix, ''))
            suffix_incrementor.setdefault(basename + suffix, 1)
            suffix_incrementor[basename + suffix] += 1

        classification = ''
        rarities = set()
        for stid in book['stat']:
            if int(stid) // 10 == int(skid) // 10:
                classification = ship_class[book['stat'][stid]['type']]
                rarities.add(book['stat'][stid]['rarity'])
        rarity = rarities if rarities else 0

        listing = book['shop'].get(str(skin['shop_id']), {})

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
                print('WARNING: Painting file {} has extra name {}'.format(paint, wikiname))
        else:
            jsonfile[paint] = (npc, wikiname)
        wikifile.append('{{{{{}}}}}'.format('|'.join([
            'ShipDisplay',
            ','.join([str(r) for r in rarities]),
            basename,
            classification,
            suffix,
            skinname,
            '{{{{Gem}}}} {} {{{{Skin ticket}}}}'.format(listing.get('resource_num', 0)), # notes
            '' if listing.get('time') == 'always' else '1', # limited
            'DUAL' if dual else 'L2D' if l2d else 'DYN' if dyn else '', # live2d
            str(bg) if bg else ''
        ])))
    with open('output/skinname.txt', 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(txtfile))
    with open('output/skinname.json', 'w', encoding='utf-8') as fp:
        json.dump({x: jsonfile[x][1] for x in jsonfile}, fp, ensure_ascii=False, indent=4)
    with open('output/skintemplate.wiki', 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(wikifile))

def main():
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
    main()
