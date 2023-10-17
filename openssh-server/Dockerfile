FROM lscr.io/linuxserver/openssh-server:latest

ENV TZ=Asia/Bangkok SUDO_ACCESS=false PUID=10000 PGID=10000

WORKDIR /config

COPY ./sshd_config /etc/ssh/sshd_config
COPY ./update-pubkey.sh /config/update-pubkey

RUN chmod +x /config/update-pubkey