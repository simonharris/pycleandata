"""
Main script for importing databases to cleandata
"""

import csv
import os
from pprint import pprint
import sys
import yaml

from dataset import Dataset


DATA_DIR = './cd_data/'


def import_dataset(key, conf):
    """Triggers import and cleaning of individual dataset"""

    print(key.upper())

    newdir = DATA_DIR + key
    os.makedirs(newdir, exist_ok=True)

    ds = Dataset(key, conf)

    # try/catch etc
    if (ds.fetch() and ds.process()):
        info = ds.save_all(newdir)

        all_info.append([info['name'],
                         info['samples_post'],
                         info['num_features'],
                         info['num_labels'],
                         ]
                        )

    else:
        print("ERROR")


# Main method -----------------------------------------------------------------


if __name__ == "__main__":

    dst = None
    all_info = []

    # TODO: this is kind of hacky
    if len(sys.argv) > 1:
        dst = sys.argv[1]

    with open("data.yml", 'r') as stream:
        try:
            cnf = yaml.load(stream, Loader=yaml.SafeLoader)

            cnt = 0

            # if a single dataset is specified
            if dst is not None:
                import_dataset(dst, cnf[dst])
                cnt = 1
            # else import the lot
            else:
                for dst in cnf:
                    import_dataset(dst, cnf[dst])
                    cnt += 1

        except yaml.YAMLError as exc:
            print(exc)

    print("Processed %i datasets" % (cnt))
    all_info = sorted(all_info, key=lambda x: x[0])
    all_info = [['name', 'objects', 'features', 'classes']] + all_info
    pprint(all_info)

    with open("realworld.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerows(all_info)
