# Contrainer Image for My Project

## List

- [x] [Keycloak](./keycloak/) 
- [x] [Jupyter HUB](./juptyerhub/) 
- [x] [N8N Workflow](./n8n/) 
- [x] [Airflow](./airflow/)
- [x] [Superset](./superset/)

---

- [x] [minio.yaml](./minio-stack.yml)
- [x] [filebrowser.yaml](./filebrowser-stack.yml)
- [x] [docker-registry.yaml](./docker-registry.yml)


## Create User In Image

```dockerfile
LABEL maintainer="Attapon.TH <attapon.4work@gmail.com>"

ARG UNAME=attapon
RUN useradd --no-log-init --create-home --shell /bin/bash --uid "1000" --no-user-group "${UNAME}"
```
