# Python version can be templatized
ARG PYTHON_VERSION=3.8
FROM python:$PYTHON_VERSION-slim

ARG SENTRY_SDK_VERSION=master

RUN apt-get update && apt-get install -y --no-install-recommends git

RUN pip install git+https://github.com/getsentry/sentry-python.git@${SENTRY_SDK_VERSION}

WORKDIR /work

COPY . .
