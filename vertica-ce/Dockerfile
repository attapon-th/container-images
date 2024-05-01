ARG VERSION=24.1.0-0
FROM vertica/vertica-ce:${VERSION}

ENV TZ=Asia/Bangkok

USER root

RUN yum update -y \
    && yum install -y git make tzdata python3.11 python3.11-pip gcc-c++ \
    && yum clean all \
    && rm -rf /var/cache/yum 

COPY --chmod=755 ./entrypoint/verticactl /home/dbadmin/verticactl
COPY --chmod=755 ./entrypoint/install_package /home/dbadmin/install_package

# RUN chmod +x /opt/vertica/bin/verticactl

USER dbadmin

ENV ENTRYPOINT_SCRIPT_PATH="/home/dbadmin/verticactl"

ENTRYPOINT $ENTRYPOINT_SCRIPT_PATH
