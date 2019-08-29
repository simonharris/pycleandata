"""
Main script for importing databases to cleandata
"""

import os
import sys
import yaml

from Dataset import Dataset


DATA_DIR = './cd_data/'


def import_dataset(key, conf):
    """Triggers import and cleaning of individual dataset"""

    print(key.upper())

    newdir = DATA_DIR + key
    os.makedirs(newdir, exist_ok=True)

    ds = Dataset(key, conf)

    # try/catch etc
    if (ds.fetch() and ds.process()):
        ds.save_all(newdir)
    else:
        print("ERROR")


# Main method -----------------------------------------------------------------


if __name__ == "__main__":

    dst = None

    # TODO: this is kind of hacky
    if len(sys.argv) > 1:
        dst = sys.argv[1]

    with open("data.yml", 'r') as stream:
        try:
            cnf = yaml.load(stream, Loader=yaml.SafeLoader)

            cnt = 0

            if dst is not None:
                import_dataset(dst, cnf[dst])
                cnt = 1
            else:
                for dst in cnf:
                    import_dataset(dst, cnf[dst])
                    cnt += 1

        except yaml.YAMLError as exc:
            print(exc)

    print("Processed %i datasets" % (cnt))
