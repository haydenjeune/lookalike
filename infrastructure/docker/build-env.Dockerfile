FROM python:3.8.12 AS build-env

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    python3-distutils \
    curl

RUN pip install --upgrade pip && \
    pip install pip-tools~=6.0.1 

ENTRYPOINT [ "/bin/sh", "-c" ]