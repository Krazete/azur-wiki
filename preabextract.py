import os
import re
import json
import buildskinname
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-s', '--skip', action='store_true', help='skip downloading data files')
args = parser.parse_args()

paintings = set()
for root, dirs, files in os.walk(os.path.join('AssetBundles')):
    for file in files:
        if re.match(r'^AssetBundles[\\/]painting(?:face)?$', root):
            paint = re.sub(r'(_(rw|tex|hx|bj|n|shophx))+$', '', file)
            assert paint == paint.lower()
            paintings.add(paint)

buildskinname.main(not args.skip)
with open('output/skinname.json', 'r', encoding='utf-8') as fp:
    skinname = json.load(fp)

print('Paintings Found:')
for paint in sorted(paintings):
    status = ''
    if paint in buildskinname.fixes:
        status = '[OK] Manually Fixed'
    elif paint in skinname:
        status = '[??] Automatic Name'
    else:
        status = '[!!] Name Not Found'
    print('{}: {} ({})'.format(status, skinname.get(paint, 'UNDEFINED'), paint))
