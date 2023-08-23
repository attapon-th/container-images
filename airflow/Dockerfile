ARG AIRFLOW_VERSION AIRFLOW_UID=50000
FROM apache/airflow:${AIRFLOW_VERSION}
USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends git \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

#  for init-airflow.sh
ADD ./airflow/init-airflow.sh /init-airflow.sh
RUN chmod +x /init-airflow.sh && chown ${AIRFLOW_UID}:0 /init-airflow.sh \
  && mkdir -p /opt/airflow/logs /opt/airflow/dags /opt/airflow/plugins /opt/airflow/config \
  && chown -R "${AIRFLOW_UID}:0" /opt/airflow/{logs,dags,plugins} \
  && mkdir -p /sources/logs /sources/dags /sources/plugins \
  && chown -R "${AIRFLOW_UID}:0" /sources/{logs,dags,plugins}

USER 50000:0

RUN pip install --no-cache-dir -U pip \
    && pip install --no-cache-dir pandas pyarrow vertica-python pymysql psycopg2-binary \
    && pip install --no-cache-dir git+https://github.com/attapon-th/sqlalchemy-vertica-python.git

