import os
import UnityPy
from UnityPy.files import BundleFile
from pathlib import Path

assetbundles = UnityPy.load('AssetBundles')

outpaths = {
    'Texture2D': set(),
    'Sprite': set(),
    'TextAsset': set()
}

iconnames = {
    'equips': 'EquipSkinIcon {}', # revert for non-skins
    'furnitureicon': 'FurnIcon {}',
    'skillicon': 'Skill {}',
    'spweapon': 'Augment {}'
}

shipassets = {
    'herohrzicon': '{}Banner',
    'qicon': '{}ChibiIcon',
    'shipmodels': '{}Chibi',
    'shipyardicon': '{}ShipyardIcon',
    'squareicon': '{}Icon'
}

shipnames = {
    'aierdeliqi_8': 'EldridgeSchool2',
    'guanghui_7': 'IllustriousWork',
    'u31_2': 'U-31School',
    'u31': 'U-31',
    'yaerweite_2': 'AlvitrWork',
    'yaerweite': 'Alvitr',
    'yuekegongjue_4': 'Duke of YorkWork',
    'z43_2': 'Z43School',
    'z43': 'Z43',
    'z47_2': 'Z47School',
    'z47': 'Z47'
}

paintings = set()
cmds = []

for obj in assetbundles.objects:
    assetfile = obj.assets_file.assetbundle.m_Name
    if obj.type.name in outpaths:
        asset = obj.read()
        parent = Path(obj.type.name, assetfile).parent
        outpath = Path(parent, asset.name)
        # prepend icon labels in certain folders
        if parent.name in iconnames:
            outpath = Path(parent, iconnames[parent.name].format(asset.name))
        # move ship assets to special folder
        elif parent.name in shipassets:
            template = shipassets[parent.name]
            parent = Path(parent.parent, 'SHIP')
            shipname = shipnames.get(asset.name.lower(), asset.name)
            outpath = Path(parent, template.format(shipname))
        # generate azur-paint commands
        elif parent.name == 'painting' and '_tex' not in asset.name and asset.name not in paintings:
            cmd = 'python -m main2 {}-p {} -o {}{}{}'.format( # warning: often nonstandard
                '-c ' if '_n' in asset.name else '',
                asset.name,
                shipnames.get(asset.name, asset.name),
                'CN' if '_hx' in asset.name else '',
                'WithoutBackground' if '_n' in asset.name else ''
            )
            cmds.append(cmd)
        # iterate duplicate names
        i = 1
        while outpath in outpaths[obj.type.name]:
            outpath = '{} ({})'.format(outpath, i)
            i += 1
        outpaths[obj.type.name].add(outpath)
        # save
        os.makedirs(parent, exist_ok=True)
        if obj.type.name in ['Texture2D', 'Sprite']:
            asset.image.save('{}.png'.format(outpath))
        else:
            with open(outpath, 'wb') as fp:
                fp.write(asset.script.tobytes())

with open('Texture2D/SHIP/azur-paint.txt', 'w') as fp:
    fp.write('\n'.join(cmds))
