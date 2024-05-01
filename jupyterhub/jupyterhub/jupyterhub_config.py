import os
import sys


c = get_config()  # noqa: F821

c.NotebookApp.iopub_data_rate_limit=1.0e10

c.JupyterHub.authenticator_class = "firstuseauthenticator.FirstUseAuthenticator"
c.FirstUseAuthenticator.dbm_path = "/data/passwd.dbm"
c.FirstUseAuthenticator.create_users = False
c.Authenticator.admin_users = set(os.getenv("JUPYTERHUB_ADMIN_USERS", "admin").split(","))
# c.Authenticator.allowed_users = {"user1", "user2", "user3"}

# ===========================================================================
#                            General Configuration
# ===========================================================================
jupyterhub_host = os.environ.get("JUPYTERHUB_HOST", "http://localhost:8000")
jupyterhub_prefix = os.environ.get("JUPYTERHUB_BASE_URL", "/")
c.JupyterHub.base_url = jupyterhub_prefix
# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = "0.0.0.0"
c.JupyterHub.hub_port = 8080


# ===========================================================================
#                         Spawner Configuration
# ===========================================================================
c.JupyterHub.spawner_class = "dockerspawner.DockerSpawner"
# Spawn containers from this image
c.DockerSpawner.image = os.environ.get(
    "DOCKER_NOTEBOOK_IMAGE", "jupyter/scipy-notebook:latest"
)

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
c.DockerSpawner.notebook_dir = "/home/jovyan"

share_dir = os.environ.get("DOCKER_SHARE_DIR", "/home/jovyan/share")


# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = {
    "jupyterhub-user-{username}": notebook_dir,
    "jupyterlab-site-package": "/home/jovyan/.local/lib"
                           }

if share_dir != "":
    if not os.path.exists(share_dir):
        os.makedirs(share_dir)
        share_dir = os.path.realpath(share_dir)
        # os.chown(share_dir, 1000, 100)
        os.chmod(share_dir, 0o777)
    c.DockerSpawner.volumes["jupyterhub-public-share"] = share_dir


# Remove containers once they are stopped
c.DockerSpawner.remove = os.getenv("JUPYTERHUB_REMOVE_CONTAINERS", "0").lower() in ("1", "true", "yes")

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = False

# Persist hub data on volume mounted inside container
c.JupyterHub.cookie_secret_file = "/data/jupyterhub_cookie_secret"
c.JupyterHub.db_url = "sqlite:////data/jupyterhub.sqlite"


# Resuource limits
c.DockerSpawner.cpu_guarantee = 1
c.DockerSpawner.mem_guarantee = "2G"
# c.DockerSpawner.cpu_limit = os.environ.get("DOCKER_CPU_LIMIT", 2)
# c.DockerSpawner.mem_limit = os.environ.get("DOCKER_MEM_LIMIT", "4G")


if os.environ.get("JUPYTERHUB_IDLE_CULLER_ENABLED", "1").lower() in (
    "true",
    "yes",
    "1",
):
    c.JupyterHub.load_roles = [
        {
            "name": "server-rights",
            "scopes": [
                "list:users",
                "read:users:activity",
                "read:servers",
                "delete:servers",
                "admin:users",  # if using --cull-users
            ],
        },
        {
            "name": "jupyterhub-idle-culler-role",
            "scopes": [
                "list:users",
                "read:users:activity",
                "read:servers",
                "delete:servers",
                "admin:users",  # if using --cull-users
            ],
            # assignment of role's permissions to:
            "services": ["jupyterhub-idle-culler-service"],
        },
    ]

    c.JupyterHub.services = [
        {
            "name": "jupyterhub-idle-culler-service",
            "command": [
                sys.executable,
                "-m",
                "jupyterhub_idle_culler",
                "--timeout={}".format(
                    os.environ.get("JUPYTERHUB_IDLE_CULLER_TIMEOUT", "3600")
                ),  # 1HR
            ],
            # "admin": True,
        }
    ]
