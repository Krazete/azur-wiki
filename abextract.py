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

ignored = [
    'activityuitable',
    'aircrafticon',
    'artresource',
    'backyardtheme',
    'buildpainting',
    'chapter', # battle bg objects
    'char', # chibi spine models
    'chargo',
    'clutter',
    'cue', # voice audio
    'dorm3d', # 3d models
    'effect',
    'extra_page',
    'furnitrues',
    'guildpainting',
    'item',
    'levelmap',
    'linkbutton',
    'linkbutton_mellow',
    'live2d',
    'map',
    'metapainting',
    'metaship',
    'metaworldboss',
    'model',
    'orbit',
    'painting',
    'paintingface',
    'scenes',
    'sfurniture',
    'shipdesignicon',
    'shopbanner',
    'shoppainting',
    'spinepainting',
    'storyicon',
    'technologyshipicon',
]

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
        # don't save
        if not parent.parts[1:] or parent.parts[1] in ignored: # also ignores root folder files
            continue
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
                'IGNORE: ' if '_bj' in fn or '_rw' in fn or '_wjz' in fn else '',
                'UNNAMED: ' if shipname == fn else '',
                '-c ' if '_n' in fn else '',
                fn,
                shipname,
                'CN' if '_hx' in fn else '',
                'WithoutBG' if '_n' in fn else '',
                'WithoutShipgirl' if '_bj' in fn else '',
                'WithoutRigging' if '_rw' in fn else '',
                'WithoutRigging' if '_wjz' in fn else ''
            ))
    if len(cmds):
        os.makedirs('Texture2D/SHIP', exist_ok=True)
        with open('Texture2D/SHIP/azur-paint.txt', 'wb') as fp:
            fp.write(bytes('\n'.join(cmds), 'utf-8'))
