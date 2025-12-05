import re
import json
from argparse import ArgumentParser

langs = ['EN', 'CN', 'JP']
suffixes = ['group', 'template']

data = {}
hall = {}

def init_data():
    for lang in langs:
        data.setdefault(lang, {})
        for suffix in suffixes:
            with open('{}/ShareCfg/memory_{}.json'.format(lang, suffix), 'r', encoding='utf-8') as fp:
                data[lang].setdefault(suffix, json.load(fp))

    with open('output/skinname.json', 'r', encoding='utf-8') as fp:
        data['ships'] = json.load(fp)

def build_halloffame():
    for lang in langs:
        for gid in data[lang]['group']:
            group = data[lang]['group'][gid]
            if group['icon'] == 'title_chara_rongyaodiantang':
                break
        for tid in group['memories']:
            template = data[lang]['template'][str(tid)]
            shipid = re.sub(r'^memory_renqi', '', template['icon'])

            ship = data['ships'][shipid].strip()
            title = template['title'].strip()
            hall.setdefault(ship, {'langs': []})
            hall[ship]['langs'].append(lang)
            hall[ship].setdefault('title', title)

def build_page():
    keys = sorted(hall.keys(), key=lambda ship: -(100 if 'EN' in hall[ship]['langs'] else len(hall[ship]['langs']))) # by en order first; by numbers of langs second

    lines = []
    for ship in keys:
        title = hall[ship]['title']
        langs = hall[ship]['langs']
        if 'EN' in langs:
            pass
        # elif 'EN' in langs and 'CN' in langs and 'JP' in langs:
        #     title = '<span style="text-decoration:orange underline;">{}</span>'.format(title)
        # elif 'EN' in langs and 'CN' in langs:
        #     title = '<span style="text-decoration:purple underline;">{}</span>'.format(title)
        # elif 'EN' in langs and 'JP' in langs:
        #     title = '<span style="text-decoration:red underline;">{}</span>'.format(title)
        elif 'CN' in langs and 'JP' in langs:
            title = '<span style="color:orange;">{}</span>'.format(title)
        elif 'CN' in langs:
            title = '<span style="color:purple;">{}</span>'.format(title)
        elif 'JP' in langs:
            title = '<span style="color:red;">{}</span>'.format(title)

        if 'EN' in langs:
            title = '[[Memories/Hall of Fame#tabber-{}|{}]]'.format(ship, title)

        lines.append('Image:{0}HallofFame.png|link=Memories/Hall of Fame#tabber-{0}|\'\'{1}\'\'{2}'.format(
            ship,
            title,
            '' # '<br>' + ' / '.join(langs)
        ))

    with open('output/halloffame.wiki', 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(lines))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        import buildskinname
        from downloader import update
        update(langs, ['ShareCfg/memory_{}'.format(suffix) for suffix in suffixes])
        buildskinname.main()
    init_data()
    build_halloffame()
    build_page()
