import os
import json
from pathlib import Path
from functools import lru_cache
from urllib.request import urlopen
from github import Github

repo = Github().get_repo('AzurLaneTools/AzurLaneData')

versionlog = {}
if os.path.exists('versionlog.json'):
    with open('versionlog.json', 'r') as fp:
        versionlog = json.load(fp)

def get_gh_file(path, decode=False):
    '''Returns decoded content of path or retrieves HTML if content is empty.
    Set decode to True to return the content as a string instead of bytes.'''
    content = repo.get_contents(path)
    if isinstance(content, list):
        print('ERROR:', path, 'is a folder, not a file.')
    elif content.content == '':
        print('NOTE:', path, 'is a big file.')
        html = urlopen(content.download_url)
        bcontent = html.read()
    else:
        bcontent = content.decoded_content
    if decode:
        return bcontent.decode()
    return bcontent

@lru_cache
def get_gh_version(lang):
    '''Returns latest version number for the specified language.'''
    return get_gh_file('versions/{}.txt'.format(lang), True)

def int_to_langs(n):
    '''Decode integer of binary flags into list of languages.'''
    langs = []
    if n // 16 % 2:
        langs.append('TW') # 0b1xxxx; unused
    if n // 8 % 2:
        langs.append('KR') # 0bx1xxx; unused
    if n // 4 % 2:
        langs.append('CN') # 0b1xx
    if n // 2 % 2:
        langs.append('EN') # 0bx1x
    if n % 2:
        langs.append('JP') # 0bxx1
    return langs

def update(langs, paths):
    '''Download files of the specified languages and paths if they are outdated.'''
    if isinstance(langs, int):
        langs = int_to_langs(langs)
    for lang in langs:
        gh_version = get_gh_version(lang)
        for path in paths:
            fullpath = '{}/{}.json'.format(lang, path)
            vl_version = versionlog.get(fullpath, '')
            if vl_version != gh_version:
                os.makedirs(Path(fullpath).parent, exist_ok=True)
                bcontent = get_gh_file(fullpath)
                with open(fullpath, 'wb') as fp:
                    fp.write(bcontent)
                versionlog[fullpath] = gh_version
                print('UPDATED:', fullpath)
                with open('versionlog.json', 'w') as fp:
                    json.dump(versionlog, fp, indent=4, sort_keys=True)
            else:
                print('SKIPPED:', fullpath)

def dl_decor():
    '''Download decor data files and List of Furniture Sets wiki page section.'''
    update(0b111, ['ShareCfg/backyard_theme_template'])
    os.makedirs('input', exist_ok=True)
    html = urlopen('https://azurlane.koumakan.jp/w/index.php?title=Decorations&action=raw&section=9')
    with open('input/decornow.wiki', 'wb') as fp:
        fp.write(html.read())

def dl_child():
    '''Download Project Identity: TB data files.'''
    contents = repo.get_contents('EN/ShareCfg')
    paths = []
    for content in contents:
        if content.name.startswith('child'):
            paths.append('ShareCfg/{}'.format(content.name[:-5])) # trim '.json'
    update(0b010, paths)

def dl_story():
    '''Download story data files.'''
    paths = [
        'ShareCfg/memory_group', # memory groups
        'ShareCfg/memory_template', # memories
        'ShareCfg/ship_skin_template', # shipgirl names
        'ShareCfg/name_code', # shipgirl namecodes
        # 'GameCfg/story', # memory text
        'GameCfg/dungeon' # battle sim info
    ]
    update(0b111, paths)
    update(0b110, ['GameCfg/story'])
    update(0b001, ['GameCfg/storyjp']) # nonstandard naming
