import os
import json
import re
from argparse import ArgumentParser

filelist = [
    'ShareCfg/activity_template',
    'sharecfgdata/task_data_template',
    'sharecfgdata/item_data_statistics',
    'sharecfgdata/item_virtual_data_statistics'
]

data = {}

def init_data():
    for file in filelist:
        with open('EN/{}.json'.format(file), 'rb') as fp:
            data[file.split('/')[-1]] = json.load(fp)

def build_tasklist():
    lines = []
    for taskid in [50112, 50136]:
        lines += [
            '{| class="wikitable"',
            '! Task Description',
            '! Rewards',
            '|-'
        ]
        for id in data['activity_template'][str(taskid)]['config_data']:
            task = data['task_data_template'][str(id)]
            imgs = []
            for awards in task['award_display']:
                for datatype in ['item_data_statistics', 'item_virtual_data_statistics', None]:
                    if datatype and str(awards[1]) in data[datatype]:
                        break
                if datatype:
                    datum = data[datatype][str(awards[1])]
                    imgs.append('{{{{Display|{}|{}|x{} {}|35}}}}'.format(
                        'Image {}'.format(datum['icon']), # item image
                        ['', 'N', 'R', 'E', 'SR', 'UR'][datum.get('rarity', 0)], # rarity
                        awards[2], # amount
                        datum['name'] # item name
                    ))
                else:
                    print('Unknown datatype for awards:', awards)
            lines += [
                '| {}'.format(task['desc']),
                '| {}'.format('; '.join(imgs)),
                '|-'
            ]
        lines[-1] = '|}'
    with open('output/tasks.txt', 'w') as fp:
        fp.write('\n'.join(lines))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import update
        update(['EN'], filelist)
    init_data()
    build_tasklist()
