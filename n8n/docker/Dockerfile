ARG N8N_VERSION=latest
FROM n8nio/n8n:${N8N_VERSION}


ENV TZ=Asia/Bangkok

USER root

RUN apk update \
    && apk add --no-cache docker-cli \
    && rm -rf /var/cache/apk/*

# default group docker is gid 2375
# change if your server gid is not 2375
RUN addgroup -g 2375 -S docker && addgroup node docker

USER node
# COPY docker/docker-entrypoint.sh /docker-entrypoint.sh

# ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]