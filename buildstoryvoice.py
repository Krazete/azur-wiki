import re
import json
from argparse import ArgumentParser

story = {}

def init_story():
    '''Initializes `story` object.'''
    global story
    with open('EN/GameCfg/story.json', 'r', encoding='utf-8') as fp:
        story = json.load(fp)

def build_voices():
    '''Build a wikitable from AzurLaneData files and current wiki page info.'''
    voice = {}
    for key in story:
        for line in story[key].get('scripts', []):
            audio = 'voice' # or 'soundeffect'
            if audio in line:
                b = re.sub('(\D)(\d)(\D)', '\g<1> \g<2>\g<3>', line[audio])
                b = re.sub('(\D)(\d)$', '\g<1> \g<2>', b)
                voice.setdefault(b, set())
                voice[b].add(line.get('say', ''))
    unique = {}
    general = {}
    for b in voice:
        if len(voice[b]) == 1:
            unique[b] = voice[b].pop()
        else:
            general[b] = list(voice[b])
    with open('output/voice_unique.json', 'w', encoding='utf-8') as fp:
        json.dump(unique, fp, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True)
    with open('output/voice_general.json', 'w', encoding='utf-8') as fp:
        json.dump(general, fp, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True)

    combined = unique
    for b in general:
        combined[b] = '<br>'.join(general[b])
    with open('output/voice.json', 'w', encoding='utf-8') as fp:
        json.dump(combined, fp, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_story
        dl_story()
    init_story()
    build_voices()
