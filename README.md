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

## Updating

Cuneiform transcriptions are normally maintained in the
[ATF]() format. To add new texts or update the collection
run the export through the `atf2cts` tool from the
[atf2tei](https://github.com/cdli-gh/atf2tei) package.

For example, fetch the latest data export published by
the cdli:

```
curl -O https://raw.githubusercontent.com/cdli-gh/data/master/cdliatf_unblocked.atf
```

Now convert the data and replace the copy in this repository checkout:

```
git clone https://github.com/cdli-gh/atf2tei
cd atf2tei
pipenv install
pipenv run python atf2cts.py ../cdliatf_unblocked.atf
mv data ../
```

A simple `git status` should then show the changed files.
