"""
Some docs
"""

import numpy as np
import pandas as pd

from cleaners import DefaultCleaner


class Dataset:

    
    INT_FORMAT = '%1i'


    def __init__(self, config):
        self._config = config
        
    
    # Throws etc
    def fetch(self):
    
        self._ds = pd.read_csv(self._config['data_url'], names=[], na_values=['?'])

        return True
        
        
    def process(self, cleaner, labeller):
    
    
    
        self._the_data = cleaner.clean(self._ds)
        self._the_labels = labeller.label(self._ds)
        
    
        return True;
        '''
        self._data, self._labels = cleaner.clean(

        # Lose the ID column
        ds = ds.drop('SCN', axis=1)

        # Drop rows with missing data
        ds = ds.dropna()

        # Convert the 2/4 labels to 1/0 and move to another dataframe
        labels = ds.loc[:,'Class'].values > 3
        ds = ds.drop('Class', axis=1)
        '''
        
        
    def save_all(self, location):
    
        labels = [1, 2, 3]
        data = [2, 3, 4]
    
        np.savetxt(location + '/labels.csv', labels, fmt=self.INT_FORMAT)
        np.savetxt(location + '/data.csv', data, fmt=self.INT_FORMAT, delimiter=',')
        # TODO: info.txt or similar
       
        print("I DONE SAVED ALL TO:", location) 

        
 
        
        
