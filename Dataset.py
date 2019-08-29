"""
Main dataset processor
"""

import os
from pprint import pprint
import urllib.request

import numpy as np
import pandas as pd


DEBUG=True
DEBUG=False

def debug(data):
    if DEBUG:
        print(data)


class Dataset:

    FORMAT_INT = '%i'
    FORMAT_FLT = '%f'
    CACHE_DIR = './_cache/'

    def __init__(self, key, config):
        self._key = key
        self._config = config

        self._info = {
            'url': self._config['data_url'],
            'samples_pre': None,
            'samples_post': None,
            'labels': None,
        }


    def fetch(self):
        """Download, cache and parse file"""

        cache_file = self.CACHE_DIR + self._key

        if not os.path.isfile(cache_file):
            urllib.request.urlretrieve(self._config['data_url'], cache_file)

        import_args = self._fetch_import_args()
        debug(import_args)

        self._ds = pd.read_csv(cache_file, **import_args)

        # TODO: handle errors
        return True


    def process(self): #, cleaner, labeller):
        """Data cleaning and label management"""

        self._info['samples_pre'] = self._ds.shape[0]

        #debug(self._ds)

        # Drop rows with missing data (TODO: make this more configurable?)
        self._ds = self._ds.dropna()

        self._info['samples_post'] = self._ds.shape[0]

        # Assume we always have labels...for now
        if 'label_col' in self._config:
            lc = self._config['label_col']
        else:
            # TODO: this doesn't work if you have an index column
            #   or have used 'usecols'. In those cases you currently
            #   have to explicitly specify a label_col
            lc = self._ds.shape[1]-1

        debug(self._ds[lc])

        self._labels, _ = pd.factorize(self._ds[lc])
        self._info['labels'] = len(np.unique(self._labels))
        self._ds = self._ds.drop(lc, axis=1)

        return True


    def save_all(self, location):
        """Save data files to disk"""

        export_args = self._fetch_export_args()
        debug(export_args)

        if 'dropcols' in export_args:
            for col in export_args['dropcols']:
                self._ds = self._ds.drop(col, axis=1)

        #debug(self._ds)

        # TODO: may need to handle other formats for output data
        np.savetxt(location + '/labels.csv', self._labels, fmt=self.FORMAT_INT)
        np.savetxt(location + '/data.csv', self._ds, fmt=self.FORMAT_FLT, delimiter=',')

        pprint(self._info)

        print("SAVED ALL TO:", location, "\n")


    def _fetch_import_args(self):
        """Fetch import_args from config file"""

        # Set up some defaults
        kwargs = {
            'header':None,
            'index_col':False,
        }

        # Then supplement or override them if they're in the config
        to_get = [
            'header',
            'index_col',
            'na_values',
            'sep',
            'usecols',
        ]

        if 'import_args' in self._config:
            for setting in to_get:
                if setting in self._config['import_args']:
                    kwargs[setting] = self._config['import_args'][setting]

        return kwargs


    def _fetch_export_args(self):

        if 'export_args' in self._config:
            return self._config['export_args']

        return []
