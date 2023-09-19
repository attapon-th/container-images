FROM apache/superset

ENV TZ=Asia/Bangkok

# Switching to root to install the required packages
USER root
# Example: installing the MySQL driver to connect to the metadata database
# if you prefer Postgres, you may want to use `psycopg2-binary` instead
RUN pip install -U --no-cache-dir pip pymysql 

USER superset