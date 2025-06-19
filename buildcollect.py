import os
import re
import json
from argparse import ArgumentParser

collection = {}

hardsubs = {
    # id_2: filename (on square folder icon) # folder name (if different)
    # '011': 'Aerolith Incident',
    # '021': 'Energy Revolution',
    # '031': 'Tech & Life',
    # '032': 'New Lifestyle',
    # '033': 'Cube Militarization',
    # '041': 'Cube Militarization II',
    '051': 'Glimmer Project', # Project Dusk
    '061': 'Mystery of the Cube', # Mysterious
    '071': 'Code G', # Mysterious
    '081': 'Arms Race', # Global Affairs
    '091': 'Confidential I', # Mysterious
    '101': 'Cold War Escalation', # Global Affairs II
    # '111': 'College Life',
    '113': 'Creator and Magister', # Creator and Magister (different spaces)
    # '115': 'Present and Future',
    # '116': 'Technological Competition',
    # '131': 'Breaking News I',
    # '132': 'Breaking News II',
    # '133': 'Global Crisis',
    # '141': 'Richard Files I',
    # '142': 'Richard Files II',
    # '143': 'Richard Files III',
    # '144': 'Richard Files IV',
    # '146': 'Richard Archives I',
}

def init_collection():
    for suffix in ['group', 'template']:
        with open('EN/ShareCfg/world_collection_file_{}.json'.format(suffix), 'r', encoding='utf-8') as fp:
            collection[suffix] = json.load(fp)

def build_page():
    lines = [
        'For information on how to obtain these files, see [[List_of_Operation_Siren_Zones#Record_Files|here]].',
        '',
        '== Archives ==',
        'The following tables show the contents of the collectable records as they presently appear in the EN servers of the game.<br/>',
        '',
        '<tabber>'
    ]
    first = True
    for gid in collection['group']:
        if gid == 'all':
            continue
        group = collection['group'][gid]

        tabtitle = '{} - {}='.format(group['id_2'], hardsubs.get(group['id_2'], group['name']))
        if first:
            lines += [tabtitle, '']
            first = False
        else:
            lines += ['|-|{}'.format(tabtitle), '']
        
        for cid in group['child']:
            child = collection['template'][str(cid)]
            idname = '{} - {}'.format(child['group_ID'], child['name'])
            lines += ['==== {} ===='.format(idname), '']
            # picPresent = False
            if child['pic']:
                 lines += ['[[File:Collectfile {0}.png|thumb|alt={1}|{1}]]'.format(child['pic'], idname), '']
                #  picPresent = True
            if child['subTitle'] and child['subTitle']:
                lines += ['<tt>{}</tt>'.format(child['subTitle']), '']
            lines.append(re.sub('\n', '<br>', child['content']))
            # lines.append('<div style="clear: both;"></div>' if picPresent else '')
            lines.append('')
    lines += [
        '</tabber>',
        '',
        '== Historical references ==',
        '',
        '* 011 - Aerolith Incident, IV - Military Blockade Announcement: The latitude and longitude match the location of the [[:wikipedia:Tunguska event|Tunguska event]], which occurred at 7:17 local time on 30 June 1908 at 60° 53′ 9″ N, 101° 53′ 40″ E.',
        '* 091 - Confidential I, 6 - Log: GGORN0296: The image shows a [[:wikipedia:United States Navy officer rank insignia|United States Navy officer rank insignia]]. The stripe indicates a rank of Chief Warrant Officer 2. Above the stripe is an aviation specialty device.',
        '',
        '[[Category:Operation Siren]]',
        ''
    ]

    os.makedirs('output', exist_ok=True)
    with open('output/collection.wiki', 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(lines))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import update
        update(['EN'], [
            'ShareCfg/world_collection_file_group',
            'ShareCfg/world_collection_file_template'
        ])
    init_collection()
    build_page()
