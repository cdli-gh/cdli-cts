# Canonical Cuneiform Text Scripts

This directory contains scripts for maintaining the data in
the rest of the repository, and is intended for developers.

Specifically `Dockerfile` describes a container which invokes
the `run.sh` script to periodically pull changes from the
bulk data export repository, filter them through `cdli2cts`,
and push the changes.

To set this up, change to this directory and execute:

```
docker build -t cdli-cts-update .
docker run -d -rm --name cdli-cts-update \
  -v /path/to/cdli-data:/data/cdli-data \
  -v /path/to/cdli-cts:/data/cdli-cts \
  cdli-cts-update
```

Then run `docker logs cdli-cts-update` to obtain the container's
ssh public key. Set this as a deployment key on the
[cdli-cts](https://github.com/cdli-gh/cdli-cts)
repository with write permission so the container can push
changes. You can bind-mount a `.ssh` directory to `/root/.ssh`
in the container if you want to set the deployment key externally.

Edit the `included_*` lists in `cdli2cts.py` to change what is
included in the conversion.

The script expects to find working checkouts of the bulk data export
repo in `/data/cdli-data` and of this repo in `/data/cdli-cts`.
If you provide a cdli-cts repo, it must be set up to push to
its origin repo.

If no bind mount is provided, the container will create fresh
clones at startup. You can save the significant bandwidth of
the download on subsequent runs by mounting a persistent storage
volume over `/data`.

Be ware of bind-mounting the same cdli-cts checkout where you're
editing the scripts. The container will clobber any changes.

## Environment

The following variables can be set to control where `run.sh` looks
for resources:

- `DATA_PATH` : Location of the cdli-data repository checkout.
- `CTS_PATH` : Location of the cdli-cts repository checkout.
- `INTERVAL` : How long to wait (in seconds) between invocations
  of `cdli2cts`.
- `SSH_KEY` : Location of the ssh public key file to use for pushes.

For example, you could change the update interval with

    docker run --env INTERVAL=300 cdli-cts-update

Please file an issue if you have any questions or suggestions.
