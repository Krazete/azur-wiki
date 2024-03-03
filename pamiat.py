import re
from time import sleep
from mwclient import Site

# https://mwclient.readthedocs.io/en/latest/reference/site.html
# https://mwclient.readthedocs.io/en/latest/reference/page.html

site = Site('azurlane.koumakan.jp')

# first create `username` and `password` files in `input` folder
with open('input/username', 'r') as fp:
    username = fp.read().strip()
with open('input/password', 'r') as fp:
    password = fp.read().strip()
site.login(username, password)

# search; rerun as necessary to update results
search_pamiat = list(site.search('Merkuria', namespace='idk'))

### ONLY PAGE TITLE IS NEEDED ###

titles = []
for result in search_pamiat:
    titles.append(result.get('title'))

# move pages
errors_move = []
skips_move = []
for title in titles:
    if 'Pamiat Merkuria' in title:
        newtitle = re.sub(r"(Pamiat)([^'])", r"\g<1>'\g<2>", title)
        if newtitle in titles:
            print('SKIP:', title)
            skips_move.append(title)
        else:
            try:
                page = site.pages.get(title)
                page.move(newtitle, 'apostrophe')
            except Exception as e:
                print('ERROR:', title, '\n\t', e)
                errors_move.append(title)
            sleep(10)
print(errors_move)
print(skips_move)

# delete redirects
errors_delete = []
unmatched = []
for title in titles:
    if 'Pamiat Merkuria' in title:
        newtitle = re.sub(r"(Pamiat)([^'])", r"\g<1>'\g<2>", title)
        if newtitle in titles:
            try:
                page = site.pages.get(title)
                page.edit('{{delete}}')
            except Exception as e:
                print('ERROR:', title, '\n\t', e)
                errors_delete.append(title)
            sleep(10)
        else:
            print('NO MATCHING NEW PAGE:', title)
            unmatched.append(title)
print(errors_delete)
print(unmatched)

### PAGE TITLE AND PAGE TEXT ARE NEEDED ###

results = {}
for result in search_pamiat:
    results[result.get('title')] = ''
for title in results:
    page = site.pages.get(title)
    results[title] = page.text()

# add skin file data
errors_skin = []
not_skins = []
for title in results:
    if "Pamiat' Merkuria" in title and '.png' in title:
        if 'META' in title:
            continue
        try:
            page = site.pages.get(title)
            if 'SkinFileData' in results[title]:
                page.edit("{{SkinFileData|Pamiat' Merkuria}}", 'fixed SkinFileData')
            else:
                not_skins.append(title)
        except Exception as e:
            print('ERROR:', title, '\n\t', e)
            errors_skin.append(title)
        sleep(10)
print(errors_skin)
print(not_skins)

# fix reference links
errors_link = []
skips_link = []
for title in results:
    if ':' in title and ': ' not in title: # skip File, Module, Template, User, etc.
        continue
    try:
        page = site.pages.get(title)
        text = results[title]
        newtext = text.\
            replace('[Pamiat Merkuria]', "[Pamiat' Merkuria]").\
            replace('[Pamiat_Merkuria]', "[Pamiat' Merkuria]").\
            replace('[S:Pamiat Merkuria', "[S:Pamiat' Merkuria").\
            replace('[S:Pamiat_Merkuria', "[S:Pamiat' Merkuria").\
            replace('[O:Pamiat Merkuria', "[O:Pamiat' Merkuria").\
            replace('[O:Pamiat_Merkuria', "[O:Pamiat' Merkuria")
        if text == newtext:
            print('SKIP:', title)
            skips_link.append(title)
        else:
            page.edit(newtext, 'apostrophe')
    except Exception as e:
        print('ERROR:', title, '\n\t', e)
        errors_link.append(title)
    sleep(10)
print(errors_link)
print(skips_link)

# check all other instances
for title in results:
    text = results[title]
    if 'Pamiat Merk' in text:
        print(title)
