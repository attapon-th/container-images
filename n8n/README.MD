# N8N Workflow (no code)

> N8N is a workflow automation tool. It helps you to automate workflows, so you can focus on real work.

## Deploy Summary of N8N Workflow

> for docker swarm and production mode
> 
> 1 main n8n
> 
> 2 worker 1 webhook (can scale up)
>
> 1 postgresql
>
> 1 redis (for queue mode)
> 
> 1 traefik (for reverse proxy)

### Requirements

- docker
- docker swarm
- docker network
  - `n8n` สำหรับใช้งานร่วมกับ n8n ในการทำ internal network
  - `proxy` สำหรับใช้งานร่วมกับ traefik ในการทำ reverse proxy


### Image Use
- `n8nio/n8n:latest` (test with version 1.1.1)
- `bitnami/postgresql:15` postgresql 15
- `redis:latest` redis last version


### Edit `default.env` and rename to `.env`
```dotenv
POSTGRES_PASSWORD=postgress-password-change-me
N8N_PROTOCOL=http
N8N_HOST=127.0.0.1
N8N_PATH=/n8n
WEBHOOK_URL=http://127.0.0.1/n8n/
N8N_ENCRYPTION_KEY=randomkey-change-me
```


### Deploy

> deploy file: [n8n-stack.yml](./n8n-stack.yml)
> 


```shell
docker stack deploy -c n8n-stack.yml n8n
```
