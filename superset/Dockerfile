ARG BASE_IMAGE=apache/superset
ARG VERSION=3.1.0
FROM ${BASE_IMAGE}:${VERSION}

ARG PYTHONPATH="/app/pythonpath"

ENV TZ=Asia/Bangkok \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 

# Switching to root to install the required packages
USER root
# Example: installing the MySQL driver to connect to the metadata database
COPY ./docker/requirements.txt /requirements.txt

RUN apt-get update \
    && apt-get install -y --no-install-recommends git curl wget tzdata \
    && apt-get autoremove -yqq --purge \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -U --no-cache-dir pip \
    && pip install  --no-cache-dir -r /requirements.txt

USER superset

COPY --chown=superset:superset --chmod=755 ./docker/*.sh /app/docker/
COPY --chown=superset:superset --chmod=755 ./docker/*.py /app/pythonpath/


CMD ["/app/docker/docker-ci.sh"]