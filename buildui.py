import json
import re
from downloader import dl_sharecfg
from argparse import ArgumentParser

def buildui():
    with open('EN/ShareCfg/pay_data_display.json', 'rb') as fp:
        shop = json.load(fp)
    with open('EN/ShareCfg/item_data_battleui.json', 'rb') as fp:
        ui = json.load(fp)
    lines = ['{{Image Gallery | width = 384']
    for id in ui:
        if id == 'all':
            continue
        lines.append('| BattleUI {}.png | {}\'\'\'{}\'\'\'<br>\'\'{}\'\'<br>Unlock: {}'.format(
            ui[id]['icon'],
            '' if ui[id]['unlock'] == 'Default' else re.sub('^ui_(\d+)$', '[[File:BattleUIIcon \g<1>.png|50px]]', ui[id]['display_icon']),
            re.sub('Battle UI\W+', '', ui[id]['name']),
            ui[id]['desc'],
            '[[Akashi\'s Shop]]' if 'Buy' in ui[id]['unlock'] else '[[Cruise Missions|{}]]'.format(ui[id]['unlock'])
        ))
    lines.append('}}')
    with open('output/ui.wiki', 'w') as fp:
        fp.write('\n'.join(lines))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        dl_sharecfg('idwontmattersoon', ['EN'], [
            'item_data_battleui',
            'pay_data_display'
        ])
    buildui()