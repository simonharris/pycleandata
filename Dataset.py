"""
Some docs
"""

import numpy as np
import pandas as pd

#from cleaners import DefaultCleaner


class Dataset:

    
    INT_FORMAT = '%1i'


    def __init__(self, config):
        self._config = config
        
    
    # Throws etc
    def fetch(self):
   
        import_args = self._fetch_import_args()
        
        #print(import_args)
    
        self._ds = pd.read_csv(self._config['data_url'], **import_args)
                                    #header=None, 
                                    #index_col=0,
                                    #na_values=['?'])
        return True
            
        # TODO: does it throw exceptions?    
        
        
    def process(self): #, cleaner, labeller):
   
    
        # TODO: make this more configurable
        # Drop rows with missing data
        self._ds = self._ds.dropna()
  
        # Assume it's always the last column...for now
        self._labels, _ = pd.factorize(self._ds.iloc[:,-1])
        self._ds = self._ds.iloc[:, :-1]

        return True
        
        
    def save_all(self, location):
        """Save data files to disk"""
    
        np.savetxt(location + '/labels.csv', self._labels, fmt=self.INT_FORMAT)
        np.savetxt(location + '/data.csv', self._ds, delimiter=',')
        # TODO: info.txt or similar
       
        print("SAVED ALL TO:", location, "\n") 

       
    def _fetch_import_args(self):
        """Build a dict from the config file"""
    
        to_get = [
            'na_values',
            'index_col',
        ]
        
        kwargs = {
            'header':None,
            'index_col':False, # TODO: may be more often true
        }
        
        if 'import_args' in self._config:
            for setting in to_get:
                if setting in self._config['import_args']:
                    kwargs[setting] = self._config['import_args'][setting]
            
        return kwargs    
        
