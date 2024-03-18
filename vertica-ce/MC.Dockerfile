ARG VERSION=23.4.0-0

FROM vertica/vertica-ce:${VERSION} as builder

USER root
# install vertica console
ARG VERTICA_CONSOLE=vertica-console-12.0.4-0.x86_64.RHEL6.rpm
ENV VERTICA_CONSOLE=${VERTICA_CONSOLE}
ADD ./package/$VERTICA_CONSOLE /tmp/$VERTICA_CONSOLE

RUN rpm -Uvh -i /tmp/$VERTICA_CONSOLE
RUN sed -i 's/=\/webui/=\/vertica\/webui/' /opt/vconsole/config/console.properties


FROM vertica/vertica-ce:${VERSION}

ENV TZ=Asia/Bangkok

USER root

ADD ./entrypoint/* /usr/local/bin/
COPY --from=builder /opt/vconsole /opt/vconsole

RUN chmod +x /usr/local/bin/verticactl \
    && chmod +x /usr/local/bin/mcctl \
    && rm /home/dbadmin/docker-entrypoint.sh

USER dbadmin

ENV VERTICA_SCRIPT_PATH=/opt/verticactl MC_SCRIPT_PATH=/opt/mcctl

ENTRYPOINT "/bin/sh" "-c" "verticactl"

