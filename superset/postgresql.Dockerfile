FROM postgres:15

ENV TZ=Asia/Bangkok

COPY ./superset/docker/docker-entrypoint-initdb.d /docker-entrypoint-initdb.d