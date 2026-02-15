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

def build_tasklist(year, month):
    lines = []
    for taskid in data['activity_template']:
        if taskid == 'all':
            continue
        time = data['activity_template'][taskid].get('time', [0, [[0, 0, 0]]])
        if not (isinstance(time, list) and time[1][0][0] == year and time[1][0][1] == month):
            continue
        lines += [
            '{| class="wikitable"',
            '! Task Description',
            '! Rewards',
            '|-'
        ]
        for id in data['activity_template'][str(taskid)]['config_data']:
            task = data['task_data_template'].get(str(id), {})
            imgs = []
            for awards in task.get('award_display', []):
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
                '| {}'.format(task.get('desc', 'NULL')),
                '| {}'.format('; '.join(imgs)),
                '|-'
            ]
        lines[-1] = '|}'
    with open('output/tasks.txt', 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(lines))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    parser.add_argument('-y', '--year', type=int, default='2026', help='year')
    parser.add_argument('-m', '--month', type=int, default='1',help='month')
    args = parser.parse_args()
    if args.download:
        from downloader import update
        update(['EN'], filelist)
    init_data()
    build_tasklist(args.year, args.month)
