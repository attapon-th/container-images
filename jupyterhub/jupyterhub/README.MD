# JupyterHUB Multiuser






# How to run
```bash
docker pull attap0n/jupyterhub:latest
docker pull quay.io/jupyter/scipy-notebook:python-3.11

docker network create --driver overlay --attachable jupyterhub_network

# use docker compose
docker compose up -d

# use docker swarm mode
# docker stack deploy -c jupyterhub-stack.yml jupyterhub
```


# URL:

[http://localhost:8000/jupyterhub](http://localhost:8000/jupyterhub)