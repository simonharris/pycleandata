"""
Main dataset processor
"""

from os.path import isfile
from pprint import pprint
import urllib.request

import numpy as np
import pandas as pd


# DEBUG = True
DEBUG = False


def debug(data):
    """Prints things out"""
    if DEBUG:
        print(data)


class Dataset:
    """Main processor for datasets"""

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
            'num_labels': None,
            'name': self._config['name'],
        }

        self._ds = None      # see self.fetch()
        self._labels = None  # see self.process()

    def fetch(self):
        """Download, cache and parse file"""

        cache_file = self.CACHE_DIR + self._key

        if not isfile(cache_file):
            urllib.request.urlretrieve(self._config['data_url'], cache_file)

        import_args = self._fetch_import_args()
        debug(import_args)

        self._ds = pd.read_csv(cache_file, **import_args)

        return True

    def process(self):
        """Data cleaning and label management"""

        self._info['samples_pre'] = self._ds.shape[0]

        debug(self._ds)

        # Drop rows with missing data (TODO: make this more configurable?)
        self._ds = self._ds.dropna()

        self._info['samples_post'] = self._ds.shape[0]

        # Assume we always have labels...for now
        if 'label_col' in self._config:
            label_col = self._config['label_col']
        else:
            # TODO: this doesn't work if you have an index column
            #   or have used 'usecols'. In those cases you currently
            #   have to explicitly specify a label_col
            label_col = self._ds.shape[1]-1

        debug(self._ds[label_col])

        self._labels, _ = pd.factorize(self._ds[label_col])
        self._info['num_labels'] = len(np.unique(self._labels))
        self._ds = self._ds.drop(label_col, axis=1)

        return True

    def save_all(self, location, standardise=True):
        """Save data files to disk"""

        export_args = self._fetch_export_args()
        debug(export_args)

        if 'dropcols' in export_args:
            for col in export_args['dropcols']:
                self._ds = self._ds.drop(col, axis=1)

        # if 'format' in export_args:
        #     fmt = export_args['format']
        # else:
        #     fmt = self.FORMAT_FLT

        # Once standardised it will always be a float
        fmt = self.FORMAT_FLT

        if standardise:
            self._ds = self._stddise(self._ds)

        np.savetxt(location + '/labels.csv', self._labels, fmt=self.FORMAT_INT)
        np.savetxt(location + '/data.csv', self._ds, fmt=fmt, delimiter=',')

        self._info['num_features'] = self._ds.shape[1]

        pprint(self._info)

        print("SAVED ALL TO:", location, "\n")

        return self._info

    def _fetch_import_args(self):
        """Fetch import_args from config file"""

        # Set up some defaults
        kwargs = {
            'header': None,
            'index_col': False,
        }

        # Then supplement or override them if they're in the config
        to_get = [
            'header',
            'index_col',
            'na_values',
            'names',
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

    @staticmethod
    def _stddise(matrix):
        """Standardise as per above comment"""

        matrix = np.array(matrix)

        debug(np.sum(matrix, axis=0))

        # TODO: fix the glaring division by 0 bug
        std = (matrix - matrix.mean(axis=0)) / \
            (matrix.max(axis=0) - matrix.min(axis=0))

        return std
