FROM python:3.7-alpine

# Install pipenv for dependency management.
RUN pip install pipenv

# Work in the default python container source location.
WORKDIR /usr/src/app

# Install git for repo access.
RUN apk add git

# Install ssh for deploying updates.
RUN apk add openssh-client
RUN ssh -o 'StrictHostKeyChecking no' -N git@github.com || true

# Setup runtime.
RUN git clone https://github.com/cdli-gh/atf2tei
RUN pipenv install pyoracc

# Copy source.
ADD cdli2cts.py .
ADD cdli.py .
ADD run.sh .

CMD ./run.sh --setup
