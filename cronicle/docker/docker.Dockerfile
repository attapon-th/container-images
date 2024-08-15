FROM       docker:latest
ARG        CRONICLE_VERSION

LABEL      maintainer="Attapon.TH <https://github.com/attapon-th>"

# Docker defaults
ENV        CRONICLE_VERSION ${CRONICLE_VERSION}
ENV        CRONICLE_base_app_url 'http://localhost:3012'
ENV        CRONICLE_WebServer__http_port 3012
ENV        CRONICLE_WebServer__https_port 3012
ENV        EDITOR=vim
ENV        PYTHONUNBUFFERED=1
ENV        TZ=Asia/Bangkok


RUN        apk add --no-cache nodejs npm git curl wget perl bash perl-pathtools tar procps vim tini python3 py3-pip tzdata
RUN        mkdir -p /opt/cronicle \
    && cd /opt/cronicle \
    && curl -L https://github.com/jhuckaby/Cronicle/archive/${CRONICLE_VERSION}.tar.gz | tar zxvf - --strip-components 1 \
    && npm install \
    && node bin/build.js dist \
    && rm -Rf /root/.npm

RUN  pip3 install --no-cache-dir --upgrade pip --break-system-packages \
    && pip3 install --no-cache-dir --break-system-packages docker 


WORKDIR    /opt/cronicle/
ADD        entrypoint/entrypoint.sh /entrypoint.sh
ADD        ./plugins/*.py ./bin/
ADD        config/*.pixl ./import/

EXPOSE     3012

# data volume is also configured in entrypoint.sh
VOLUME     ["/opt/cronicle/data", "/opt/cronicle/logs", "/opt/cronicle/plugins"]

ENTRYPOINT ["/sbin/tini", "--"]
CMD        ["sh", "/entrypoint.sh"]