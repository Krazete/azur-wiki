import os
import json
from PIL import Image
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-d', '--download', action='store_true', help='download data files')
args = parser.parse_args()
if args.download:
    from downloader import update
    update(['EN'], ['ShareCfg/activity_coloring_template'])

os.makedirs('output/drawingbook/small', exist_ok=True)
os.makedirs('output/drawingbook/big', exist_ok=True)

letters = 'abcdefghijklmnopqrstuvwxyz'
txts = []
mats = set()

with open('EN/ShareCfg/activity_coloring_template.json', 'r') as fp:
    dbs = json.load(fp)
    for id in dbs:
        if id != 'all':
            db = dbs[id]
            name = '[{:04d}] {}'.format(db['id'], db['name'])
            colors = [
                (0, 0, 0, 0),
                *(tuple(round(0xff * n) for n in c) for c in db['colors'])
            ]
            matrix = [[' ' for x in range(db['theme'][1])] for y in range(db['theme'][0])]
            im = Image.new('RGBA', (db['theme'][1], db['theme'][0]))
            for cell in db['cells']:
                matrix[cell[0]][cell[1]] = letters[cell[2] - 1]
                im.putpixel((cell[1], cell[0]), colors[cell[2]])
            mat = ''.join(''.join(row) for row in matrix)
            if db['name'] == 'NO.1' and len(txts):
                txts[-1] += '\n</tabber>\n'
            txts.append('\n'.join([
                '<tabber>' if db['name'] == 'NO.1' else '|-|',
                db['name'].replace('O.', 'º ') + '=',
                '{{DrawingBook',
                *('|{}=rgb({}, {}, {})'.format(letters[i], *c) for i, c in enumerate(colors[1:])),
                *('|' + ''.join(row) for row in matrix),
                '}}' + (' <!--DUPLICATE-->' if mat in mats else '')
            ]))
            mats.add(mat)
            im.save('output/drawingbook/small/{}.png'.format(name))
            IM = im.resize((20 * n for n in im.size), resample=Image.NEAREST)
            IM.save('output/drawingbook/big/{}.png'.format(name))
    txts[-1] += '\n</tabber>\n'

with open('output/drawingbook/all.wiki', 'w', encoding='utf-8') as fp:
    fp.write('\n'.join(txts))
