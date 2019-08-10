#!/bin/sh -e

# Periodically pull, run the conversion, and push changes from
# the bulk data export repo to the cdli-cts repo.

# Log the time we started running.
echo "--- launch $(date -u) ---"

# Configuration.
# Can be overridden by setting the same variables in the environment.
: ${DATA_PATH:=/data/cdli-data}
: ${CTS_PATH:=/data/cdli-cts}
: ${INTERVAL:=21600}

: ${APPDIR:=$(dirname $0)}
: ${PYTHONPATH:=$APPDIR/atf2tei}
: ${SSH_KEY:=$HOME/.ssh/id_rsa.pub}

# Set up the environment if requested.
if [ "$1" == "--setup" ]; then

  echo "--- setup  $(date -u) ---"

  # Checkout the data repo if none was provided.
  if ! [ -d ${DATA_PATH}/.git ]; then (
    set -x
    mkdir -p $(dirname ${DATA_PATH})
    git clone --depth 10 https://github.com/cdli-gh/data ${DATA_PATH}
  )
  fi

  # Checkout the cdli-cts repo if none was provided.
  # Set up push over ssh for uploading new conversions.
  if ! [ -d ${CTS_PATH}/.git ]; then (
    set -x
    mkdir -p $(dirname ${CTS_PATH})
    git clone --depth 10 https://github.com/cdli-gh/cdli-cts ${CTS_PATH}
    git -C ${CTS_PATH} remote set-url origin --push git@github.com:cdli-gh/cdli-cts
    git -C ${CTS_PATH} config user.name "CDLI CTS Update"
    git -C ${CTS_PATH} config user.email "no-reply@cdli.ucla.edu"
  )
  fi

  # Generate an ssh keypair if none was provided.
  if ! [ -f ${SSH_KEY} ]; then (
    set -x
    ssh-keygen -N '' -f ${SSH_KEY%.pub}
  )
  fi
  # Write the public half of the keypair to the log
  # so we can be authorized out-of-band to push changes.
  cat ${SSH_KEY}

fi # End of set up.

# Loop forever, periodically running a conversion.
while /bin/true; do

  # Log the time we started running.
  echo "--- start  $(date -u) ---"

  # Start logging commands.
  set -x

  # Update the upstream data repo.
  git -C ${DATA_PATH} pull
  commit=$(git -C ${DATA_PATH} rev-parse HEAD)

  # Reset to the latest upstream cts revision.
  git -C ${CTS_PATH} fetch
  git -C ${CTS_PATH} reset --hard origin/master

  # Run the conversion.
  rm -rf ${CTS_PATH}/data
  PYTHONPATH=${PYTHONPATH} pipenv run python cdli2cts.py \
    -d ${DATA_PATH} \
    -o ${CTS_PATH}

  # Report and commit any changes.
  git -C ${CTS_PATH} add data
  git -C ${CTS_PATH} status
  git -C ${CTS_PATH} commit -m "Updated from data commit ${commit}" && \
  git -C ${CTS_PATH} push

  # Stop logging commands.
  set +x

  # Log the time we finished running.
  echo "--- finish $(date -u) ---"

  # Wait until it's time to run the job again.
  sleep ${INTERVAL}

done # End of run loop.

# Log the final time.
echo "--- exit   $(date -u) ---"
