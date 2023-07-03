from flask_caching import Cache
import pandas as pd

# just some csv data to open for use on different pages
FILE_LIST = [
    'https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-10000.csv',
    'https://github.com/datablist/sample-csv-files/raw/main/files/organizations/organizations-100000.csv'
]

# setting up the disk cache
CACHE_CONFIG = {
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': './cache',
    "CACHE_DEFAULT_TIMEOUT": 0
}
cache = Cache()


@cache.memoize()
def open_file(arg: str):
    print('got cached: ', arg)
    return pd.read_csv(arg)

