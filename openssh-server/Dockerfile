FROM lscr.io/linuxserver/openssh-server:latest

ENV TZ=Asia/Bangkok SUDO_ACCESS=false PUID=10000 PGID=10000

COPY ./sshd_config /etc/ssh/sshd_config

# ENV 
# RUN mkdir -p /config/pubkeys