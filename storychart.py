import os
import re
import json
from argparse import ArgumentParser

langs = {
    'EN': 'English',
    'CN': 'Chinese',
    'JP': 'Japanese'
}
book = {}
namecode = {}

def init_namecode():
    '''Initializes namecode dictionary or loads it from file if up to date.'''
    global namecode
    if os.path.exists('versionlog.json'):
        with open('versionlog.json', 'r') as fp:
            versionlog = json.load(fp)
    else:
        raise Exception('No versionlog found.')
    uptodate = 'namecode' in versionlog and 'story' in versionlog and versionlog['namecode'] == versionlog['story']
    if uptodate and os.path.exists('input/namecode.json'):
        with open('input/namecode.json', 'r', encoding='utf-8') as fp:
            namecode = json.load(fp)
    else:
        matches = re.findall('{namecode:(\d+):(.+?)}', str(book)) # hacky search
        for match in matches:
            if match[0] in namecode:
                assert namecode[match[0]] == match[1], 'MISMATCH: namecode {} = {} & {}'.format(match[0], namecode[match[0]], match[1])
            namecode[match[0]] = match[1]
        with open('input/namecode.json', 'w', encoding='utf-8') as fp:
            json.dump(namecode, fp)
        versionlog['namecode'] = versionlog['story']
        with open('versionlog.json', 'w', encoding='utf-8') as fp:
            json.dump(versionlog, fp)

def init_book():
    '''Initializes `child` object with JSON files downloaded from AzurLaneData repo.'''
    subpaths = {
        'ShareCfg/memory_group': 'group',
        'ShareCfg/memory_template': 'memory',
        'ShareCfg/ship_skin_template': 'skin',
        'GameCfg/story': 'story'
    }
    for lang in langs:
        for subpath in subpaths:
            cat = subpaths[subpath]
            path = '{}/{}.json'.format(lang, subpath)
            with open(path, 'r', encoding='utf-8') as fp:
                book.setdefault(cat, {})
                book[cat][lang] = json.load(fp)

def get_groupid(title):
    '''Get memory group id by title or title fragment.'''
    for gid in book['group']['EN']:
        if title in book['group']['EN'][gid]['title']:
            return gid

def parse_scripts(scripts, lang):
    lines = []
    bgrn = None
    bgmrn = None
    nobgname = set()
    for script in scripts:
        skinid = script.get('actor')
        skinnameEN = book['skin']['EN'].get(str(skinid), {}).get('name', '').replace(' (Retrofit)', '/Kai').strip()
        skinname = book['skin'][lang].get(str(skinid), {}).get('name', '').replace(' (Retrofit)', '/Kai').strip()
        actorname = script.get('actorName', skinname).replace(' (Retrofit)', '/Kai').strip()
        actortext = script.get('say', '').strip()

        if 'subActors' in script: # todo: include subactors in output file
            for subactor in script['subActors']:
                subskinid = subactor['actor']
                subskinnameEN = book['skin']['EN'].get(str(subskinid), {}).get('name', '').replace(' (Retrofit)', '/Kai').strip()
                subskinname = book['skin'][lang].get(str(subskinid), {}).get('name', '').replace(' (Retrofit)', '/Kai').strip()
                print('SUBACTORS:', subskinnameEN, subskinname)

        actorname = re.sub('[.·]?改', '', actorname) # kai

        br = []
        if 'bgName' in script and script['bgName'] != bgrn:
            bgrn = script['bgName']
            if bgrn.startswith('star_level_bg_'):
                filename = 'Skin BG {}.png'.format(bgrn[14:])
            else:
                bgmatch = re.match('^bg_(.+?)(?:_(bg|cg|n)?(\d+))?$', bgrn)
                if bgmatch:
                    bggroups = bgmatch.groups()
                    if bggroups[0] in bgnames:
                        bgtitle = bgnames[bggroups[0]]
                        if bggroups[2]:
                            bgcg = {'cg': 'CG', 'n': 'Background Part'}.get(bggroups[1], 'Background')
                            filename = 'Memory {} {} {}.png'.format(bgtitle, bgcg, bggroups[2])
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
            lines.append(' | [] ' + '<br>'.join(br))

        if 'optionFlag' in script:
            actortext = 'Option {}<br>{}'.format(script['optionFlag'], actortext)

        for nc in namecode:
            actorname = re.sub('{{namecode:{}(:.+?)?}}'.format(nc), namecode[nc], actorname)
            actortext = re.sub('{{namecode:{}(:.+?)?}}'.format(nc), namecode[nc], actortext)

        if skinnameEN in bannedbanners:
            skinname = None
        paintingname = book['skin'][lang].get(str(skinid), {}).get('painting', '')
        if skinname and not paintingname.endswith('_hei'):
            if skinnameEN == actorname:
                lines.append(' | [S:{}] {}'.format(actorname, actortext))
            else:
                lines.append(' | [S:{}:{}] {}'.format(skinnameEN, actorname, actortext))
        elif actorname:
            lines.append(' | [O:{}] {}'.format(actorname, actortext))
        elif actortext:
            lines.append(' | [] {}'.format(actortext))
        
        if 'options' in script:
            for option in script['options']:
                optcon = option['content']
                for nc in namecode:
                    optcon = re.sub('{{namecode:{}(:.+?)?}}'.format(nc), namecode[nc], optcon)
                lines.append(' | [O:Commander] \'\'\'Option {}\'\'\'<br>{}'.format(option['flag'], optcon))

        if 'sequence' in script:
            seqlist = []
            for seq in script['sequence']:
                seqlist.append(re.sub('<.+?>', '', seq[0]).replace('\n', '<br>'))
            seqlistall = '<br>'.join(seqlist).strip()
            if seqlistall:
                lines.append(' | [] {}'.format(seqlistall))
    return lines, nobgname

def build_memory(gid):
    bgs = set()
    lines = ['<tabber>']
    for lang in langs:
        group = book['group'][lang][str(gid)]
        lines += [
            '{} Story='.format(langs[lang]),
            '=== {} ==='.format(group['title']),
            '{{#tag:tabber|'
        ]
        for i, mid in enumerate(group['memories']):
            memory = book['memory'][lang][str(mid)]
            lines += [
                'Chapter {}='.format(i + 1),
                '{{Story',
                ' | Title = {}'.format(memory['title']),
                ' | Unlock = {}'.format(memory['condition']),
                ' | Language = {}'.format(lang)
            ]
            sid = memory['story']
            story = book['story'][lang].get(sid.lower())

            # print('STORY:', sid)
            if story == None: # todo: figure out how to identify split stories (37-1, 37-2, 37-3) (b/c battle sims)
                print('NO STORY:', sid)
                continue

            scriptlines, nobgname = parse_scripts(story['scripts'], lang)
            lines += scriptlines
            bgs = bgs.union(nobgname)
            lines += ['}}', '{{!}}-{{!}}']
        lines.pop()
        lines += ['}}', '|-|']
    lines.pop()
    lines += [
        '</tabber>',
        '<noinclude>',
        '{{MemoryNavbox}}',
        '</noinclude>',
        '[[Category:Event Memories|{}]]'.format(book['group']['EN'][str(gid)]['title'])
    ]
    print('UNKNOWN BGS:', bgs)
    return '\n'.join(lines) + '\n'

# find stories with certain sprite ids
def get_groupids_by_painting(name):
    for skid in book['skin']['EN']:
        skin = book['skin']['EN'][skid]
        if name in skin.get('name'):
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

bgnames = {
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
    'xuejing': 'Snowrealm Peregrination'
}

ignoredbgnames = [
    'bg_unnamearea_0', # sakura islands map
    'bg_zhuiluo_2', # big lava 'x' island map
    'star_level_bg_1100',
    'star_level_bg_1104', # white screen???
]

bannedbanners = [
    # 'Dr. Anzeel',
    # 'Dr. Aoste',
    'Bon Homme Richard',
    # 'Jintsuu META',
    'Yorktown META',
    'Arbiter: The Devil XV'
]

if 0: # testing
    gid = get_groupid('Causality')
    # gid = get_groupid('Superimposition')
    # gid = get_groupid('Peregrination')
    mid = build_memory(gid)
    with open('output/story.txt', 'w', encoding='utf-8') as fp:
        fp.write(mid)

    get_groupid_by_painting('anjie') # anzeel
    # get_groupid_by_painting('aosita') # aoste
    # get_groupid_by_painting('silverfox') # silver fox
    # get_groupid_by_painting('anjie_hei') # anzeel shadow
    # get_groupid_by_painting('aosita_hei') # aoste shadow
    # get_groupid_by_painting('silverfox_shadow') # silver fox shadow

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
        init_namecode()
        gid = get_groupid(args.title)
        mid = build_memory(gid)
        with open('output/story.txt', 'w', encoding='utf-8') as fp:
            fp.write(mid)
        print('https://azurlane.koumakan.jp/w/index.php?title=Memories/{}&action=raw'.format(book['group']['EN'][gid]['title'].replace(' ', '_')))
    if args.painting:
        get_groupids_by_painting(args.painting)
