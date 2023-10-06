import logging
import os

from celery.schedules import crontab
from flask_appbuilder.security.manager import AUTH_OAUTH
from security_manager import CustomSecurityManager
from urllib.request import urlopen, urljoin, quote
import json

logger: logging.Logger = logging.getLogger()

SECRET_KEY = os.getenv("SUPERSET_SECRET_KEY")

FEATURE_FLAGS = {"ALERT_REPORTS": True}
ALERT_REPORTS_NOTIFICATION_DRY_RUN = False


WEBDRIVER_BASEURL = "http://superset:8088/"
WEBDRIVER_BASEURL_USER_FRIENDLY = WEBDRIVER_BASEURL

#  ROW Config
SQLLAB_CTAS_NO_LIMIT = False
ROW_LIMIT = 5000

ENABLE_PROXY_FIX = True
# PROXY_FIX_CONFIG = {"x_for": 1, "x_proto": 1, "x_host": 1, "x_port": 0, "x_prefix": 1}


# Flask-WTF flag for CSRF
WTF_CSRF_ENABLED = True
# Add endpoints that need to be exempt from CSRF protection
WTF_CSRF_EXEMPT_LIST = []
# A CSRF token that expires in 1 year
WTF_CSRF_TIME_LIMIT = 60 * 60 * 24 * 365


# ===========================================================================
#                         Database Configuration
# ===========================================================================
DATABASE_DIALECT: str = os.getenv("DATABASE_DIALECT", 'postgresql+psycopg2')
DATABASE_USER: str = os.getenv("DATABASE_USER", 'superset')
DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", 'superset')
DATABASE_HOST: str = os.getenv("DATABASE_HOST", 'db')
DATABASE_PORT: str = os.getenv("DATABASE_PORT", '5432')
DATABASE_DB: str = os.getenv("DATABASE_DB", 'superset')


# ===========================================================================
#                         Cache Configuration
# ===========================================================================
# '''
# ---------------------------Use Redis ----------------------------
# '''
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CELERY_DB = os.getenv("REDIS_CELERY_DB", "0")
REDIS_RESULTS_DB = os.getenv("REDIS_RESULTS_DB", "1")
REDIS_RESULTS_BACKEND = os.getenv("REDIS_RESULTS_DB", "3")
REDIS_FILTER_STATE = os.getenv("REDIS_RESULTS_DB", "4")
REDIS_FORM_DATA = os.getenv("REDIS_RESULTS_DB", "5")

# 1
CACHE_CONFIG = {
    "CACHE_TYPE": "RedisCache",
    "CACHE_DEFAULT_TIMEOUT": 300,
    "CACHE_KEY_PREFIX": "superset_rs",
    "CACHE_REDIS_HOST": REDIS_HOST,
    "CACHE_REDIS_PORT": REDIS_PORT,
    "CACHE_REDIS_DB": REDIS_RESULTS_DB,
}
# 2
DATA_CACHE_CONFIG = CACHE_CONFIG
# 3
RESULTS_BACKEND = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 3600,
    'CACHE_KEY_PREFIX': 'superset_be_',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_BACKEND}'
}
# 4
FILTER_STATE_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,  # 1 day
    'CACHE_KEY_PREFIX': 'superset_fc_',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_FILTER_STATE}'
}
# 5
EXPLORE_FORM_DATA_CACHE_CONFIG = {
    'CACHE_TYPE': 'RedisCache',
    'CACHE_DEFAULT_TIMEOUT': 86400,  # 1 day
    'CACHE_KEY_PREFIX': 'superset_fd_',
    'CACHE_REDIS_URL': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_FORM_DATA}'
}


class CeleryConfig:
    broker_url = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
    imports = ("superset.sql_lab",)
    result_backend = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_RESULTS_DB}"
    worker_prefetch_multiplier = 1
    task_acks_late = False
    beat_schedule = {
        "reports.scheduler": {
            "task": "reports.scheduler",
            "schedule": crontab(minute="*", hour="*"),
        },
        "reports.prune_log": {
            "task": "reports.prune_log",
            "schedule": crontab(minute=10, hour=0),
        },
    }


CELERY_CONFIG = CeleryConfig
# ===========================================================================
#                         Cache END
# ===========================================================================


#
# Optionally import superset_config_docker.py (which will have been included on
# the PYTHONPATH) in order to allow for local settings to be overridden
#
try:
    import superset_config_docker
    from superset_config_docker import *  # noqa

    logger.info(
        f"Loaded your Docker configuration at " f"[{superset_config_docker.__file__}]"
    )
except ImportError:
    logger.info("Using default Docker config...")


# ===========================================================================
#                         OAuthenticator Configuration
# ===========================================================================
# Set the authentication type to OAuth
# openid_config_url: str = os.getenv("KEYCLOAK_OPENID_CONFIG_URL", "")
# with urlopen(openid_config_url) as f:
#     wellknown = json.loads(f.read())
# '''
# ---------------------------KEYCLOACK ----------------------------
# '''
AUTH_TYPE = AUTH_OAUTH
# ["Admin", "Alpha", "Gamma", "Public", "granter", "sql_lab"]
AUTH_ROLES_MAPPING = {
    "admin": ["Admin"],
    "alpha": ["Alpha"],
    "editor": ["Alpha"],
    "gamma": ["Gamma"],
    "public": ["Public"],
    "viewer": ["Public"],
    "sql_lab": ["sql_lab"],
}
# AUTH_ROLES_SYNC_AT_LOGIN = False
AUTH_ROLES_SYNC_AT_LOGIN = True
AUTH_USER_REGISTRATION = True
AUTH_USER_REGISTRATION_ROLE = "Public"
CUSTOM_SECURITY_MANAGER = CustomSecurityManager
# LOGOUT_REDIRECT_URL = ''
OAUTH_PROVIDERS = [
    {
        'name': 'keycloak',
        'token_key': 'access_token',  # Name of the token in the response of access_token_url
        'icon': 'fa-key',   # Icon for the provider
        'remote_app': {
            'client_id': os.environ.get("KEYCLOAK_CLIENT_ID"),  # Client Id (Identify Superset application)
            'client_secret': os.environ.get("KEYCLOAK_CLIENT_SECRET"),  # Secret for this Client Id (Identify Superset application)
            'api_base_url': os.environ.get("KEYCLOAK_ISSUER").rstrip('/') + "/protocol/openid-connect/",
            'client_kwargs': {
                'scope': 'openid profile email',
            },
            'logout_redirect_uri': os.environ.get("KEYCLOAK_LOGOUT_REDIRECT_URL"),
            'server_metadata_url': os.environ.get("KEYCLOAK_ISSUER").rstrip('/') + '/.well-known/openid-configuration',  # URL to get metadata from
        }
    }
]
