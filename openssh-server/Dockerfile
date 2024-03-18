FROM lscr.io/linuxserver/openssh-server:latest

ENV TZ=Asia/Bangkok \
    SUDO_ACCESS=false \
    PUID=10000 \
    PGID=10000 \
    LOG_STDOUT=true \
    LC_ALL="en_US.UTF-8" \
    LANG="en_US.UTF-8" \
    LANGUAGE="en_US.UTF-8"


RUN \
  echo "**** install runtime packages ****" && \
  apk add --no-cache --upgrade \
    tzdata \
    iputils-ping \
    locales \
    locales-all &&\
  rm -rf \
    /tmp/* \
    $HOME/.cache

WORKDIR /config

COPY ./sshd_config /etc/ssh/sshd_config
