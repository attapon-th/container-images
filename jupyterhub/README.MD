# Jupyter HUB on Docker Swarm


## 1. Setup Keycloak for Jupyter HUB

### [setup-keycloak.md](./setup-keycloak.md)


## 2. Deploy Jupyter HUB

- Create a network for the Jupyter HUB
    ```shell
    docker network create --driver overlay --attachable jupyterhub_swarm_network
    ```

- Create a volume for the Jupyter HUB
    ```shell
    docker volume create jupyterhub_data
    ```

- Deploy jupyter hub with docker stack
    >  docker compose stack file: 
    > > [`jupyterhub-stack.yml`](./jupyterhub-stack.yml) -- example jupyterhub localhost

    setup environment variables
    ```shell
    # follow environment variables
    # file: example.env
    #  -------- Env ----------
    HTTPS=http
    DOMAIN=localhost
    PREFIX=/jupyterhub
    CLIENT_ID=
    CLIENT_SECRET=
    CRYPT_KEY=changeme # (example random: openssl rand -base64 32)
    OPENID_URL=http://localhost:8080/auth/realms/master/.well-known/openid-configuration
    #  -------- END Env ----------
    ```

- Open Jupyter HUB in your browser
    ```shell
    http://localhost:8000/jupyterhub
