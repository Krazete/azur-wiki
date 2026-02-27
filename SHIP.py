import re

shipnames = { # run buildskinname to check what these should be
    # 2024-09-12
    'chicheng_alter': 'Akagi META',
    # 'huangjianfangzhou_6': 'Ark RoyalTheme Park', # typo dupe of huangjiafangzhou_6
    # 2024-09-26 (3D Dorm Update)
    'xufulun_3': 'SuffrenParty',
    # 2024-10-24 (tempesta/halloween)
    'gaoxiong_6': 'TakaoNinja',
    # 2024-11-21 (To LOVE-Ru)
    'weixi_5': 'WeserMaid',
    # 2024-12-12
    'moon': 'Arbiter: The Moon XVIII',
    # 2025-01-23 (Project Identity: Oceana)
    'lingyangzhe1_1': 'NaviBaby',
    'lingyangzhe1_2': 'NaviBabySchool',
    'lingyangzhe21_1': 'NaviMildTeen',
    'lingyangzhe22_1': 'NaviRebelliousTeen',
    'lingyangzhe22_2': 'NaviTeen',
    'lingyangzhe31_1': 'NaviMild',
    'lingyangzhe31_2': 'NaviMildCasual',
    'lingyangzhe32_1': 'NaviRebellious',
    'lingyangzhe32_2': 'NaviRebelliousCasual',
    'lingyangzhe32_3': 'Navi',
    'npclingyangzhe3_2': 'NaviHome RelaxationWithoutBG',
    # 2025-02-20
    'npcandelieyaduoliya_alter': 'NPCAndrea Doria META',
    # 2025-02-27 (A Day After Kizuna AI Returned)
    'chariot': 'Arbiter: The Chariot VII',
    'missr': 'Bon Homme RichardSchool',
    'shenpanjizhanche': 'MECHArbiter: The Chariot',
    # 2025-05-14 (Wednesday Update)
    'npcgelunweier_alter': 'NPCGrenville META',
    'npcguangrong_alter': 'NPCGlorious META',
    'shuixingjinian_6': 'Pamiat\' MerkuriaEvent',
    # 2025-05-20 (Tuesday Update)
    'magician': 'Arbiter: The Magician I',
    'npcchuyue_3': 'NPCHatsuzukiTravel',
    'npcfeiteliekaer_3': 'NPCFriedrich CarlSummer',
    'npcheianjie_alter': 'NPCErebus META',
    'npcjunzhu_5': 'NPCMonarchSummer',
    'npckewei_6': 'NPCFormidableParty2',
    'npclieren_alter': 'NPCHunter META',
    'npcmalilan_3': 'NPCMarylandSummer',
    'star': 'Star',
    'unknownstar': 'Arbiter: The Star XVII',
    # 2025-07-17
    'bulvxieer_4': 'BlücherSchool',
    # 2025-09-04 (Call to Arms: Amahara)
    'ryouko_shallow': 'Ryouko AmaharaShadow',
    # 2025-09-12 (Amahara)
    'i404_3': 'I-404NinjaEX',
    'npcaersasi_3': 'NPCAlsaceNinja',
    'npcbulunnusi_3': 'NPCBrennusFestival',
    'npcguandao_3': 'NPCGuamNinja',
    'npcjiasikenie_3': 'NPCGascogneFestival',
    'npclafeiii_4': 'NPCLaffey IIFestival',
    'npcyanzhan_4': 'NPCWarspiteNinja',
    'npcyunxian_3': 'NPCUnzenNinja',
    # 2025-09-25 (Amahara Week 3)
    'jiangfeng_3': 'KawakazeNinjaTravel',
    'tiancheng_h': 'AmagiWedding',
    # 2025-12-04 (Popularity Vote start)
    'midchicheng_alter': 'Akagi META (Akagi)',
}

dupes = set()
for id in shipnames:
    shipnames[id] = re.sub(r'[<>:"/\\|?*]+', '', shipnames[id])
    shipname = shipnames[id]
    if shipname in dupes:
        print('WARNING: Duplicate ship name: {}'.format(shipname))
    dupes.add(shipname)
