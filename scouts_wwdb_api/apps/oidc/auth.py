from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from pprint import pprint


class InuitsOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def update_user(self, user, claims):
        """Update existing user with new claims, if necessary save, and return user"""
        updated_user = self.map_user_with_claims(user, claims)
        updated_user.full_clean()
        updated_user.save()
        pprint(updated_user.__dict__)
        return updated_user

    def create_user(self, claims):
        """Return object for a newly created user account."""
        email = claims.get("email")
        username = self.get_username(claims)

        return self.UserModel.objects.create_user(username, email)

    def map_user_with_claims(self, user, claims):
        user.first_name = claims.get("given_name", user.first_name)
        user.last_name = claims.get("family_name", user.last_name)
        return user
