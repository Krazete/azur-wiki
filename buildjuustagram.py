from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--download', action='store_true', help='download data files')
    args = parser.parse_args()
    if args.download:
        from downloader import dl_sharecfg
        dl_sharecfg('juustagram', ['CN', 'EN', 'JP'], [
            'activity_ins_language',
            'activity_ins_npc_template',
            'activity_ins_ship_group_template',
            'activity_ins_template'
        ])
