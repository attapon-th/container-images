from math import log
from superset.security import SupersetSecurityManager
import logging
from flask_appbuilder.security.views import AuthOAuthView
from flask_appbuilder.baseviews import expose
import time
from flask import redirect


class CustomAuthOAuthView(AuthOAuthView):

    @expose("/logout/")
    def logout(self, provider="keycloak", register=None):
        provider_obj = self.appbuilder.sm.oauth_remotes[provider]
        url = ("logout?client_id={}&post_logout_redirect_uri={}".format(
            provider_obj.client_id,
            provider_obj.server_metadata.get('logout_redirect_uri')
        ))

        ret = super().logout()
        time.sleep(1)

        return redirect("{}{}".format(provider_obj.api_base_url, url))


class CustomSecurityManager(SupersetSecurityManager):
    # override the logout function
    authoauthview = CustomAuthOAuthView

    def oauth_user_info(self, provider, response=None):
        logging.debug("Oauth2 provider: {0}.".format(provider))
        if provider == 'keycloak':
            # superset_roles: list[str] = ["Admin", "Alpha", "Gamma", "Public", "granter", "sql_lab"]
            me = self.appbuilder.sm.oauth_remotes[provider].get('userinfo').json()
            roles = ["public", ]
            if "roles" in me:
                role_prefix = "superset-"
                roles = [r[len(role_prefix):].lower() for r in me.get("roles", []) if r.startswith(role_prefix)]

            return {
                "username": me.get("preferred_username", ""),
                "first_name": me.get("given_name", ""),
                "last_name": me.get("family_name", ""),
                "email": me.get("email", ""),
                "role_keys": roles,
            }
        return {}
