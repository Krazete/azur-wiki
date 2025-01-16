import os
import json
from urllib.request import urlopen
from github import Github

repo = Github().get_repo('AzurLaneTools/AzurLaneData')

versionlog = {}
if os.path.exists('versionlog.json'):
    with open('versionlog.json', 'r') as fp:
        versionlog = json.load(fp)

def get_new_version(id, langs):
    '''Return new versionlog if outdated. Return False otherwise.'''
    up_to_date = True
    ghversionlog = {}
    for lang in langs:
        idversionlog = versionlog.get(id, {})
        idversion = idversionlog.get(lang)

        decontent = get_decontent('versions/{}.txt'.format(lang))
        ghversion = decontent.decode()
        ghversionlog.setdefault(lang, ghversion)

        if idversion != ghversion:
            up_to_date = False
    if up_to_date:
        return False
    return ghversionlog

def set_new_version(id, ghversionlog):
    '''Update versionlog.'''
    versionlog[id] = ghversionlog
    with open('versionlog.json', 'w') as fp:
        json.dump(versionlog, fp)

def get_latest(id, langs):
    '''Iterate updated localized data folders.'''
    new_version = get_new_version(id, langs)
    if new_version:
        for lang in langs:
            os.makedirs(lang, exist_ok=True)
            yield lang
        set_new_version(id, new_version)
        print('Data updated.')
    else:
        print('Data is up to date.')

def get_decontent(path):
    '''Returns decoded content of path or retrieves HTML if content is empty.'''
    content = repo.get_contents(path)
    if isinstance(content, list):
        print('ERROR:', path, 'is a folder, not a file.')
    if content.content == '':
        print('NOTE:', path, 'is a big file.')
        html = urlopen(content.download_url)
        return html.read()
    return content.decoded_content

def dl_from(id, langs, parent, files):
    '''Download specific files from specific parent folder(s).'''
    for lang in get_latest(id, langs):
        folder = '{}/{}'.format(lang, parent)
        os.makedirs(folder, exist_ok=True)
        for file in files:
            path = '{}/{}.json'.format(folder, file)
            decontent = get_decontent(path)
            with open(path, 'wb') as fp:
                fp.write(decontent)

def dl_sharecfg(id, langs, files):
    '''Download specific files from the ShareCfg folder(s).'''
    dl_from(id, langs, 'ShareCfg', files)

def dl_decor():
    '''Download decor data files and List of Furniture Sets wiki page section.'''
    dl_sharecfg('decor', ['CN', 'EN', 'JP'], ['backyard_theme_template'])
    os.makedirs('input', exist_ok=True)
    html = urlopen('https://azurlane.koumakan.jp/w/index.php?title=Decorations&action=raw&section=9')
    with open('input/decornow.txt', 'wb') as fp:
        fp.write(html.read())

def dl_child():
    '''Download Project Identity: TB data files.'''
    for lang in get_latest('child', ['EN']):
        folder = '{}/ShareCfg'.format(lang)
        os.makedirs(folder, exist_ok=True)
        contents = repo.get_contents(folder)
        for content in contents:
            if content.name.startswith('child_'):
                with open(content.path, 'wb') as fp:
                    fp.write(content.decoded_content)

def dl_story():
    '''Download story data files.'''
    subpaths = [
        'ShareCfg/memory_group', # memory groups
        'ShareCfg/memory_template', # memories
        'ShareCfg/ship_skin_template', # shipgirl names
        'ShareCfg/name_code', # shipgirl namecodes
        'GameCfg/story', # memory text
        'GameCfg/dungeon' # battle sim info
    ]
    for lang in get_latest('story', ['CN', 'EN', 'JP']):
        for subfolder in ['Share', 'Game']:
            folder = '{}/{}Cfg'.format(lang, subfolder)
            os.makedirs(folder, exist_ok=True)
        for subpath in subpaths:
            path = '{}/{}.json'.format(lang, subpath)
            with open(path, 'wb') as fp:
                if 'JP/GameCfg/story' in path: # nonstandard naming
                    path = '{}/{}jp.json'.format(lang, subpath)
                decontent = get_decontent(path)
                fp.write(decontent)

def dl_medal_experimental():
    '''Download abextract_medal.py stuff.'''
    for lang in get_latest('medal_experimental', ['EN']):
        folder = '{}/ShareCfg'.format(lang)
        os.makedirs(folder, exist_ok=True)
        path = '{}/ShareCfg/medal_template.json'.format(lang)
        with open(path, 'wb') as fp:
            decontent = get_decontent(path)
            fp.write(decontent)
