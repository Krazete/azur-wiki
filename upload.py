import os
import re
from time import sleep
from mwclient import Site

def signin():
    global alw
    alw = Site('azurlane.koumakan.jp')
    with open('input/username', 'r') as fp:
        username = fp.read().strip()
    with open('input/password', 'r') as fp:
        password = fp.read().strip()
    alw.login(username, password)
    return alw

def uploadimage(path, content='', summary='', ignore=False):
    with open(path, 'rb') as fp:
        return alw.upload(fp, path.split('/')[-1], content, ignore=ignore, comment=summary)
    sleep(0.5)

def updateimage(path, summary='update'):
    uploadimage(path, '', summary, True)

patterns = {
    r'/activitybanner/': '[[Category:Event banners]]',
    r'/bg/Skin BG': '[[Category:Skin Backgrounds]]',
    r'/bg/Memory .+ Background \d+\.png': '[[Category:Memory backgrounds]]',
    r'/bg/Memory .+ CG \d+\.png': '[[Category:Memory artwork]]',
    r'/combatuistyle/': '[[Category:Battle UI previews]]',
    # r'/crusingwindow/': '[[Category:Event banners]]', # discontinued after Season 23
    r'/equips/EquipSkinIcon': '[[Category:Equipment Skins]]',
    r'/equips/\d+\.png': '[[Category:EQUIPMENTTYPE]]',
    r'/loadingbg/': '[[Category:Loading Screens]]',
    r'/mangapic/': '[[Category:Comics]]',
    r'/memoryicon/': '[[Category:Memory thumbnails]]',
    r'/props/BattleUIIcon': '[[Category:Shop icons]]',
    r'/props/.+ Pt\.png': '[[Category:Event point icons]]',
    r'/props/.+ GearSkinBox\.png': '{{ItemData|Props/FILENAME|BOXID|Gear Skin Box (BOXNAME)}}\n[[Category:Equipment skin boxes]]',
    r'/props/.+ SelectionSkinBox\.png': '{{ItemData|Props/FILENAME|BOXID|Selection Gear Skin Box (BOXNAME)}}\n[[Category:Equipment skin boxes]]',
    r'/SHIP/': '{{SkinFileData|SHIPGIRLNAME}}',
    r'/skillicon/': '[[Category:Ship skill icons]]',
    r'/spweapon/': '[[Category:Augment Module]]',
    r'/strategyicon/': '[[Category:Buff icons]]',
}

if __name__ == '__main__':
    py = 'from upload import signin, uploadimage\nsignin()\n'
    for root, dirs, files in os.walk('Texture2D'):
        for file in files:
            path = '{}/{}'.format(root.replace('\\', '/'), file)
            content = ''
            for pattern in patterns:
                if re.search(pattern, path):
                    content = patterns[pattern]
                    break
            py += 'uploadimage(\'{}\', \'{}\')\n'.format(path, content).replace(', \'\'', '')
    with open('output/UPLOADING.py', 'w') as fp:
        fp.write(py)
