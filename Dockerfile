FROM ubuntu:23.04

RUN apt-get update \
    && apt-get install -yqq --no-install-recommends \
        python3.11 \
        python3-venv \
        python3-pip \
        pipx \
        wget \
        unzip \
        nano \
        git \
        build-essential \
        ca-certificates \
        curl \
        gnupg \
        lsb-release \
        jq \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /root/src

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt --break-system-packages

COPY resources resources

COPY pysurfer pysurfer
COPY pipeline.py pipeline.py
COPY pipeline.sh pipeline.sh

ENTRYPOINT ["bash", "pipeline.sh"]
