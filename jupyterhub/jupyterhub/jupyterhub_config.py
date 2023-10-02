import os
import sys
import json
from urllib.request import urlopen, urljoin, quote
from oauthenticator import generic

c = get_config()  # noqa: F821



# ===========================================================================
#                            General Configuration
# ===========================================================================
jupyterhub_host = os.environ.get('JUPYTERHUB_HOST', "http://localhost:8000")
jupyterhub_prefix = os.environ.get('JUPYTERHUB_BASE_URL', "/")
c.JupyterHub.base_url = jupyterhub_prefix
# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_port = 8080



# ===========================================================================
#                         OAuthenticator Configuration
# ===========================================================================
c.JupyterHub.authenticator_class = generic.GenericOAuthenticator
# OAuth2 application info
# -----------------------
with urlopen(os.getenv("KEYCLOAK_OPENID_CONFIG_URL")) as f:
    wellknown = json.loads(f.read())

# issuer_url = wellknown_url.removesuffix("/.well-known/openid-configuration")

c.GenericOAuthenticator.login_service = "Keycloak"
c.GenericOAuthenticator.client_id = os.environ['OAUTH2_CLIENT_ID']
c.GenericOAuthenticator.client_secret = os.environ['OAUTH2_CLIENT_SECRET']
c.GenericOAuthenticator.validate_server_cert = os.getenv("OAUTH2_VALIDATE_SERVER_CERT", "True").lower() in ("true", "yes", "1")

# Identity provider info
# ----------------------
c.GenericOAuthenticator.authorize_url = wellknown.get("authorization_endpoint")
c.GenericOAuthenticator.token_url = wellknown.get("token_endpoint")
c.GenericOAuthenticator.userdata_url = wellknown.get("userinfo_endpoint")
c.GenericOAuthenticator.oauth_callback_url = os.getenv("OAUTH2_CALLBACK_URL", None) or "{}/{}/{}".format(jupyterhub_host.removesuffix("/"), jupyterhub_prefix.strip("/") ,"oauth_callback")
c.GenericOAuthenticator.logout_redirect_url = os.getenv("OAUTH2_LOGOUT_REDIRECT_URL", None) or "{}?post_logout_redirect_uri={}&client_id={}".format(
    wellknown.get("end_session_endpoint"),
    quote(urljoin(jupyterhub_host , c.JupyterHub.base_url)),
    quote(c.GenericOAuthenticator.client_id),
    )

# What we request about the user
# ------------------------------
c.GenericOAuthenticator.scope = os.environ.get("OAUTH2_SCOPE", "openid,roles").split(",")
c.GenericOAuthenticator.username_claim = os.environ.get("OAUTH2_USER_CLAIM", "preferred_username")
# c.GenericOAuthenticator.claim_groups_key = os.environ.get("OAUTH2_CLAIM_GROUPS_KEY", "resource_access.{}.roles".format(os.environ['OAUTH2_CLIENT_ID']))
c.GenericOAuthenticator.claim_groups_key = os.environ.get("OAUTH2_CLAIM_GROUPS_KEY", "roles")

# Group whitelisting
# -------------
c.GenericOAuthenticator.allowed_groups = set(os.environ.get("OAUTH2_ALLOWED_GROUPS", "user").split(","))
c.GenericOAuthenticator.admin_groups = set(os.environ.get("OAUTH2_ADMIN_GROUPS", "admin").split(","))

# ===========================================================================
#                         Spawner Configuration
# ===========================================================================
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
# Spawn containers from this image
c.DockerSpawner.image = os.environ.get("DOCKER_NOTEBOOK_IMAGE", "jupyter/scipy-notebook:latest")

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get("DOCKER_SPAWN_CMD", "start-singleuser.sh")
c.DockerSpawner.cmd = spawn_cmd

# Connect containers to this Docker network
network_name = os.environ["DOCKER_NETWORK_NAME"]
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name
# c.DockerSpawner.network_name = network_name
# c.DockerSpawner.extra_host_config = {'network_mode': network_name}
c.DockerSpawner.host_ip = "0.0.0.0"

# Explicitly set notebook directory because we'll be mounting a volume to it.
# Most `jupyter/docker-stacks` *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get("DOCKER_NOTEBOOK_DIR", "/home/jovyan/work")
c.DockerSpawner.notebook_dir = notebook_dir

share_dir = os.environ.get("DOCKER_SHARE_DIR", "/home/jovyan/share")

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {"jupyterhub-user-{username}": notebook_dir}

if share_dir != "":
    if not os.path.exists(share_dir):
        os.makedirs(share_dir)
        share_dir = os.path.realpath(share_dir)
        # os.chown(share_dir, 1000, 100)
        os.chmod(share_dir, 0o777)
    c.DockerSpawner.volumes["jupyterhub-public-share"] = share_dir


# Remove containers once they are stopped
c.DockerSpawner.remove = False

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = False

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"


# Resuource limits
c.DockerSpawner.cpu_guarantee = 1
c.DockerSpawner.mem_guarantee = "2G"
c.DockerSpawner.cpu_limit = os.environ.get("DOCKER_CPU_LIMIT", 2)
c.DockerSpawner.mem_limit = os.environ.get("DOCKER_MEM_LIMIT", "4G")




if os.environ.get("JUPYTERHUB_IDLE_CULLER_ENABLED", "1").lower() in ("true", "yes", "1"):
    c.JupyterHub.load_roles = [
        {
            "name": "server-rights",
            "scopes": [
                "list:users",
                "read:users:activity",
                "read:servers",
                "delete:servers",
                "admin:users", # if using --cull-users
            ]
        },
        {
            "name": "jupyterhub-idle-culler-role",
            "scopes": [
                "list:users",
                "read:users:activity",
                "read:servers",
                "delete:servers",
                "admin:users", # if using --cull-users
            ],
            # assignment of role's permissions to:
            "services": ["jupyterhub-idle-culler-service"],
        }
    ]



    c.JupyterHub.services = [
        {
            "name": "jupyterhub-idle-culler-service",
            "command": [
                sys.executable,
                "-m", "jupyterhub_idle_culler",
                "--timeout={}".format(os.environ.get("JUPYTERHUB_IDLE_CULLER_TIMEOUT", '3600')), #1HR
            ],
            # "admin": True,
        }
    ]