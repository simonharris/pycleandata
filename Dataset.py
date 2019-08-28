"""
Main dataset processor
"""

import os
from pprint import pprint
import urllib.request

import numpy as np
import pandas as pd


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
        
    
    # Throws etc
    def fetch(self):
        """Download, cache and parse file"""
   
        cache_file = self.CACHE_DIR + self._key

        if not os.path.isfile(cache_file):
            urllib.request.urlretrieve(self._config['data_url'], cache_file)

        import_args = self._fetch_import_args()
        self._ds = pd.read_csv(cache_file, **import_args)

        # TODO: handle errors
        return True
        
        
    def process(self): #, cleaner, labeller):
        """Data cleaning and label management"""  
        
        self._info['samples_pre'] = self._ds.shape[0]
        
        # Drop rows with missing data (TODO: make this more configurable?)
        self._ds = self._ds.dropna()
  
        self._info['samples_post'] = self._ds.shape[0]
  
        # Assume we always have labels...for now
        if 'label_col' in self._config:
            lc = self._config['label_col']
        else:
            lc = self._ds.shape[1]-1
        
        self._labels, _ = pd.factorize(self._ds.iloc[:,lc])
        self._info['labels'] = len(np.unique(self._labels))
        self._ds = self._ds.drop(lc, axis=1)

        return True
        
        
    def save_all(self, location):
        """Save data files to disk"""
        
        # TODO: may need to handle other formats for output data     
        np.savetxt(location + '/labels.csv', self._labels, fmt=self.FORMAT_INT)
        np.savetxt(location + '/data.csv', self._ds, fmt=self.FORMAT_FLT, delimiter=',')
        
        pprint(self._info)
        
        print("SAVED ALL TO:", location, "\n") 

       
    def _fetch_import_args(self):
        """Build a dict from the config file"""
    
        to_get = [
            'na_values',
            'index_col',
        ]
        
        kwargs = {
            'header':None,
            'index_col':False,
        }
        
        if 'import_args' in self._config:
            for setting in to_get:
                if setting in self._config['import_args']:
                    kwargs[setting] = self._config['import_args'][setting]
            
        return kwargs    
        
