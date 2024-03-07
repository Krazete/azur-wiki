import json
from argparse import ArgumentParser

story = {}

def init_story():
    '''Initializes `child` object with JSON files downloaded from AzurLaneData repo.'''
    subpaths = {
        'ShareCfg/memory_group': 'group',
        'ShareCfg/memory_template': 'memory',
        'GameCfg/story': 'line'
    }
    for lang in ['CN', 'EN', 'JP']:
        for subpath in subpaths:
            cat = subpaths[subpath]
            path = '{}/{}.json'.format(lang, subpath)
            with open(path, 'r', encoding='utf-8') as fp:
                story.setdefault(cat, {})
                story[cat][lang] = json.load(fp)

# find a story by title
for gid in story['group']['EN']:
    if 'Parallel Superimposition' in story['group']['EN'][gid]['title']:
        print(gid)
        break

# parse story
for mid in story['group']['EN'][gid]['memories']:
    memory = story['memory']['EN'][str(mid)]
    icon = memory['icon']
    sid = memory['story'].lower()
    line = story['line']['EN'][sid]
    for script in line['scripts']:
        print(script.get('actor', 'NOACTOR'), script.get('actorName', 'NONAME'))
        print('\t', script.get('say', 'NOSCRIPT'))
        # also: 'options'

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_story
        dl_story()
    init_story()
