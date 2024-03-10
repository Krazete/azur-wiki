import re
import json
from argparse import ArgumentParser

langs = {
    'EN': 'English',
    'CN': 'Chinese',
    'JP': 'Japanese'
}
book = {}

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

# find a book by title
for gid in book['group']['EN']:
    if 'Parallel Superimposition' in book['group']['EN'][gid]['title']:
        print(gid)
        break

# parse book
for mid in book['group']['EN'][gid]['memories']:
    memory = book['memory']['EN'][str(mid)]
    icon = memory['icon']
    sid = memory['story'].lower()
    line = book['story']['EN'][sid]
    for script in line['scripts']:
        skinid = str(script.get('actor'))
        skinname = book['skin']['EN'].get(skinid, {}).get('name')
        actorname = script.get('actorName', skinname)
        actortext = script.get('say')
        if skinname:
            ppp = '[S:{}:{}]'.format(skinname, actorname)
        else:
            ppp = '[O:{}]'.format(actorname)
        print(skinname, actorname)
        print('\t', actortext)
        # also: 'options'
    break

# group
#   memory
#     skin
#     line

bgnames = {
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
    'zhedie': 'Parallel Superimposition'
}

def parse_scripts(scripts, lang):
    lines = []
    bgrn = None
    abcdefg = set()
    for script in scripts:
        skinid = script.get('actor')
        skinnameEN = book['skin']['EN'].get(str(skinid), {}).get('name', '').strip()
        skinname = book['skin'][lang].get(str(skinid), {}).get('name', '').strip()
        actorname = script.get('actorName', skinname).strip()
        actortext = script.get('say', '').strip()

        br = []
        if 'bgName' in script and script['bgName'] != bgrn:
            bgrn = script['bgName']
            if bgrn.startswith('star_level_bg_'):
                filename = 'Skin BG {}.png'.format(bgrn[14:])
            else:
                bgmatch = re.match('^bg_(.+?)(?:_(?:bg)?(\d+))?$', bgrn)
                if bgmatch:
                    bggroups = bgmatch.groups()
                    if bggroups[0] in bgnames:
                        bgtitle = bgnames[bggroups[0]]
                        if bggroups[1]:
                            filename = 'Memory {} Background {}.png'.format(bgtitle, bggroups[1])
                        else:
                            filename = 'Memory {} Background.png'.format(bgtitle)
                    else:
                        filename = bgrn
                        abcdefg.add(bgrn)
                else:
                    filename = bgrn + 'HMMMM'
                    abcdefg.add(bgrn)
            if bgrn != 'star_level_bg_1104': # pure white
                br.append('[[File:{}|300px]]'.format(filename))
        if 'bgm' in script:
            br.append('bgm: {}'.format(script['bgm']))
        if len(br) > 0:
            lines.append(' | [] ' + '<br>'.join(br))

        if skinnameEN in ['Dr. Anzeel', 'Dr. Aoste', 'Bon Homme Richard']:
            skinname = None
        if skinname:
            if skinnameEN == actorname:
                lines.append(' | [S:{}] {}'.format(actorname, actortext))
            else:
                lines.append(' | [S:{}:{}] {}'.format(skinnameEN, actorname, actortext))
        elif actorname:
            lines.append(' | [O:{}] {}'.format(actorname, actortext))
        elif actortext:
            lines.append(' | [] {}'.format(actortext))
    return lines, abcdefg

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
            story = book['story'][lang][sid.lower()]
            scriptlines, abdefg = parse_scripts(story['scripts'], lang)
            lines += scriptlines
            bgs = bgs.union(abdefg)
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
    print(bgs)
    return '\n'.join(lines) + '\n'

# init_book()
abc = build_memory(235)
with open('output/story.txt', 'w', encoding='utf-8') as fp:
    fp.write(abc)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_story
        dl_story()
    init_book()
