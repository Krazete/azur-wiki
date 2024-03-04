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

        contents = repo.get_contents('versions/{}.txt'.format(lang))
        ghversion = contents.decoded_content.decode()
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
    '''Iterate outdated ShareCfg folders.'''
    new_version = get_new_version(id, langs)
    if new_version:
        for lang in langs:
            folder = '{}/ShareCfg'.format(lang)
            os.makedirs(folder, exist_ok=True)
            yield folder
        set_new_version(id, new_version)

def dl_child():
    '''Download Project Identity: TB data files.'''
    for folder in get_latest('child', ['EN']):
        contents = repo.get_contents(folder)
        for content in contents:
            if content.name.startswith('child_'):
                with open(content.path, 'wb') as fp:
                    fp.write(content.decoded_content)

def dl_decor():
    '''Download decor data files and List of Furniture Sets wiki page section.'''
    for folder in get_latest('decor', ['CN', 'EN', 'JP']):
        path = '{}/backyard_theme_template.json'.format(folder)
        content = repo.get_contents(path)
        with open(path, 'wb') as fp:
            fp.write(content.decoded_content)
    os.makedirs('input', exist_ok=True)
    html = urlopen('https://azurlane.koumakan.jp/w/index.php?title=Decorations&action=raw&section=8')
    with open('input/decorchartnow.txt', 'wb') as fp:
        fp.write(html.read())
