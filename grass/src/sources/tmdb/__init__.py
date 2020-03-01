import os
import gzip
import json
import datetime

from utils import temp_dir


def download_today_file(tmdb_client, url_name, filename):
    load_date = datetime.datetime.today()
    update_time = datetime.datetime(
        year=load_date.year, month=load_date.month, day=load_date.day, hour=8, minute=0, second=0
    )

    if load_date <= update_time:
        load_date -= datetime.timedelta(days=1)

    load_date = load_date.date()

    url = tmdb_client.create_url(url_name, [tmdb_client.format_date(load_date)])

    filename = os.path.join(temp_dir, filename)
    filename_gz = filename + '.gz'

    # download file
    with tmdb_client.clear_send('get', url, stream=True) as r:
        r.raise_for_status()
        with open(filename_gz, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
        r.close()

    # unzip
    with gzip.open(filename_gz, 'rb') as f_gz:
        with open(filename, 'wb') as f:
            while True:
                block = f_gz.read(8192)
                if block == b'':
                    break
                f.write(block)

    # delete gzip file
    os.remove(filename_gz)

    return filename


def read_file(filename):
    with open(filename) as f:
        line = f.readline()
        while line:
            yield json.loads(line)
            line = f.readline()


# test
def test():
    from .client import TMDBApiClient
    tmdb_client = TMDBApiClient()
    download_today_file(tmdb_client, 'files-collections', 'collections.json')
