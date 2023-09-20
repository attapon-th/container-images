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
# if you prefer Postgres, you may want to use `psycopg2-binary` instead
RUN pip install -U --no-cache-dir pip \
    pymysql psycopg2-binary \
    clickhouse-connect sqlalchemy-vertica-python

USER superset

COPY --chown=superset:superset --chmod=755 ./superset/docker/*.sh /app/docker/
COPY --chown=superset:superset --chmod=755 ./superset_config.py /app/pythonpath/superset_config.py

CMD ["/app/docker/docker-ci.sh"]