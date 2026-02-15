import re
import json
from argparse import ArgumentParser

data = {}
hall = {}

def init_data():
    with open('EN/ShareCfg/activity_medal_group.json', 'r', encoding='utf-8') as fp:
        global data
        data = json.load(fp)

fix_event = {
    '星光下的余晖（占坑配置）': 'Substellar Crepuscule',
    'Villa Resort': 'Midsummer Returns! The Villa Reconstruction',
}
fix_page = {
    'Midsummer Returns! The Villa Reconstruction': 'A Rose on the High Tower',
}
fix_section = {
    'Substellar Crepuscule': 'One-Time Missions',
    'Paradiso of Shackled Light': 'One-Time Missions',
    'Letters from Valley Hospital': 'One-Time Missions',
    'Toward Tulipa\'s Seas': 'One-Time Missions',
    'A Rose on the High Tower': 'One-Time Missions',
    'Tempesta and Islas de Libertád': 'Commemorative Album Missions',
}

def build_page():
    lines = [
        '== Commemorative Album ==',
        '* During an ongoing event, you can complete event missions to receive \'\'\'commemorative stickers\'\'\'. Finishing your collection will award you with a \'\'\'[[Medallion#Limited|medal]]\'\'\' and sometimes a \'\'\'[[Decorations#Event_Medals|limited furniture piece]]\'\'\'.',
        '**\'\'While the event is available, tapping the \'\'\'Commemorative button on the event banner\'\'\' or the \'\'\'Commemorative Album tab under Memories\'\'\' will bring you to the commemorative stickers menu.\'\'',
        '**\'\'Following the end of the event, you can only access the stickers menu from the Commemorative Album tab under Memories.\'\'',
        '**\'\'Rewards may be claimed for a period even after the event ends.\'\'',
        '<gallery mode="packed" heights="100px" style="margin:1em 0em;">'
    ]

    for aid in data:
        if aid == 'all':
            continue

        event = data[aid]['group_name']
        if event in fix_event:
            event = fix_event[event]

        image = re.sub(r'[\\/:*?"<>|]', '', event)

        page = event
        if event in fix_page:
            page = fix_page[event]

        section = 'Commemorative Missions'
        if event in fix_section:
            section = fix_section[event]

        lines.append('Image:Album {0}.png|link={1}#{2}|\'\'[[{1}#{2}|{3}]]\'\''.format(
            image,
            page,
            section,
            event
        ))

    lines += [
        '</gallery>',
        '',
        '[[Category:Memories|*]]'
    ]

    with open('output/album.wiki', 'w', encoding='utf-8') as fp:
        fp.write('\n'.join(lines))

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import update
        update(['EN'], ['ShareCfg/activity_medal_group'])
    init_data()
    build_page()
