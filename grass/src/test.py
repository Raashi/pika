import sys


def main():
    arg = sys.argv[1]
    if arg == 'tmdb-file':
        from sources.tmdb import test
        test()
    elif arg == 'tmdb-startup':
        from sources.tmdb.tasks import startup
        startup()
    else:
        raise Exception


if __name__ == '__main__':
    main()
