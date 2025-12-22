import os
import re
import json
from argparse import ArgumentParser

story = {}

def init_story():
    '''Initializes `story` object.'''
    for lang in ['EN', 'CN', 'JP']:
        with open('{}/GameCfg/story{}.json'.format(lang, 'jp' if lang == 'JP' else ''), 'r', encoding='utf-8') as fp:
            story[lang] = json.load(fp)

def build_voices(lang, format_numbers):
    '''Build a wikitable from AzurLaneData files and current wiki page info.'''
    voice = {}
    for key in story[lang]:
        if isinstance(story[lang][key], list):
            print('Skipping:', key)
            continue
        for line in story[lang][key].get('scripts', []):
            audio = 'voice' # or 'soundeffect'
            if audio in line:
                if format_numbers:
                    b = re.sub('(\D)(\d)(\D)', '\g<1> \g<2>\g<3>', line[audio])
                    b = re.sub('(\D)(\d)$', '\g<1> \g<2>', b)
                    voice.setdefault(b, set())
                    voice[b].add(line.get('say', ''))
                else:
                    voice.setdefault(line[audio], set())
                    voice[line[audio]].add(line.get('say', ''))
    
    os.makedirs('output/voice', exist_ok=True)

    unique = {}
    general = {}
    for b in voice:
        if len(voice[b]) == 1:
            unique[b] = voice[b].pop()
        else:
            general[b] = list(voice[b])    
    with open('output/voice/{}_unique.json'.format(lang), 'w', encoding='utf-8') as fp:
        json.dump(unique, fp, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True)
    with open('output/voice/{}_general.json'.format(lang), 'w', encoding='utf-8') as fp:
        json.dump(general, fp, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True)

    combined = unique
    for b in general:
        combined[b] = '<br>'.join(general[b])
    with open('output/voice/{}.json'.format(lang), 'w', encoding='utf-8') as fp:
        json.dump(combined, fp, ensure_ascii=False, indent=4, separators=(',', ': '), sort_keys=True)

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    parser.add_argument('-f', '--format', action='store_true', help='prefix single-digit numbers with a space')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_story
        dl_story()
    init_story()
    build_voices('EN', args.format)
    build_voices('CN', args.format)
    build_voices('JP', args.format)
