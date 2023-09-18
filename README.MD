# Contrainer Image for My Project

## List

- [x] [Jupyter HUB](./juptyerhub/) 
- [x] [N8N Workflow](./n8n/) 
- [ ] [Airflow](./airflow/)


## Create User In Image

```dockerfile
LABEL image.authors="Attapon.TH <attapon.4work@gmail.com>"

ENV UNAME=attapon
RUN groupadd --gid 1000 $UNAME && useradd --uid 1000 --gid $UNAME --shell /bin/sh --create-home $UNAME
```
