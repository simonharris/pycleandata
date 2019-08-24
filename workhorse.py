"""
Python file
"""

import os
import yaml

import pandas as pd

from Dataset import Dataset
from cleaners.DefaultCleaner import DefaultCleaner
from labellers.DefaultLabeller import DefaultLabeller


DATA_DIR='./cd_data/'


def import_dataset(key, conf):
    """The actual stuff"""
    
    print(conf['data_url'])

    newdir = DATA_DIR + key
    os.makedirs(newdir, exist_ok=True)

    ds = Dataset(conf)
    
    # try/catch etc
    if (ds.fetch() 
            and ds.process(DefaultCleaner(), DefaultLabeller())):
        ds.save_all(newdir)
        print("YAY :)")
        
    else:
        print("NAY :(")


def save_dataset(foo):
    print(foo)  

        
## Main method -----------------------------------------------------------------
        
 
if __name__ == "__main__": 
        
    with open("data.yml", 'r') as stream:
        try:
            cnf = yaml.load(stream, Loader=yaml.SafeLoader)
        
            for dst in cnf:
                import_dataset(dst, cnf[dst])

        except yaml.YAMLError as exc:
            pass
            #print(exc)
        
    
    #print("Done")

