from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import update
        update(['CN', 'EN', 'JP'], [
            'ShareCfg/activity_ins_language',
            'ShareCfg/activity_ins_npc_template',
            'ShareCfg/activity_ins_ship_group_template',
            'ShareCfg/activity_ins_template'
        ])
