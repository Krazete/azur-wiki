import os
import json
import re
from argparse import ArgumentParser
from github import Github

decor = {}

def dl_decor():
    '''Downloads JSON files relevant to Furniture from AzurLaneData repo.'''
    repo = Github().get_repo('AzurLaneTools/AzurLaneData')
    for lang in ['CN', 'EN', 'JP']:
        os.makedirs('{}/ShareCfg'.format(lang), exist_ok=True)
        pathName = '{}/ShareCfg/backyard_theme_template.json'.format(lang)
        content = repo.get_contents(pathName)
        with open(pathName, 'wb') as fp:
            fp.write(content.decoded_content)

def init_decor():
    '''Initializes `decor` object with JSON files downloaded from AzurLaneData repo.'''
    for lang in ['CN', 'EN', 'JP']:
        with open('{}/ShareCfg/backyard_theme_template.json'.format(lang), 'r', encoding='utf-8') as fp:
            decor[lang] = json.load(fp)
    
    # pocky theme has no icon
    decor['EN']['54']['icon'] = 'pockyheziicon'

def get_current_info():
    '''Get supplementary data from the List of Furniture Sets section on the wiki Decorations page.'''
    # Before running this, copy the textarea content on
    # https://azurlane.koumakan.jp/w/index.php?title=Decorations&action=edit&section=8
    # and paste it into the `input/decorchartnow.txt` file.
    pattern = re.compile('\| (\d+)\n(?:.+\n){4}((?:.+\n)+?)\|[-}]')
    info = {}
    with open('input/decorchartnow.txt', 'r', encoding='utf-8') as fp:
        matches = re.findall(pattern, fp.read())
        for match in matches:
            assert len(match) == 2
            assert match[0] not in info
            info.setdefault(match[0], match[1])
    return info

def build_decor():
    '''Build a wikitable from AzurLaneData files and current wiki page info.'''
    info = get_current_info()
    
    lines = [
        '== List of Furniture Sets ==',
        '',
        '{| class="wikitable" style="text-align: center;"',
        '! rowspan="2" | ID',
        '! rowspan="2" | Icon',
        '! colspan="3" | Set Name',
        '! colspan="3" | Availability',
        '! rowspan="2" | Associated Event',
        '|-',
        '! EN',
        '! CN',
        '! JP',
        '! EN',
        '! CN',
        '! JP'
    ]

    names = {}
    keys = []
    for lang in decor:
        names[lang] = {}
        for key in decor[lang]:
            names[lang][key] = decor[lang][key]
        keys += decor[lang]['all']
    for key in set(keys):
        id = str(key)
        themeCN = decor['CN'].get(id, {})
        themeEN = decor['EN'].get(id, {})
        themeJP = decor['JP'].get(id, {})
        icon = themeCN.get('icon') or themeEN.get('icon') or themeJP.get('icon')
        lines += [
            '|-',
            '| {}'.format(id),
            '| [[File:FurnIcon {}.png|60px]]'.format(icon),
            ('| [[Furniture Sets/{0}|{0}]]' if themeEN.get('is_view') else '| {}').format(themeEN.get('name', '--').strip()),
            '| {}'.format(themeCN.get('name', '--').strip()),
            '| {}'.format(themeJP.get('name', '--').strip()),
            info.get(id)[:-1]
        ]
    lines.append('|}')
    
    os.makedirs('output', exist_ok=True)
    page = '\n'.join(lines) + '\n'
    with open('output/decorchart.txt', 'w', encoding='utf-8') as fp:
        fp.write(page)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download decor files')
    args = parser.parse_args()
    if args.download:
        dl_decor()
    init_decor()
    build_decor()
