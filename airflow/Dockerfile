ARG AIRFLOW_VERSION
FROM apache/airflow:${AIRFLOW_VERSION}
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends git \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

USER 50000:0

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir pandas pyarrow vertica-python pymysql psycopg2-binary \
    && pip install --no-cache-dir git+https://github.com/attapon-th/sqlalchemy-vertica-python.git