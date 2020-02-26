import sys


def main():
    arg = sys.argv[1]
    if arg == 'tmdb-file':
        from sources.tmdb import test
        test()
    elif arg == 'tmdb-startup':
        from sources.tmdb.tasks import startup
        startup()
    elif arg == 'tmdb-changes':
        import datetime
        from sources.tmdb.tasks import process_changes
        today = datetime.date.today() - datetime.timedelta(days=1)
        process_changes(today, today)
    else:
        raise Exception


if __name__ == '__main__':
    main()
