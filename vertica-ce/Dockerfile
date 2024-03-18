ARG VERSION=24.1.0-0
FROM vertica/vertica-ce:${VERSION}

ENV TZ=Asia/Bangkok

USER root

ADD ./entrypoint/* /usr/local/bin/

RUN chmod +x /usr/local/bin/verticactl \
    && rm /home/dbadmin/docker-entrypoint.sh

USER dbadmin

ENV VERTICA_SCRIPT_PATH=/opt/verticactl MC_SCRIPT_PATH=/opt/mcctl

ENTRYPOINT "/bin/sh" "-c" "verticactl"

