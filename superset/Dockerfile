ARG BASE_IMAGE=apache/superset
ARG VERSION=3.0.0
FROM ${BASE_IMAGE}:${VERSION}

ARG PYTHONPATH="/app/pythonpath"

ENV TZ=Asia/Bangkok \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 

# Switching to root to install the required packages
USER root
# Example: installing the MySQL driver to connect to the metadata database
COPY ./docker/requirements.txt /requirements.txt

RUN pip install -U --no-cache-dir pip \
    &  pip install  --no-cache-dir -r /requirements.txt

USER superset

COPY --chown=superset:superset --chmod=755 ./superset/docker/*.sh /app/docker/
COPY --chown=superset:superset --chmod=755 ./docker/superset_config.py /app/pythonpath/superset_config.py
COPY --chown=superset:superset --chmod=755 ./docker/keycloack_security_manager.py /app/pythonpath/keycloack_security_manager.py


CMD ["/app/docker/docker-ci.sh"]