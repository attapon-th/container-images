# JupyterHUB Multi-User with



# How to run
```bash
docker pull attap0n/jupyterhub:latest
docker pull quay.io/jupyter/scipy-notebook:python-3.11

docker network create --driver overlay --attachable jupyterhub_network

# use docker compose
# compose file: https://raw.githubusercontent.com/attapon-th/container-images/main/jupyterhub/jupyterhub/docker-compose.yml
docker compose up -d

# use docker swarm mode
# stack file: https://raw.githubusercontent.com/attapon-th/container-images/main/jupyterhub/jupyterhub/jupyterhub-stack.yml
# docker stack deploy -c jupyterhub-stack.yml jupyterhub
```


# URL:
[http://localhost:8000/jupyterhub](http://localhost:8000/jupyterhub)


# login 
> Username: admin
>
> Password: __first login is create new password__