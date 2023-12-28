# Docker Images  (All projects is reverse proxy with traefik 2.x)

> this docker images are created for `Docker stack`
>


## Project Support (Required)

1. [traefik-setup](https://github.com/attapon-th/traefik-setup)  
2. [portainer](https://github.com/attapon-th/portainer)
3. [taskfile.dev](https://taskfile.dev/) - (help command line)

## List

- [x] [Keycloak](./keycloak/) 
- [x] [JupyterHub](./juptyerhub/) 
- [x] [N8N Workflow](./n8n/) 
- [x] [Superset](./superset/)
- [x] [Cronicle v0.9.39](./cronicle/)
- [x] [Docker Registry v2](./docker-registry/)
- [x] [Minio](./minio/)
- [x] [Filebrowser](./filebrowser/)
- [x] [Openssh-server](./openssh-server/)
- [x] [Vertica CE Standalone v.23.4.0](./vertica-ce/)


## How to Deploy with Portainer

> request `docker swarm` mode
>
> request `portainer` to be installed
>
> request `docker-compose` to be installed
>

1. Use deploy docker stack with portainer ui  

<img src="./imgs/add-starck.png" width="500px">  

2. config with `docker compose` version: 3


<img src="./imgs/example-stack.png" width="500px"> 


