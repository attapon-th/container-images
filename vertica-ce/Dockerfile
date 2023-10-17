FROM vertica/vertica-ce:23.3.0-0

ENV TZ=Asia/Bangkok

USER root

COPY docker-entrypoint.sh /home/dbadmin/docker-entrypoint.sh

RUN chmod +x /home/dbadmin/docker-entrypoint.sh \
    && chown dbadmin /home/dbadmin/docker-entrypoint.sh
    
USER dbadmin
