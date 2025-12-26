import os
import shutil
import re
from time import sleep
from mwclient import Site
from SHIP import shipnames

def signin(): # use https://azurlane.koumakan.jp/wiki/Special:BotPasswords
    global alw
    if 'alw' not in globals():
        alw = Site('azurlane.koumakan.jp')
    if not alw.logged_in:
        with open('input/username', 'r') as fp:
            username = fp.read().strip()
        with open('input/password', 'r') as fp:
            password = fp.read().strip()
        alw.login(username, password)
    return alw

def uploadimage(path, content='', summary='', ignore=False):
    with open(path, 'rb') as fp:
        pathsplit = path.split('/')
        response = alw.upload(fp, pathsplit[-1], content, ignore=ignore, comment=summary)
        result = response.get('result', 'Unknown')
        if result == 'Unknown':
            result = response.get('upload', {}).get('result', 'Unknown')
        print('{}: {}'.format(result, pathsplit[-1]))
        if result == 'Success':
            os.makedirs('Texture2D/_UPLOADED_/{}'.format('/'.join(pathsplit[1:-1])), exist_ok=True)
            shutil.move(path, 'Texture2D/_UPLOADED_/{}'.format('/'.join(pathsplit[1:])))
        else:
            print(response)
    sleep(0.5)

def updateimage(path, summary='update'):
    uploadimage(path, '', summary, True)

ships = []
for paintingname in shipnames:
    if '_' not in paintingname:
        ships.append(shipnames[paintingname])
ships.sort(key=lambda ship: -len(ship))

patterns = {
    r'/activitybanner/': '[[Category:Event banners]]',
    r'/activitymedal/': '[[Category:Commemorative Album stickers]]',
    r'/bg/Skin BG': '[[Category:Skin Backgrounds]]',
    r'/bg/Memory .+ Background \d+\.png': '[[Category:Memory backgrounds]]',
    r'/bg/Memory .+ CG \d+\.png': '[[Category:Memory artwork]]',
    r'/collectionfileillustration': '[[Category:Collection Archives images]]',
    r'/combatuistyle/': '[[Category:Battle UI previews]]',
    r'/commanderskillicon/': '[[Category:Meowfficer skill icons]]',
    # r'/crusingwindow/': '[[Category:Event banners]]', # discontinued after Season 23
    r'/equips/EquipSkinIcon': '[[Category:Equipment Skins]]',
    r'/equips/\d+\.png': '[[Category:EQUIPMENTTYPE]]',
    r'/iconframe': '[[Category:Portrait frames]]',
    r'/loadingbg/': '[[Category:Loading Screens]]',
    r'/mangapic/': '[[Category:Comics]]',
    r'/MEDALLION/': '[[Category:Medallions]]',
    r'/memoryicon/': '[[Category:Memory thumbnails]]',
    r'/props/BattleUI': '[[Category:Shop icons]]',
    r'/props/UR Voucher .+\.png': '[[Category:Event point icons]]',
    r'/props/.+ Pt\.png': '[[Category:Event point icons]]',
    r'/props/.+ GearSkinBox\.png': '{{ItemData|Props/FILENAME|BOXID|Gear Skin Box (BOXNAME)}}\\n[[Category:Equipment skin boxes]]',
    r'/props/.+ SelectionSkinBox\.png': '{{ItemData|Props/FILENAME|BOXID|Selection Gear Skin Box (BOXNAME)}}\\n[[Category:Equipment skin boxes]]',
    # r'/SHIP/': '{{SkinFileData|SHIPGIRLNAME}}', # handled separately
    r'/skillicon/': '[[Category:Ship skill icons]]',
    r'/spweapon/': '[[Category:Augment Module]]',
    r'/strategyicon/': '[[Category:Buff icons]]',
}

if __name__ == '__main__':
    py = 'from uploader import signin, uploadimage, updateimage\nsignin()\n'
    for root, dirs, files in os.walk('Texture2D'):
        if '_UPLOADED_' in root:
            continue
        for file in files:
            if file.endswith('.jpg') or file.endswith('.png'):
                path = '{}/{}'.format(root.replace('\\', '/'), file)
                content = ''
                if re.search(r'/SHIP/', path):
                    content = '{{SkinFileData|SHIPGIRLNAME}}'
                    for ship in ships:
                        if re.search(r'/SHIP/{}'.format(ship), path):
                            content = '{{{{SkinFileData|{}}}}}'.format(ship)
                            break
                else:
                    for pattern in patterns:
                        if re.search(pattern, path):
                            content = patterns[pattern]
                            break
                py += 'uploadimage(\'{}\', \'{}\')\n'.format(
                    path.replace('\'', '\\\''),
                    content.replace('\'', '\\\'')
                ).replace(', \'\'', '')
    with open('UPLOADING.py', 'w', encoding='utf-8') as fp:
        fp.write(py)

'''
Notes on Names, Data Templates, and Categories

SHIP Images
    {{SkinFileData|<Ship Name>}}
Skill Icon
    [[Category:Ship skill icons]]
Event Buff Icon
    [[Category:Buff icons]]

Siren Images
    Key Visual
        [[Category:Sirens]]
    Banner
        [[Category:Siren banner images]]
    Square Icon
        [[Category:Siren icons]]
    Chibi
        [[Category:Siren Chibi]]
    Chibi Icon
        [[Category:Siren Chibi icons]]
Human Images
    Key Visual
        [[Category:Humans]]
    Banner
        [[Category:Human banner images]]
    Square Icon
        [[Category:Human icons]]

Backgrounds
    star_level_bg_<BG ID>.png
        Skin BG <BG ID>.png
        [[Category:Skin Backgrounds]]
    bg_<Event ID>_<#>.png
        Memory <Event Name> Background <#>.png
        [[Category:Memory backgrounds]]
    bg_<Event ID>_cg<#>.png
        Memory <Event Name> CG <#>.png
        [[Category:Memory artwork]]
Event Point Icon
    <Name> Pt.png
    [[Category:Event point icons]]
Retrofit Material Icon
    <Name>.png
    [[Category:Retrofit material icons]]

Event Banner
    <Event Name> Event Banner EN.jpg
    [[Category:Event banners]]
Blueprint Completion Plan
    PR<Season Number> Catchup <Ship Name> Event Banner EN.jpg
    [[Category:Event banners]]
Cruise Mission Menu
    Cruise Missions Season <Season Number>.png
    [[Category:Event banners]]
Loading Screen
    Bg <YYYY>.<MM>.<DD> <Index>.png
    [[Category:Loading Screens]]
Manga / Comic
    [[Category:Comics]]

Memory Icon
    Memory <Story Title>.png
    [[Category:Memory thumbnails]]
Character Memory Folder
    <Ship Name>Memory.png
    [[Category:Character Memory folders]]
Hall of Fame Memory Icon
    <Ship Name>HallofFame.png
    [[Category:Memory thumbnails]]
Secret CD
    <Ship Name>Secret.png

Operation Siren Collection Archives Pictures
    [[Category:Collection Archives images]]

Commemorative Album Sticker
    [[Category:Commemorative Album stickers]]
Medallions
    <Medal Name> <Medal Rank>.png
    [[Category:Medallions]]

Gear / Equipment Skin
    [[Category:Equipment Skins]]
Gear / Equipment Skin Box
    <Box Name> GearSkinBox.png
    {{ItemData|Props/<File Name>|<Box ID>|Gear Skin Box (<Box Name>)}}
    [[Category:Equipment skin boxes]]
Gear / Equipment Skin Box (ALL)
    <Box Name> SelectionSkinBox.png
    {{ItemData|Props/<File Name>|<Box ID>|Selection Gear Skin Box (<Box Name>)}}
    [[Category:Equipment skin boxes]]

Augment
    [[Category:Augment Module]]
Gear / Equipment
    <Gear ID>.png
    check equip_data_statistics.json for gear categories
    [[Category:Auxiliary]]
    [[Category:Cargo]]
    [[Category:Depth Charge]]
    [[Category:Equipment]]
    [[Category:Sonar]]
    [[Category:AA Gun]]
    [[Category:BB Gun]]
    [[Category:CA Gun]]
    [[Category:CB Gun]]
    [[Category:CL Gun]]
    [[Category:DD Gun]]
    [[Category:ASW Bomber]]
    [[Category:Dive Bomber]]
    [[Category:Fighter]]
    [[Category:Seaplane]]
    [[Category:Torpedo Bomber]]
    [[Category:Submarine Torpedo]]
    [[Category:Torpedo]]
    sometimes:
        [[Category:Research-only Equipment]]

Portrait Frame
    <Frame ID>.png
    [[Category:Portrait frames]]

Sticker Set Icon
    Stickers <Prop ID>.png

Research Blueprint
    <Ship Name>SUnit.png
    no category
Research Blueprint (ALL)
    AllSUnit<Series Number>.png
    [[Category:Resource icons]]

META Crystal
    <Ship Name> METACrystal.png
UR Voucher
    UR Voucher <Ship Name>.png
    [[Category:Event point icons]]

Arcade Games
    <Game Name> Arcade Banner.png
    [[Category:Arcade banners]]

Akashi Shop Icons
    [[Category:Shop icons]]

Battle UI
    [[Category:Battle UI previews]]
'''
