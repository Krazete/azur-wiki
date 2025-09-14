import os
import json
import re
from argparse import ArgumentParser

decor = {}
decorshop = {}

def init_decor():
    '''Initializes `decor` object with JSON files downloaded from AzurLaneData repo.'''
    for lang in ['CN', 'EN', 'JP']:
        with open('{}/ShareCfg/backyard_theme_template.json'.format(lang), 'r', encoding='utf-8') as fp:
            decor[lang] = json.load(fp)
    
    # pocky theme has no icon
    decor['EN']['54']['icon'] = 'pockyheziicon'

    with open('EN/ShareCfg/furniture_shop_template.json', 'r', encoding='utf-8') as fp:
        decorshop['EN'] = json.load(fp)

def get_current_info():
    '''Get supplementary data from the List of Furniture Sets section on the wiki Decorations page.'''
    pattern = re.compile('\| (\d+)\n(?:.+\n){4}((?:.+\n)+?)\|[-}]')
    info = {}
    with open('input/decornow.wiki', 'r', encoding='utf-8') as fp:
        matches = re.findall(pattern, fp.read())
        for match in matches:
            assert len(match) == 2
            assert match[0] not in info
            info.setdefault(match[0], match[1])
    return info

def formatTime(year, month, day):
    months = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    return '{:02d} {} {}'.format(day, months[month], year)

def formatTimes(time0, time1):
    ft0 = formatTime(*time0)
    ft1 = formatTime(*time1)
    if ft0[-4:] == ft1[-4:]:
        ft0 = ft0[:-5]
    return '{} - {}'.format(ft0, ft1)

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
        if key == 126: # skip atelier yumia trio
            continue
        id = str(key)
        themeCN = decor['CN'].get(id, {})
        themeEN = decor['EN'].get(id, {})
        themeJP = decor['JP'].get(id, {})
        icon = themeCN.get('icon') or themeEN.get('icon') or themeJP.get('icon')
        times = '--'
        if themeEN:
            decortime = decorshop['EN'].get(str(themeEN['ids'][0]), {}).get('time', '--')
            if decortime == 'always':
                times == 'Permanent'
            elif isinstance(decortime, list):
                times = formatTimes(decortime[0][0], decortime[1][0])
        lines += [
            '|-',
            '| {}'.format(id),
            '| [[File:FurnIcon {}.png|60px]]'.format(icon),
            ('| [[Furniture Sets/{0}|{0}]]' if themeEN.get('is_view') else '| {}').format(themeEN.get('name', '--').strip()),
            '| {}'.format(themeCN.get('name', '--').strip()),
            '| {}'.format(themeJP.get('name', '--').strip()),
            info.get(id, '| colspan="3" | {}\n| [[{}]]'.format(times, 'EVENT')).strip()
        ]
    lines.append('|}')
    
    os.makedirs('output', exist_ok=True)
    page = '\n'.join(lines) + '\n'
    with open('output/decor.wiki', 'w', encoding='utf-8') as fp:
        fp.write(page)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_decor
        dl_decor()
    init_decor()
    build_decor()
