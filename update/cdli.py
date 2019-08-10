'Common routines for accessing the CDLI catalogue.'

import io
import os
import csv
import fileinput

files = [
    'cdli_catalogue_1of2.csv',
    'cdli_catalogue_2of2.csv',
]


def as_utf8(filename, mode='r'):
    '''Return a file opened as UTF-8 text.

    The gives correct unicode strings on systems where the
    default text encoding is different.'''
    return io.open(filename, mode, encoding='utf-8')


def _catalogue_reader(data_path):
    'Helper returning a DictReader instance over the data.'

    filenames = [os.path.join(data_path, fn) for fn in files]

    csvfile = fileinput.input(files=filenames, openhook=as_utf8)
    return csv.DictReader(csvfile)


def read_catalogue(data_path):
    '''Concatenate and read the catalogue file data.

    Read catalogue data from the given path, which should
    be a directory containing the export data files.

    The catalogue is split into multiple smaller files to fit
    better in a git repository. Open these in sequence and
    yield a series of dictionaries representing each row.

    The keys in the dictionary are taken from the column labels
    on the first row.'''

    for row in _catalogue_reader(data_path):
        yield row


def id_from_row(row):
    'Construct a CDLI id from a catalogue data dictionary.'

    # The index is stored as an integer.
    # CDLI reference numbers start with P and have 6 digits.
    return f'P{int(row["id_text"]):06d}'


def print_entries(data_path):
    'Dump each row in the catalogue for debugging.'
    for row in read_catalogue(data_path):
        print(id_from_row(row), row['designation'])
