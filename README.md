# Canonical Cuneiform Texts

*Currently __experimental__ and __incomplete__!*

This is a collection of cuneiform tablets in
[Canonical Text Services](http://cite-architecture.org/) format,
from the database of the
[Cuneiform Digital Library Initiative](https://cdli.ucla.edu).
This format is used by a number of viewing an analysis tools
for learning and scholarship. It is hoped that this collection
will make the texts more accessible.

- Converted by [atf2tei](https://github.com/cdli-gh/atf2tei)
  from `cdliatf_unblocked.atf` in the
  [data repository](https://github.com/cdli-gh/data).
- Layout following the [CapiTainS Guidelines](http://capitains.org/pages/guidelines).

## Adding files

Cuneiform transcriptions are normally maintained in the
[ATF](http://oracc.museum.upenn.edu/doc/help/editinginatf/primer/) format.
To add new texts or update the collection run the transcriptions through
the `atf2cts` tool from the [atf2tei](https://github.com/cdli-gh/atf2tei)
package.

For example, to convert a atf file containing one or more tablet
transcriptions and add it to the repository:

```
pip install pipenv # if necessar.
git clone https://github.com/cdli-gh/atf2tei
cd atf2tei
pipenv install
pipenv run python atf2cts.py /path/to/your/transcription.atf
mv data/* ../data/
```

A simple `git status` should then show the added (or changed) files.

## Updating

There is also a script in the update directory which reads the entire
CDLI bulk data export and converts a subset of the records, based
on a list of CDLI id numbers or particular catalogue field entries.

```
git clone --depth https://github.com/cdli-gh/data cdli-data
pipenv install pyoracc
PYTHONPATH=$PWD/atf2tei update/cdli2cts.py -d cdli-data -o .
```

The data repository is quite large. Passing the `--depth` option
to git downloads only the most recent changes, reducing the size
to several hundred MB.

Until `atf2cts` is properly packaged, it also needs to be checked
out with git and the location passed through the `PYTHONPATH`
environment variable. See the section above about added files
for how to do this.

A docker container configuration is included which can be used
to set up automatic updates. See [update](update/README.md) for
details.
