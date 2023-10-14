# Setup Keycloak for jupyter hub


## Create Client for Jupyter hub 

  - Create Client   
  - <img width="600px" src="./images/keycloak-create-client.png" />
  - 
  - Create Client name
  -  <img width="600px" src="./images/keycloak-create-client-input.png" />
  -  
  - Turn on client authentication   
  - <img width="600px" src="./images/keycloak-capability.png" />
  - 
  - Setup Valid Redirect URIs  
  - <img width="600px" src="./images/keycloak-validate-url.png" />  
  - Valid redirect URIs: `*`
  - Valid post logout redirect URIs: `*`
  - 
  - Get ClientID and Client Secret (Page: `Clients > Client details`)
    - client_id: `my-jupyter`
    - client_secret: get from tab `Credentials` in field `Client secret`  
  - <img width="600px" src="./images/keycloak-copy-client-secret.png" />

- Get KEYCLOAK_OPENID_CONFIG_URL  
- <img width="600px" src="./images/keycloak-get-openid-config.png" />


## Create `Role` and `Scope`

- Create Client Role for Jupyter hub Role (`jupyter-user` and `jupyter-admin`)
- <img width="600px" src="./images/keycloak-roles.png" />


- Create `Scope`
- <img width="600px" src="./images/keycloak-ht-create-client-scope.png" />

- Create Client role name: `client_roles`
- <img width="600px" src="./images/keycloak-create-client_role.png" />


- Add Mapper Roles for `client_roles`
- <img width="600px" src="./images/keycloak-add-mappers.png" />


- Add Mapper Roles
- <img width="600px" src="./images/keycloak-select-user-client-role.png" />  
- <img width="600px" src="./images/keycloak-setup-user-client-role.png" />


- Add scopes `client_roles` to `client`
- <img width="600px" src="./images/keycloak-add-scopes.png" />
- <img width="600px" src="./images/keycloak-confirm.png" />


# Success Config keycloak