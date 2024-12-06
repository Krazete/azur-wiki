import os
import re
import UnityPy
from UnityPy.files import BundleFile
from pathlib import Path

assetbundles = UnityPy.load('AssetBundles')

outpaths = {
    'Texture2D': set(),
    # 'Sprite': set(),
    # 'TextAsset': set()
}

iconnames = {
    'collectionfileillustration': 'Collectfile {}',
    'equips': 'EquipSkinIcon {}', # revert for non-skin gear
    'furnitureicon': 'FurnIcon {}',
    'mangapic': 'Manga {}',
    'skillicon': 'Skill {}',
    'spweapon': 'Augment {}',
    'strategyicon': 'Buff {}'
}

shipassets = {
    'herohrzicon': '{}Banner',
    'qicon': '{}ChibiIcon',
    'shipmodels': '{}Chibi',
    'shipyardicon': '{}ShipyardIcon',
    'squareicon': '{}Icon'
}

shipnames = { # run buildskinname to check what these should be
    # 2024-07-02
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
    'z47': 'Z47',
    # 2024-07-11
    'aijier_3': 'ÄgirSpring',
    'aersasi': 'Alsace',
    'beiyade': 'Bayard',
    'dashan': 'Daisen',
    'haerfude': 'Halford',
    'haitian_5': 'Hai TienSpring2',
    'nabulesi': 'Napoli',
    'naximofu': 'Admiral Nakhimov',
    # 2024-07-25
    'dipulaikesi': 'Dupleix',
    'dipulaikesi_2': 'DupleixRaceQueen',
    'guogan': 'L\'Audacieux',
    'guogan_2': 'L\'AudacieuxRaceQueen',
    'haman_6': 'HammannRaceQueen',
    'luoma_4': 'RomaSummer',
    'ruihe_4': 'ZuikakuRaceQueen2',
    'sitelasibao': 'Strasbourg',
    'sitelasibao_2': 'StrasbourgRaceQueen',
    'u96_4': 'U-96RaceQueen',
    'xiafei_4': 'JoffreRaceQueen',
    'xia_alter': 'Kasumi META',
    # 2024-08-15
    'aierdeliqi_g': 'EldridgeKai',
    'ankeleiqi_h': 'AnchorageWedding',
    'banerwei_3': 'PainlevéSummer',
    'beier_2': 'BellWild West',
    'beier': 'Bell',
    'dujiaoshou_11': 'UnicornSport',
    'fage_2': 'FargoWild West',
    'fage': 'Fargo',
    'feiteliedadi_2': 'Friedrich der GroßeNew Year',
    'feiteliedadi_3': 'Friedrich der GroßeSummer',
    'feiteliedadi_h': 'Friedrich der GroßeWedding',
    'feiteliedadi': 'Friedrich der Große',
    'feiyu_2': 'HerringWild West',
    'feiyu': 'Herring',
    'kaiersheng_3': 'KersaintWild West',
    'pizibao_2': 'PittsburghWild West',
    'pizibao': 'Pittsburgh',
    'u556_2': 'U-556Party',
    'u556_3': 'U-556Wild West',
    'u556': 'U-556',
    'yindianna_2': 'IndianaWild West',
    'yindianna': 'Indiana',
    # 2024-08-29
    'lingbo_10': 'AyanamiParty',
    'ruifeng': 'Zuihou',
    'ruifeng_2': 'ZuihouTheme Park',
    # 2024-09-05
    'changmen_alter': 'Nagato META',
    'huangjiafangzhou_6': 'Ark RoyalTheme Park',
    'muyue_5': 'MutsukiTheme Park',
    'yuekecheng_alter': 'Yorktown META',
    # 2024-09-12
    'beierfasite_9': 'BelfastTheme Park',
    'birui_alter': 'Hiei META',
    'chicheng_alter': 'Akagi META',
    'chuixue_7': 'FubukiSpring',
    'dulianglai_2': 'WataraseParty',
    'dulianglai': 'Watarase',
    'huangjianfangzhou_6': 'Ark RoyalTheme Park', # dupe of huangjiafangzhou_6
    'liangbo_2': 'SuzunamiTheme Park',
    'liangbo': 'Suzunami',
    'linglai_2': 'AyaseHome Relaxation',
    'linglai': 'Ayase',
    'malilan_g': 'MarylandKai',
    'tiancheng_cv_2': 'Amagi(CV)Party',
    'tiancheng_cv': 'Amagi(CV)',
    'xiefeierde_6': 'SheffieldTheme Park',
    'z35_4': 'Z35Theme Park',
    # 2024-09-19
    'dingan_3': 'Ting AnTheme Park',
    'geluosite_2': 'GloucesterSpring',
    'geluosite_3': 'GloucesterTheme Park',
    'longxiang_4': 'RyuujouTheme Park',
    'lupuleixite_3': 'Prinz RupprechtTheme Park',
    'tianlangxing': 'Sirius',
    'tianlangxing_5': 'SiriusTheme Park',
    'wuzang_3': 'MusashiTheme Park',
    'bulaimodun_6': 'BremertonTheme Park',
    'jianye_5': 'KashinoTheme Park',
    # 2024-09-26 (3D Dorm Update)
    'xianghe_h': 'ShoukakuWedding',
    'xufulun_3': 'SuffrenParty',
    'bisimai_h': 'BismarckWedding',
    'fengxiang_alter': 'Houshou META',
    'fusang_h': 'FusouWedding',
    'bailong_4': 'HakuryuuFestival',
    'qiye_6': 'EnterpriseParty',
    # 2024-10-24 (tempesta/halloween)
    'aidang_6': 'AtagoHalloween',
    'bulisituoer_3': 'BristolHalloween',
    'gangyishawa': 'Ganj-i-Sawai',
    'gangyishawa_2': 'Ganj-i-SawaiHalloween',
    'gaoxiong_6': 'TakaoNinja',
    'haitunhao': 'Dolphin',
    'haitunhao_2': 'DolphinHalloween',
    'hemuhao': 'Amity',
    'hemuhao_2': 'AmityHalloween',
    'huanxianghao': 'Fancy',
    'huanxianghao_2': 'FancyHalloween',
    'pucimaosi': 'Portsmouth Adventure',
    'pucimaosi_2': 'Portsmouth AdventureHalloween',
    'weizhang_3': 'OwariHalloween',
    # 2024-11-21 (To LOVE-Ru)
    'aersasi_2': 'AlsaceSummer',
    'aogusite_3': 'August von ParsevalHome Relaxation',
    'bisimaiz_2': 'Bismarck ZweiSummer',
    'bulaimodun_3': 'BremertonSport',
    'dingan_2': 'Ting AnSpring',
    'kaisa_alter': 'Giulio Cesare META',
    'luodeni_alter': 'Rodney META',
    'weixi_5': 'WeserMaid',
    'wuerlixi_4': 'Ulrich von HuttenSchool',
    'lala_tolove': 'Lala Satalin Deviluke',
    'lala_2_tolove': 'Lala Satalin DevilukeHome Relaxation',
    'nana_tolove': 'Nana Astar Deviluke',
    'nana_2_tolove': 'Nana Astar DevilukeHome Relaxation',
    'mengmeng_tolove': 'Momo Belia Deviluke',
    'mengmeng_2_tolove': 'Momo Belia DevilukeHome Relaxation',
    'jinseanying_tolove': 'Golden Darkness',
    'jinseanying_2_tolove': 'Golden DarknessHome Relaxation',
    'xiliansi_tolove': 'Haruna Sairenji',
    'xiliansi_2_tolove': 'Haruna SairenjiHome Relaxation',
    'gushouchuan_tolove': 'Yui Kotegawa',
    'gushouchuan_2_tolove': 'Yui KotegawaHome Relaxation',
}

# extract asset types as listed in outpaths
for obj in assetbundles.objects:
    if not (obj.assets_file and obj.assets_file.assetbundle and obj.assets_file.assetbundle.m_Name):
        continue
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
            shipname = shipnames.get(asset.name.lower().replace('_hx', ''), asset.name)
            if '_hx' in asset.name:
                shipname += 'CN'
            outpath = Path(parent, template.format(shipname))
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
            asset.image.save('{}.png'.format(outpath))
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
    <Event Name> Event Banner EN.png
    [[Category:Event banners]]
Cruise Mission Menu
    Cruise Missions Season <Season Number>.jpg
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
'''
