FROM python:3.8

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-dev \
    python3-distutils \
    curl

RUN pip install --upgrade pip && \
    pip install pip-tools~=6.0.1 

COPY requirements.in requirements.in
RUN pip-compile requirements.in -o requirements.txt &&  \
    pip install -r requirements.txt

WORKDIR /workdir