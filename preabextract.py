import os
import re
import json
from datetime import date
import buildskinname

paintings = set()
for root, dirs, files in os.walk(os.path.join('AssetBundles')):
    for file in files:
        if re.match(r'^AssetBundles[\\/]painting(?:face)?$', root):
            paint = re.sub(r'(_(rw|tex|hx|bj|n|shophx))+$', '', file)
            assert paint == paint.lower()
            paintings.add(paint)

buildskinname.main()
with open('output/skinname.json', 'r', encoding='utf-8') as fp:
    skinname = json.load(fp)

print('Paintings Found:')
for paint in paintings:
    status = ''
    if paint in buildskinname.base_fixes:
        status = '[OK] Base Manually Fixed'
    elif paint in buildskinname.type_fixes:
        status = '[OK] Type Manually Fixed'
    elif paint in skinname:
        status = '[??] Automatically Named'
    else:
        status = '[!!] Skin Name Not Found'
    print('{}: {} ({})'.format(status, skinname.get(paint, 'UNDEFINED'), paint))
