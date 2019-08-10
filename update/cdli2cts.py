#!/usr/bin/env python3

'Script to convert the CDLI atf database to a CTS file hierarchy.'

import io
import os
import cdli
import atf2cts

'Catalogue metadata fields to keep for filtering.'
catalogue_keys = [
        'designation',
        'accession_no',
        'museum_no',
        'language',
        'primary_publication',
        'publication_history',
        'genre',
        'object_type',
        'period',
        'provenience',
]


'ATF records to include by CDLI id.'
included_ids = [
        'P481090',
        'P464358',
        'P497322',
]

'ATF records to include by catalogue entry.'
included_metadata = {
        'museum_no': 'BM — PJ',
}


def included(data, id):
    'Return whether a CDLI id should be included in the conversion.'
    if id in included_ids:
        return True
    for key, value in included_metadata.items():
        if data[id][key] == value:
            return True
    return False


def load_catalogue(data_path):
    'Load catalogue metadata into a dict for reference.'
    data = {}
    for row in cdli.read_catalogue(data_path):
        cdli_id = cdli.id_from_row(row)
        data[cdli_id] = {key: row[key] for key in catalogue_keys}
    return data


def read_atf(data_path):
    'Read and segment the atf data export.'
    filename = os.path.join(data_path, 'cdliatf_unblocked.atf')
    fp = io.open(filename, encoding='utf-8')
    for atf in atf2cts.segmentor(fp):
        # Parse out the CDLI id code.
        if atf.startswith('&P'):
            # Drop the '&' sigil and any trailing garbage.
            cdli_id = atf[1:8]
        elif atf.startswith('&'):
            # Handle broken entries with whitespace around the id.
            token = atf.split()[1]
            cdli_id = token[0:7]
            print('Warning: whitespace at the start of &-line.')
        else:
            cdli_id = ''
        # Check if we found what looks like a cdli id.
        if not cdli_id.startswith('P') or not cdli_id[1:].isdecimal():
            print("Error: ATF record doesn't start with a CDLI id!")
            print(atf.splitlines()[0])
            continue
        # Parse out the language header, if any.
        language = None
        for line in atf.splitlines():
            if line.startswith('#atf') and 'lang' in line:
                part = line.split('lang')
                # Skip spurious equal signs.
                # These are invalid syntax, but occur sometimes.
                if part[1].strip() == '=':
                    del part[1]
                language = part[1].strip()
                break
        yield (cdli_id, language, atf)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='Convert the CDLI bulk export data to CTS.')
    parser.add_argument(
        '-d', '--data_path', required=True,
        help='path to a directory containing the exporet data files.')
    parser.add_argument(
        '-o', '--output_path', required=True,
        help='path to write the CTS file hierarchy under.')
    args = parser.parse_args()

    print('Loading catalogue from', args.data_path)
    data = load_catalogue(args.data_path)
    print('Parsing atf data from', args.data_path)
    output_path = os.path.join(args.output_path, 'data')
    successful = 0
    parse_failures = 0
    export_failures = 0
    missing = []
    extra = []
    atf_ids = set()
    for cdli_id, language, atf in read_atf(args.data_path):
        atf_ids.add(cdli_id)
        if cdli_id not in data:
            print('WARNING: atf not in catalogue', cdli_id)
            missing.append(cdli_id)
            continue
        if included(data, cdli_id):
            s, p, e = atf2cts.convert(atf, output_path)
            successful += s
            parse_failures += p
            export_failures += e

    if parse_failures:
        print('Error:', parse_failures, 'records did not convert.')
    if export_failures:
        print('Error:', export_failures, 'records did not serialize.')
    print(f'Successfully converted {successful} records from ATF.')

    if missing:
        print(f'{len(missing)} atf records do not have catalogue entries:')
        print(','.join(missing))
    atf_available = [key for key in data.keys() if key in atf_ids]
    ratio = len(atf_available)/len(data)
    print(f'{ratio*100:0.2f}% of catalogue entries have atf records.')
