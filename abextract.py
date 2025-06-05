import os
import re
import UnityPy
from UnityPy.files import BundleFile
from pathlib import Path
from SHIP import shipnames

assetbundles = UnityPy.load('AssetBundles')

outpaths = {
    'Texture2D': set(),
    # 'Sprite': set(),
    # 'TextAsset': set()
}

iconnames = {
    'activitymedal': 'AlbumSticker {}',
    'collectionfileillustration': 'Collectfile {}',
    'combatuistyle': 'BattleUI {}',
    'equips': 'EquipSkinIcon {}', # revert for non-skin gear
    'furnitureicon': 'FurnIcon {}',
    'mangapic': 'Manga {}',
    'skillicon': 'Skill {}',
    'spweapon': 'Augment {}',
    'strategyicon': 'Buff {}'
}

regexsubs = {
    'props': {
        r'^ui(\d+)$': 'BattleUIPack \g<1>',
        r'^ui_(\d+)$': 'BattleUIIcon \g<1>'
    }
}

shipassets = {
    'herohrzicon': '{}Banner',
    'qicon': '{}ChibiIcon',
    'shipmodels': '{}Chibi',
    'shipyardicon': '{}ShipyardIcon',
    'squareicon': '{}Icon'
}

# extract asset types as listed in outpaths
for obj in assetbundles.objects:
    if not (obj.assets_file and obj.assets_file.assetbundle and obj.assets_file.assetbundle.m_Name):
        continue
    assetfile = obj.assets_file.assetbundle.m_Name
    if obj.type.name in outpaths:
        asset = obj.read()
        parent = Path(obj.type.name, assetfile).parent
        outpath = Path(parent, asset.m_Name)
        # prepend icon labels in certain folders
        if parent.name in iconnames:
            outpath = Path(parent, iconnames[parent.name].format(asset.m_Name))
        elif parent.name in regexsubs:
            for reg in regexsubs[parent.name]:
                sub = regexsubs[parent.name][reg]
                if re.match(reg, asset.m_Name):
                    outpath = Path(parent, re.sub(reg, sub, asset.m_Name))
                    continue
        # move ship assets to special folder
        elif parent.name in shipassets:
            template = shipassets[parent.name]
            parent = Path(parent.parent, 'SHIP')
            shipname = shipnames.get(asset.m_Name.lower().replace('_hx', ''), asset.m_Name)
            if '_hx' in asset.m_Name:
                shipname += 'CN'
            outpath = Path(parent, template.format(shipname))
        elif parent.name == 'paintingface':
            if asset.m_Name == '0':
                print('WARNING: There is a 0-index expression within {}.'.format(assetfile))
                print('         Inspect the output for this sprite and edit Texture2D/SHIP/azur-paint.txt')
                print('         by adding "-f {} -t 0" to appropriate lines as necessary.'.format(assetfile.split('/')[-1]))
        # increment duplicate names
        i = 0
        inc = ''
        while str(outpath) + inc in outpaths[obj.type.name]:
            i += 1
            inc = ' ({})'.format(i)
        outpath = str(outpath) + inc
        outpaths[obj.type.name].add(outpath)
        # save
        os.makedirs(parent, exist_ok=True)
        if obj.type.name in ['Texture2D', 'Sprite']:
            try:
                asset.image.save('{}.png'.format(outpath))
                if parent.name == 'activitybanner':
                    asset.image.convert('RGB').save('{}.jpg'.format(outpath))
            except PermissionError:
                print('PermissionError for asset.image: \'{}\''.format(assetfile))
                continue
        else:
            with open(outpath, 'wb') as fp:
                fp.write(asset.script.tobytes())

# generate azur-paint commands
painting = Path('AssetBundles/painting')
if painting.is_dir():
    cmds = []
    for fn in os.listdir(painting):
        if Path(painting, fn).is_file() and '_tex' not in fn:
            shipname = shipnames.get(re.sub('_n|_hx|_bj|_rw', '', fn), fn)
            cmds.append('{}{}python -m main2 {}-p {} -o "{}{}{}{}{}"'.format( # warning: often nonstandard
                'IGNORE: ' if '_bj' in fn or '_rw' in fn else '',
                'UNNAMED: ' if shipname == fn else '',
                '-c ' if '_n' in fn else '',
                fn,
                shipname,
                'CN' if '_hx' in fn else '',
                'WithoutBG' if '_n' in fn else '',
                'WithoutShipgirl' if '_bj' in fn else '',
                'WithoutRigging' if '_rw' in fn else ''
            ))
    if len(cmds):
        os.makedirs('Texture2D/SHIP', exist_ok=True)
        with open('Texture2D/SHIP/azur-paint.txt', 'wb') as fp:
            fp.write(bytes('\n'.join(cmds), 'utf-8'))

'''
Notes on Names, Data Templates, and Categories

SHIP Images
    {{SkinFileData|<Ship Name>}}
Skill Icon
    [[Category:Skill icons]]
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

Akashi Shop Icons
    [[Category:Shop icons]]

Battle UI
    [[Category:Battle UI previews]]
'''
