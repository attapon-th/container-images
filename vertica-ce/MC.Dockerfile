ARG VERSION=23.4.0-0

FROM attap0n/vertica-ce:${VERSION} as builder

USER root
# install vertica console
ARG VERTICA_CONSOLE=vertica-console-12.0.4-0.x86_64.RHEL6.rpm
ENV VERTICA_CONSOLE=${VERTICA_CONSOLE}
ADD ./package/$VERTICA_CONSOLE /tmp/$VERTICA_CONSOLE

RUN rpm -Uvh -i /tmp/$VERTICA_CONSOLE
RUN sed -i 's/=\/webui/=\/vertica\/webui/' /opt/vconsole/config/console.properties


FROM attap0n/vertica-ce:${VERSION}

ENV TZ=Asia/Bangkok

USER root
COPY --from=builder /opt/vconsole /opt/vconsole

USER dbadmin

COPY --chmod=755 ./entrypoint/mcctl /home/dbadmin/bin/mcctl
ENV TZ=Asia/Bangkok
ENV PATH "/home/dbadmin/bin:$PATH"
ENV ENTRYPOINT_SCRIPT_PATH="/home/dbadmin/bin/mcctl"

ENTRYPOINT $ENTRYPOINT_SCRIPT_PATH

