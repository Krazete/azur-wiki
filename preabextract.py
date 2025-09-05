import os
import re
import json
from datetime import date
import buildskinname

paintings = set()
for root, dirs, files in os.walk(os.path.join('AssetBundles')):
    for file in files:
        if re.match(r'^AssetBundles[\\/]painting(?:face)?$', root):
            paintings.add(re.sub(r'(_(rw|tex|hx|bj|n|shophx))+$', '', file))

buildskinname.main()
with open('output/skinname.json', 'r', encoding='utf-8') as fp:
    skinname = json.load(fp)
    skinnamelower = {painting.lower(): skinname[painting] for painting in skinname}

with open('SHIP.py', 'r', encoding='utf-8') as fp:
    SHIP = fp.read()
with open('SHIP.py', 'w', encoding='utf-8') as fp:
    comment = '\n    # {} ()\n'.format(date.today().isoformat())
    content = '\n'.join('    \'{}\': \'{}\','.format(
        painting,
        re.sub(r'\'', '\\\'', skinnamelower.get(painting.lower(), 'UNKNOWN'))
    ) for painting in sorted(paintings))
    closure = '\n}\n'
    fp.write(re.sub(closure, comment + content + closure, SHIP))
