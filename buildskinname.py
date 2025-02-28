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
    9997: 'Kai',
    9998: 'Wedding',
    9999: '_OTHER_9999', # other
}

book = {}

def init_book():
    '''Initializes `child` object with JSON files downloaded from AzurLaneData repo.'''
    files = {
        'ShareCfg/ship_skin_template': 'skin',
        'ShareCfg/name_code': 'code',
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
        return book['code'][cid]['name']
    return skin['name']

def build_skinnames():
    txtfile = ''
    jsonfile = {}

    incrementor = {}
    for sid in book['skin']:
        skin = book['skin'][sid]
        paint = skin['painting']
        stid = skin['shop_type_id']
        dual = 0 if skin['change_skin'] == '' else skin['change_skin']['index']
        base = book['skin'].get(str(10 * skin['ship_group']))
        if base:
            if skin['skin_type'] < 0: # default
                assert skin == base
                name = get_decoded_name(skin)
            else:
                name = get_decoded_name(base) + shop_type[stid]
            if dual > 1:
                name += 'Form{}'.format(dual)
        else: # likely an enemy or npc
            name = get_decoded_name(skin) + '_NO_BASE'
        for tid in book['tip']: # detect if skin is in Cruise Pass
            if 'battlepass_main_help' in tid:
                for tip in book['tip'][tid].get('tip', []):
                    if '_' in paint and '"' + skin['name'] in tip['info']:
                        name += ' (Travel?)'
        wikiname = '{}{}'.format(name, incrementor.get(name, ''))
        incrementor.setdefault(name, 1)
        incrementor[name] += 1
        txtfile += '{:8d} {:4d} {:32s} {}\n'.format(
            int(sid),
            int(stid),
            paint,
            wikiname
        )
        if base:
            if paint in jsonfile:
                print('WARNING: Painting file {} has extra name {}'.format(paint, wikiname))
            jsonfile.setdefault(paint, wikiname)
    with open('output/skinname.txt', 'w', encoding='utf-8') as fp:
        fp.write(txtfile)
    with open('output/skinname.json', 'w', encoding='utf-8') as fp:
        json.dump(jsonfile, fp, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_sharecfg, dl_from
        dl_sharecfg('shipnames', ['EN'], [
            'ship_skin_template',
            'name_code'
        ])
        dl_from('shipnames2', ['EN'], 'sharecfgdata', [
            'gametip'
        ])
    init_book()
    build_skinnames()
