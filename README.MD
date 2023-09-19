# Contrainer Image for My Project

## List

- [x] [Jupyter HUB](./juptyerhub/) 
- [x] [N8N Workflow](./n8n/) 
- [ ] [Airflow](./airflow/)


## Create User In Image

```dockerfile
LABEL maintainer="Attapon.TH <attapon.4work@gmail.com>"

ARG UNAME=attapon
RUN useradd --no-log-init --create-home --shell /bin/bash --uid "1000" --no-user-group "${UNAME}"
```
