import os
import re
import json
from urllib.parse import quote
from argparse import ArgumentParser

langs = {
    'EN': 'English',
    'CN': 'Chinese',
    'JP': 'Japanese'
}
book = {}

tb = False # set True to quick fix Project Identity: TB issues

def init_book():
    '''Initializes `child` object with JSON files downloaded from AzurLaneData repo.'''
    subpaths = {
        'ShareCfg/memory_group': 'group',
        'ShareCfg/memory_template': 'memory',
        'ShareCfg/ship_skin_template': 'skin',
        'ShareCfg/name_code': 'code',
        'GameCfg/story': 'story',
        'GameCfg/dungeon': 'battle'
    }
    for lang in langs:
        for subpath in subpaths:
            cat = subpaths[subpath]
            path = '{}/{}.json'.format(lang, subpath)
            with open(path, 'r', encoding='utf-8') as fp:
                book.setdefault(cat, {})
                book[cat][lang] = json.load(fp)
        if tb:
            for i in range(1000, 2000):
                book['skin'][lang][str(i)] = {
                    'ship_group': 90284,
                    'shop_type_id': 9999
                }

def get_groupid(title):
    '''Get memory group id by title or title fragment.'''
    for gid in book['group']['EN']:
        if title in book['group']['EN'][gid]['title']:
            return gid

def getwikiname(skinid, lang):
    skin = book['skin'][lang].get(str(skinid))
    if not skin:
        return ''
    sgid = skin['ship_group']
    stid = skin['shop_type_id']
    if not stid:
        return skin['name']
    for skid in book['skin'][lang]:
        skin2 = book['skin'][lang][skid]
        if skin2['ship_group'] == sgid and skin2['group_index'] == 0:
            skname = skin2['name'].strip()
            shtype = shop_type[stid]
            if skname in shop_type_fixer:
                if shtype in shop_type_fixer[skname]:
                    shtype = shop_type_fixer[skname][shtype]
            return '{}/{}'.format(skname, shtype)

def parse_scripts(scripts, lang):
    lines = []
    bgrn = None
    bgmrn = None
    nobgname = set()
    for script in scripts:
        if isinstance(script, str):
            print('Not a script:', script)
            continue
        skinid = script.get('actor')
        skinnameEN = getwikiname(skinid, 'EN')
        skinname = getwikiname(skinid, lang)
        actorname = script.get('actorName', '').strip()
        if not actorname and skinnameEN != skinname:
            actorname = skinname.split('/')[0]
        actortext = script.get('say', '').strip()
        if tb:
            skinnameEN = skinnameEN.replace('/OTHER', '')
            skinname = skinname.replace('/OTHER', '')
            actortext = re.sub('\{tb\}|\$\d+', '<{}>'.format(commander[lang]), actortext)
        actorname = re.sub('\{playername\}', commander[lang], actorname)
        actortext = re.sub('\{playername\}', commander[lang], actortext)

        subactors = []
        if 'subActors' in script: # todo: include subactors in output file
            for subactor in script['subActors']:
                if 'actor' in subactor:
                    subskinid = subactor['actor']
                    subskinnameEN = getwikiname(subskinid, 'EN')
                    subskinname = getwikiname(subskinid, lang)
                    print('SUBACTORS:', subskinnameEN, subskinname)
                    subactors.append(subskinnameEN)

        actorname = re.sub('[.·]?改', '', actorname) # kai

        br = []
        if 'bgName' in script and script['bgName'] != bgrn:
            bgrn = script['bgName']
            if bgrn.startswith('star_level_bg_'):
                filename = 'Skin BG {}.png'.format(bgrn[14:])
            else:
                bgmatch = re.match('^bg_(.+?)(?:_(bg|cg|n|room)?(\d+))?$', bgrn)
                if bgmatch:
                    bggroups = bgmatch.groups()
                    bgcode = bggroups[0].strip()
                    if bgcode in bgnames:
                        bgtitle = bgnames[bgcode]
                        if bggroups[2]:
                            bgcg = {'cg': 'CG', 'n': 'Background Part', 'room': 'Room Background'}.get(bggroups[1], 'Background')
                            bgn = bggroups[2]
                            if bgcode in ['bsm', 'bsmre'] and bgcg == 'Background':
                                bgn = int(bgn) + 1
                            filename = 'Memory {} {} {}.png'.format(bgtitle, bgcg, bgn)
                        else:
                            filename = 'Memory {} Background.png'.format(bgtitle)
                    else:
                        filename = bgrn
                        nobgname.add(bgrn)
                else:
                    filename = bgrn + 'HMMMM'
                    nobgname.add(bgrn)
            if bgrn not in ignoredbgnames:
                br.append('[[File:{}|300px]]'.format(filename))
        if 'bgm' in script and script['bgm'] != bgmrn:
            bgmrn = script['bgm']
            br.append('bgm: {}'.format(bgmrn))
        if len(br) > 0:
            lines.append('| [] ' + '<br>'.join(br))

        if 'optionFlag' in script:
            actortext = 'Option {}<br>{}'.format(script['optionFlag'], actortext)

        for nc in book['code'][lang]:
            skinnameEN = re.sub('{{namecode:{}(:.+?)?}}'.format(nc), book['code']['EN'][nc]['name'], skinnameEN)
            skinname = re.sub('{{namecode:{}(:.+?)?}}'.format(nc), book['code'][lang][nc]['name'], skinname)
            actorname = re.sub('{{namecode:{}(:.+?)?}}'.format(nc), book['code'][lang][nc]['name'], actorname)
            actortext = re.sub('{{namecode:{}(:.+?)?}}'.format(nc), book['code'][lang][nc]['name'], actortext)
            for subactor in subactors:
                subactor = re.sub('{{namecode:{}(:.+?)?}}'.format(nc), book['code'][lang][nc]['name'], subactor)

        if skinnameEN in bannedbanners:
            skinname = None
        paintingname = book['skin'][lang].get(str(skinid), {}).get('painting', '')

        # name quickfixes
        if skinnameEN == 'Bon Homme Richard':
            if not actorname:
                actorname = skinnameEN
            skinnameEN = 'Bon Homme Richard META'
        if 'gaoxiong_dark' in paintingname:
            skinnameEN = 'Takao META'
        if 'qiye_dark' in paintingname:
            skinnameEN = 'Enterprise META'
        skinnameEN = skinnameEN.replace(':', '').strip() # for arbiters
        actorname = actorname.replace(':', '').strip() # for arbiters
        actortext = actortext.replace('=', '&#61;') # prevent named parameters

        if skinname and not paintingname.endswith('_hei'):
            if skinnameEN and actorname and skinnameEN.split('/')[0] != actorname:
                lines.append('| [S:{}:{}]'.format(skinnameEN, actorname))
            else:
                lines.append('| [S:{}]'.format(skinnameEN))
            for subactor in subactors:
                lines[-1] += '[S:{}]'.format(subactor)
            lines[-1] += ' {}'.format(actortext)
        elif actorname:
            lines.append('| [O:{}] {}'.format(actorname, actortext))
        elif actortext:
            lines.append('| [] {}'.format(actortext))
        
        if 'options' in script:
            for option in script['options']:
                optcon = option['content']
                for nc in book['code'][lang]:
                    optcon = re.sub('{{namecode:{}(:.+?)?}}'.format(nc), book['code'][lang][nc]['name'], optcon)
                lines.append('| [{}] \'\'\'Option {}\'\'\'<br>{}'.format('O:Commander' if tb else '', option['flag'], optcon)) # usually Commander

        if 'sequence' in script:
            seqlist = []
            for seq in script['sequence']:
                seqlist.append(re.sub('<.+?>', '', seq[0]).replace('\n', '<br>'))
            seqlistall = '<br>'.join(seqlist).strip()
            if seqlistall:
                lines.append('| [] {}'.format(seqlistall))
    return lines, nobgname

def build_memory(gid):
    bgs = set()
    lines = ['<tabber>']
    for lang in langs:
        if str(gid) not in book['group'][lang]:
            print('WARNING: Story', gid, 'is not available in', lang, '.')
            continue
        group = book['group'][lang][str(gid)]
        lines += [
            '{} Story='.format(langs[lang]),
            '=== {} ==='.format(group['title'].strip()),
            '{{#tag:tabber|'
        ]
        for i, mid in enumerate(group['memories']):
            memory = book['memory'][lang][str(mid)]
            lines += [
                'Chapter {}='.format(i + 1),
                '{{Story',
                '| Title = {}'.format(memory['title'].strip()),
                '| Unlock = {}'.format(memory['condition'].strip()),
                '| Language = {}'.format(lang)
            ]
            sid = memory['story']
            if sid.lower() in book['story'][lang]:
                story = book['story'][lang][sid.lower()]
            else: # battle sim
                story = {'scripts': []}
                battle = book['battle'][lang][sid.lower()]
                triggers = []
                for stage in battle['stages']:
                    for wave in stage['waves']:
                        if wave['triggerType'] == 3:
                            triggers.append(wave['triggerParams']['id'])
                for trigger in triggers:
                    story['scripts'] = story['scripts'] + book['story'][lang][trigger.lower()]['scripts']

            if 'scripts' in story:
                scriptlines, nobgname = parse_scripts(story['scripts'], lang)
                lines += scriptlines
                bgs = bgs.union(nobgname)
            lines += ['}}', '{{!}}-{{!}}']
        lines.pop()
        lines += ['}}', '|-|']
    lines.pop()

    groupEN = book['group']['EN'][str(gid)]

    lines += [
        '</tabber>',
        '<noinclude>',
        '{{MemoryNavbox}}',
        '</noinclude>',
        '[[Category:{} Memories|{}]]'.format(
            memory_type[groupEN['type']][groupEN['subtype']],
            groupEN['title']
        )
    ]
    print('UNKNOWN BGS:', bgs)
    return '\n'.join(lines) + '\n'

# find stories with certain sprite ids
def get_groupids_by_painting(name):
    '''Find stories that include the specified shipgirl by name, skin name, or skin id.'''
    for skid in book['skin']['EN']:
        skin = book['skin']['EN'][skid]
        if name.lower() in skin.get('name').lower() or name.lower() in skin.get('painting').lower():
            # skid = skin['ship_group'] # should be the same already
            print('{} ({})'.format(skin.get('name'), skin.get('painting')))
            
            stids = []
            for stid in book['story']['EN']:
                story = book['story']['EN'][stid]
                if skid in str(story): # hacky search
                    stids.append(story['id']) # capitalization difference between stid and story['id']
            mids = []
            for mid in book['memory']['EN']:
                memory = book['memory']['EN'][mid]
                if memory.get('story') in stids:
                    mids.append(memory['id']) # mid is str, memory['id'] is int
            titles = set()
            for gid in book['group']['EN']:
                group = book['group']['EN'][gid]
                for gmid in group.get('memories', []):
                    if gmid in mids:
                        titles.add(group['title'])
            for title in titles:
                print('-', title)

# manually built lists

commander = {
    'EN': 'Commander',
    'CN': '指挥官',
    'JP': '指揮官'
}

memory_type = {
    1: {0: 'Campaign'},
    2: {
        1: 'Event',
        2: 'Special',
        3: 'Permanent'
    },
    3: {0: 'Character'}
}

# from skin_page_template.json
shop_type = { # todo: use buildskinname.py instead
    # 0: 'Original', # on wiki, this is alpha art
    1: 'Christmas',
    2: 'New Year',
    3: 'Spring',
    4: 'School',
    6: 'Summer',
    7: 'Party',
    8: 'Halloween',
    9: 'Casual',
    10: 'Festival',
    11: 'Idol',
    12: 'Special Exercise',
    13: 'Sport',
    14: 'RaceQueen',
    15: 'Hospital',
    16: 'Bunny',
    17: 'Maid',
    18: 'Vampire',
    19: 'Fairy Tale',
    20: 'Home Relaxation',
    21: 'Dance',
    22: 'Hot Springs',
    23: 'Work',
    24: 'RPG',
    25: 'Wild West',
    26: 'Theme Park',
    9997: 'Kai',
    9998: 'Wedding',
    9999: '_OTHER_9999', # other
}

shop_type_fixer = { # todo: find mislabeled shop_type instances
    'Ayanami': {
        'Casual': 'RaceQueen'
    },
    'Prototype Bulin MKII': {
        'OTHER': 'Event'
    }
}

bgnames = {
    'bg_bigbuli': 'The Golden Doubulin',
    # Parallel Superimposition
    'aircraft_future': 'Aircraft Future',
    'aostelab': 'Aoste Lab',
    'camelot': 'Pledge of the Radiant Court',
    'cccpv2': 'Khorovod of Dawn\'s Rime',
    'endingsong': 'Rondo at Rainbow\'s End',
    'highschool_future': 'Highschool Future',
    'port_chongdong': 'Situational Port',
    'port_ny_future': 'New York Port Future',
    'qiongding': 'Skybound Oratorio',
    'roma': 'Aquilifer\'s Ballade',
    'starsea_core': 'Causality Transposition',
    'story': 'Story',
    'story_task': 'Task',
    'story_tower': 'Virtual Tower',
    'wuzang': 'Violet Tempest, Blooming Lycoris',
    'xiangting': 'Ashen Simulacrum',
    'zhedie': 'Parallel Superimposition',
    # Snowrealm Peregrination
    'deepecho': 'Abyssal Refrain',
    'guild_blue': 'Guild Blue',
    'guild_red_n': 'Guild Red Background Part 2',
    'xuejing': 'Snowrealm Peregrination',
    # Zero to Hero
    'mmorpg': 'From Zero to Hero',
    'story_chuansong': 'Fantastical Encounter',
    'story_school': 'School',
    'unnamearea': 'Unnamed Area',
    # Confluence of Nothingness
    'bsm': 'Scherzo of Iron and Blood',
    'bsmre': 'Confluence of Nothingness',
    'xinnong2': 'Dreamwaker\'s Butterfly',
    'fuxiangxian': 'Inverted Orthant',
    'story_tiancheng': 'Crimson Echoes',
    'battle_night': 'Night Battle',
    'underwater': 'Underwater',
    'story_italy': 'Italy',
    # Pledge of the Radiant Court
    'midgard': 'Tower of Transcendence',
    # Reflections of the Oasis
    'alexandria': 'Reflections of the Oasis',
    # Windborne / Wild West
    'tieyiqingfeng': 'Windborne Steel Wings',
    'westdaily': 'Wild West Vacation Log',
    'renaya': 'The Flame-Touched Dagger',
    'banama': 'Microlayer Medley',
    # 'moran': 'Tranquil Sea, Distant Thunder', # unsure if this event is the first appearance; also weird that only _3 is used
    'luoxuan': 'Mirror Involution',
    'story_nagato': 'Ink-Stained Steel Sakura',
    'firedust': 'Revelations of Dust',
    'map_tiancheng': 'Crimson Echoes Map',
    'yunxian': 'Effulgence Before Eclipse',
    'story_outdoor': 'Outdoors',
    'bianzhihua': 'Whence Flowers Bear No Fruit',
    # Convergence of Hearts
    'project_tb': 'Project Identity TB',
    '': '',
}

ignoredbgnames = [
    'bg_unnamearea_0', # sakura islands map
    'bg_zhuiluo_2', # big lava 'x' island map
    'blackbg',
    'star_level_bg_1100',
    'star_level_bg_1104', # white screen???
    # strategy map plans with markers and stuff
    'storymap_taipingyang',
    'storymap_taipingyang_99',
    'storymap_maliyana',
    'storymap_maliyana_99',
    'bg_moran_3' # dead sakura tree
]

bannedbanners = [
    # 'Dr. Anzeel',
    # 'Dr. Aoste',
    # 'Bon Homme Richard',
    # 'Jintsuu META',
    # 'Yorktown META',
    # 'Arbiter The Devil XV',
    # 'Arbiter The Tower XVI',
]

if 0: # testing
    # gid = get_groupid('Causality')
    # gid = get_groupid('Superimposition')
    # gid = get_groupid('Peregrination')
    gid = get_groupid('Zero')
    mid = build_memory(gid)
    with open('output/story.txt', 'w', encoding='utf-8') as fp:
        fp.write(mid)

    # get_groupids_by_painting('anzeel') # anjie
    # get_groupids_by_painting('aoste') # aosita
    # get_groupids_by_painting('silver fox') # silverfox
    get_groupids_by_painting('colette') # kelei

    def findeq(key, pattern): # check stories for `=` (named parameter bug)
        checked = [
            'Veiled in White',
            'A Bump in the Rainy Night',
            'Confluence of Nothingness',
            'Prologue',
        ]
        checked404 = [
            'KONGXIANGJIAOHUIDIAN31-3',
            'WORLD508C',
            'WORLD508E',
            'WORLD508G',
        ]

        def getmemory(id, lang, z):
            for mid in book['memory'][lang]:
                memory = book['memory'][lang][mid]
                if memory['story'] == id:
                    for gid in book['group'][lang]:
                        group = book['group'][lang][gid]
                        if memory['id'] in group['memories']:
                            titleEN = book['group']['EN'][gid]['title']
                            print('\t' if titleEN in checked else '', z, lang, titleEN, group['id'], id, say, sep=' | ')
                            return True
            return False

        x = 0
        for lang in langs:
            for sid in book['story'][lang]:
                story = book['story'][lang][sid]
                for script in story.get('scripts', {}):
                    if key in script:
                        say = str(script[key])
                        if re.findall(pattern, say):
                            x += 1
                            if getmemory(story['id'], lang, 'A'):
                                continue
                            breakout = False
                            for bid in book['battle'][lang]:
                                battle = book['battle'][lang][bid]
                                for stage in battle['stages']:
                                    for wave in stage['waves']:
                                        if wave['triggerType'] == 3:
                                            if wave['triggerParams']['id'] == story['id']:
                                                if getmemory(str(battle['id']), lang, 'B'):
                                                    breakout = True
                                                    break
                                        if 'spawn' in wave:
                                            for spawn in wave['spawn']:
                                                if 'phase' in spawn:
                                                    for phase in spawn['phase']:
                                                        if 'story' in phase:
                                                            if phase['story'] == story['id']:
                                                                if getmemory(str(battle['id']), lang, 'C'):
                                                                    breakout = True
                                                                    break
                                        if breakout:
                                            break
                                    if breakout:
                                        break
                                if breakout:
                                    break
                            if breakout:
                                continue
                            print('\t' if story['id'] in checked404 else '', '-', lang, 'NOT FOUND', story['id'], say, sep=' | ')
        print(x)
    findeq('say', '^[^<]*=') # =
    findeq('bgName', 'hongran') # Tranquil Sea, Distant Thunder
    findeq('actor', '900355') # hermit meta
    # findeq('actorName', 'Omitter')

    get_groupids_by_painting('Omitter')
    get_groupids_by_painting('Compiler')
    get_groupids_by_painting('Observer')
    get_groupids_by_painting('Purifier')
    # get_groupids_by_painting('Tester')
    get_groupids_by_painting('unknown1') # Tester

    get_groupids_by_painting('Empress')
    get_groupids_by_painting('Temperance')
    get_groupids_by_painting('Strength')
    get_groupids_by_painting('Hierophant')
    get_groupids_by_painting('Hermit')

    get_groupids_by_painting('TB')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    parser.add_argument('-t', '--title', default='', help='build story by title')
    parser.add_argument('-p', '--painting', default='', help='get story ids by sprite name')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_story
        dl_story()
    init_book()
    if args.title:
        gid = get_groupid(args.title)
        mid = build_memory(gid)
        with open('output/story.txt', 'w', encoding='utf-8') as fp:
            fp.write(mid)
        print('https://azurlane.koumakan.jp/wiki/Memories/{}?action=raw'.format(quote(book['group']['EN'][gid]['title'])))
    if args.painting:
        get_groupids_by_painting(args.painting)
