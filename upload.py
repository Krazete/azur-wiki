from time import sleep
from mwclient import Site

site = Site('azurlane.koumakan.jp')

with open('input/username', 'r') as fp:
    username = fp.read().strip()
with open('input/password', 'r') as fp:
    password = fp.read().strip()
site.login(username, password)

def uploadimage(path, content='', summary='', ignore=False):
    with open(path, 'rb') as fp:
        return site.upload(fp, path.split('/')[-1], content, ignore=ignore, comment=summary)
    sleep(0.5)

def updateimage(path, summary='update'):
    uploadimage(path, '', summary, True)

