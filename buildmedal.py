import os
import re
import json
import UnityPy
from UnityPy.files import BundleFile
from pathlib import Path
from argparse import ArgumentParser

medals = {}

def init_medals():
    with open('EN/ShareCfg/medal_template.json', 'r', encoding='utf-8') as fp:
        medal_template = json.load(fp)
        for id in medal_template:
            if id != 'all':
                try:
                    icon = medal_template[id]['icon']
                except:
                    continue
                if 'name' in medal_template[id] and '子' in medal_template[id]['name']:
                    continue
                medals[icon] = medal_template[id]

def abget_medals():
    assetbundles = UnityPy.load('AssetBundles/medal')
    for obj in assetbundles.objects:
        if not (obj.assets_file and obj.assets_file.assetbundle and obj.assets_file.assetbundle.m_Name):
            continue
        assetfile = obj.assets_file.assetbundle.m_Name
        if obj.type.name == 'Texture2D':
            asset = obj.read()
            try:
                int(asset.m_Name)
            except:
                continue
            outname = '{} {}'.format(medals[asset.m_Name]['name'], medals[asset.m_Name]['rank'])
            os.makedirs('Texture2D/MEDALLION', exist_ok=True)
            asset.image.save('Texture2D/MEDALLION/{}.png'.format(outname))

def build_medal():
    lines = [
        'Medals are miscellaneous items that can be used to decorate your Profile once unlocked. They do not provide any benefits at all, and are not to be confused with the Medals for Dorm decoration.',
        '',
        'Medals can be checked in the Medallion monument of the [[Academy]].',
        '',
        'Each Medal has multiple Ranks, and Rank 5 is the highest Medal rank possible currently.',
        '',
        '== Regular ==',
        '|- (this line will pop)']
    limited = []
    # regular medals
    currentname = ''
    for icon in medals:
        name = medals[icon]['name']
        if name != currentname:
            lines.pop()
            if currentname:
                lines.append('|}')
            if 'Event' in [medals[icon]['explain1'], medals[icon]['explain2']]:
                limited.append(icon)
                continue
            # explainsAreSwapped = medals[icon]['explain1'].endswith('.') or medals[icon]['explain2'] == 'Event'
            lines += [
                '',
                '=== {} ==='.format(name),
                '',
                '\'\'{}\'\''.format(re.sub('\s+', ' ', medals[icon]['desc'])),
                # '',
                # '{} {}'.format(
                #     medals[icon]['explain2'] if explainsAreSwapped else medals[icon]['explain1'],
                #     medals[icon]['explain1'] if explainsAreSwapped else medals[icon]['explain2']
                # ),
                '',
                '{| class="wikitable"',
                '!Rank',
                '!Icon',
                '!Requirements',
                '|-'
            ]
            currentname = name
        if medals[icon]['condition'] != 'Coming Soon':
            lines += [
                '|{}'.format(medals[icon]['rank']),
                '|[[File:{} {}.png|50px]]'.format(name, medals[icon]['rank']),
                '|{}'.format(medals[icon]['condition']),
                '|-'
            ]
    lines[-1] = '|}'
    # limited medals
    lines += [
        '',
        '== Limited ==',
        '',
        '{| class="wikitable"',
        '!Icon',
        '!Name',
        '!Description',
        '!Requirements',
        '|-'
    ]
    for icon in limited:
        name = medals[icon]['name']
        rank = medals[icon]['rank']
        condition = re.sub(
            '(stickers (?:from|in) )([\w\s\':]+)', '\g<1>[[\g<2>]]',
            re.sub(
                '"(.+?)"', '[[\g<1>]]',
                medals[icon]['condition']
            )
        )
        if medals[icon]['rank'] != 1:
            print('WARNING: Medal {} has a non-unary rank.'.format(rank))
        lines += [
            '|[[File:{} {}.png|50px]]'.format(name, rank),
            '|\'\'\'{}\'\'\''.format(name),
            '|\'\'{}\'\''.format(re.sub('\n+', '<br>', medals[icon]['desc'])),
            '|{}'.format(condition), # replace quotes with hyperlink to event page
            '|-'
        ]
    lines[-1] = '|}'
    page = '\n'.join(lines)
    with open('output/medallion.wiki', 'w', encoding='utf-8') as fp:
        fp.write(page) # will need revision

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    parser.add_argument('-e', '--extract', action='store_true', help='extract images from AssetBundles')
    parser.add_argument('-b', '--build', action='store_true', help='build Medallion page')
    args = parser.parse_args()
    if args.download:
        from downloader import update
        update(['EN'], ['ShareCfg/medal_template'])
    init_medals()
    if args.extract:
        abget_medals()
    if args.build:
        build_medal()