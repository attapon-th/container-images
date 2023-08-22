ARG AIRFLOW_VERSION
FROM apache/airflow:${AIRFLOW_VERSION}
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends git \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

#  for init-airflow.sh
ADD ./airflow/init-airflow.sh /init-airflow.sh
RUN chmod +x /init-airflow.sh && chown 50000:0 /init-airflow.sh

USER 50000:0

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir pandas pyarrow vertica-python pymysql psycopg2-binary \
    && pip install --no-cache-dir git+https://github.com/attapon-th/sqlalchemy-vertica-python.git

