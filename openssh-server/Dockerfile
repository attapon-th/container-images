FROM lscr.io/linuxserver/openssh-server:latest

ENV TZ=Asia/Bangkok SUDO_ACCESS=false PUID=10000 PGID=10000

COPY ./sshd_config /etc/ssh/sshd_config

COPY ./update-pubkey.sh /usr/local/bin/update-pubkeys

RUN chmod +x /usr/local/bin/update-pubkeys