# pycleandata

Retrieve and clean datasets for use in machine learning experiments.

## Usage

To process all configured data sets:

``$ python3 cleandata.py``

Or to specify a single data set using the key from ``data.yml``:

``$ python3 cleandata.py <dataset_key>``

## Requirements

 - Python 3
 - numpy
 - pandas
 - PyYAML

## Future work

 - better documentation, especially this file
 - rename cd_data/ to output/ for consistency with pygendata
 - specify config file as command-line option
 - ...and place output in a subdirectory of output/ named after it
 - add a suitable license
 - more flexibility regarding normalisation (and remove the term standardisation)


