import os
import json
from argparse import ArgumentParser
from github import Github
from educate import textures

# Initialize

child = {}

def init_child():
    '''Initializes `child` object with JSON files downloaded from AzurLaneData repo.'''
    folder = 'EN/ShareCfg'
    for filename in os.listdir(folder):
        if filename.startswith('child_') and filename.endswith('.json'):
            suffix = filename[6:-5]
            with open('{}/{}'.format(folder, filename), 'r', encoding='utf-8') as fp:
                child[suffix] = json.load(fp)

# Save

def save_csv(name, table):
    os.makedirs('output', exist_ok=True)

    csv = ''
    for row in table:
        for cell in row:
            csv += '"{}",'.format(cell.strip())
        csv = csv[:-1] + '\n'
    with open('output/{}.csv'.format(name), 'w', encoding='utf-8') as fp:
        fp.write(csv)
    return csv

def save_wikitable(name, table):
    os.makedirs('output', exist_ok=True)

    lines = ['{| class="wikitable sortable mw-collapsible" style="text-align:center"']
    for i, row in enumerate(table):
        for cell in row:
            lines.append('{} {}'.format('!' if i <= 0 else '|', cell.strip()).strip())
        lines.append('|-')
    lines[-1] = '|}'

    wikitable = '\n'.join(table) + '\n'
    with open('output/{}.wiki'.format(name), 'w', encoding='utf-8') as fp:
        fp.write(wikitable)
    return wikitable

# IDK

def filter_data(key, condition):
    for id in child[key]:
        datum = child[key][id]
        if condition(datum):
            yield datum

# for shopid in child['shop']:
#     filter_data('site_option', lambda datum = shop in datum['param'])

def chart_items():
    items = child['resource'] | child['attr']
    colindex = {}
    table = [['Item', 'Activity', 'Time']]
    for i, iid in enumerate(items):
        table[0].append(items[iid]['name'])
        colindex[iid] = i
    for iid in child['item']:
        item = child['item'][iid]
        table.append([item['name']])

        shids = []
        for shid in child['shop']:
            shop = child['shop'][shid]
            for goods in shop['goods_pool']:
                if iid == goods[0]:
                    shids.append(shid)
        site_options = []
        soids = []
        sotime = []
        for soid in child['site_option']:
            site_option = child['site_option'][soid]
            for shid in shids:
                if shid in site_option['param']:
                    site_options.append(site_option['name'])
                    soids.append(soid)
                    sotime.append(str(site_option['time_limit']))
        sites = []
        for sid in child['site']:
            site = child['site'][sid]
            for soid in soids:
                if soid in site['option']:
                    sites.append(site['name'])
        assert len(site_options) < 2
        assert len(sites) < 2
        table[-1].append('{} - {}'.format(''.join(sites), ''.join(site_options)))
        table[-1].append(''.join(sotime))

        table[-1] += [''] * len(colindex)
        for reward in item['display']:
            i = colindex[reward[1]]
            table[-1][i + 3] = '{:+}'.format(reward[2])
    
    cats = {tab[1]: {'cols': [], 'data': []} for tab in table}
    for tab in table:
        for i, col in enumerate(tab):
            if i in [1, 2]:
                continue
            if col.strip() not in ['', '-']:
                cats[tab[1]]['cols'].append(i)
    for cid in cats:
        cats[cid]['data'] = [[table[0][i] for i in set(sorted(cats[cid]['cols']))]]
    for tab in table:
        cats[tab[1]]['data'].append([tab[i] for i in set(sorted(cats[tab[1]]['cols']))])
    for cid in cats:
        save_wikitable(cid, cats[cid]['data'])

    save_csv('item', table)
    return save_wikitable('item', table)

def chart_arbitrary(key, idkey):
    for intid in child[key]['all']:
        id = str(intid)
        child = child[key][id]

def chart_polaroids():
    table = [['Group', 'ID', 'Title', 'Stage', 'Personality', 'Location']]
    for id in child['polaroid']:
        gid = 0
        for gidstr in child['x']:
            if id in child['x'][gidstr]:
                gid = int(gidstr)

        polaroid = child['polaroid'][id]

        title = polaroid['title']

        slist = [str(i) for i in polaroid['stage']]
        stages = ', '.join(slist)
        
        plist = []
        for pid in polaroid['xingge']:
            plist.append(child['attr'][pid]['name'])
        personalities = ', '.join(plist)

        lset = set()
        for soid in child['site_option']:
            site_option = child['site_option'][soid]
            if gid in site_option['polarid_list']:
                for sid in child['site']:
                    site = child['site'][sid]
                    if soid in site['option']:
                        lset.add(site['name'])
        locations = ', '.join(lset)

        table.append([gid - 100, id, title, stages, personalities, locations])

    save_csv('polaroid', table)

    grouped = {}
    for tab in table:
        if tab[0] in grouped:
            for i, t in enumerate(tab):
                grouped[tab[0]][i].add(t)
        else:
            grouped[tab[0]] = [set([t]) for t in tab]
    gtable = [[', '.join((str(g) for g in gtab)) for gtab in grouped[i]] for i in grouped]
    save_wikitable('polo', gtable)

    return save_wikitable('polaroid', table)

def chart_endings():
    csv = 'Ending,Personality,Stat 1,Value,Stat 2,Value,Ability 1,Value,Ability 2,Value\n'
    table = '{| class="azltable sortable" style="text-align:center"\n'

    for eid in child['ending']:
        ending = child['ending'][eid]
        print(ending['name'])

if __name__ == '__main__':
    # lines = ['This game mode is for special secretaries and does not impact any other aspect of the game at all.']
    # lines.append('==Moments==')
    # lines.append(chart_polaroids())
    # lines.append('==Items==')
    # lines.append(chart_items())

    # page = '\n'.join(line.strip() for line in lines) + '\n'
    # with open('out/page.wiki', 'w', encoding='utf-8') as fp:
    #     fp.write(page)
    # chart_endings()

    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_child
        dl_child()
    init_child()
