FROM jupyterhub/jupyterhub:latest

ENV PYTHONUNBUFFERED=1 TZ=Asia/Bangkok

COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

RUN pip install --no-cache-dir \
    oauthenticator \
    jupyterhub-idle-culler \
    dockerspawner

