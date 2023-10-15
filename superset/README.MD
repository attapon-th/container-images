# Superset with Keycloak Authentication


## Deployment

> use **[superset-stack.yml](./superset-stack.yml)** for deployment
>
> and edit config for your server with file **[example.env](./example.env)**
>

## Superset Roles and Keycloak Roles

| Superset Role | Keycloak Roles                       | Description                                                |
| ------------- | ------------------------------------ | ---------------------------------------------------------- |
| Admin         | `superset-admin`                     | Admins have all possible rights                            |
| Alpha         | `superset-alpha`, `superset-editor`  | Alpha users have access to all data sources                |
| Gamma         | `superset-gamma`                     | Gamma users have limited access.                           |
| Public        | `superset-public`, `superset-viewer` | To allow logged-out users to access some Superset features |
| sql_lab       | `superset-sql_lab`                   | The sql_lab role grants access to SQL Lab                  |
