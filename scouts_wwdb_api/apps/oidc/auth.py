from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from rest_framework import exceptions
from requests.exceptions import HTTPError
from pprint import pprint


class InuitsOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def update_user(self, user, claims):
        """Update existing user with new claims, if necessary save, and return user"""
        updated_user = self.map_user_with_claims(user, claims)
        updated_user.full_clean()
        updated_user.save()
        return updated_user

    def create_user(self, claims):
        """Return object for a newly created user account."""
        email = claims.get("email")
        username = self.get_username(claims)

        # Creating user like this because user is special
        user = self.UserModel.objects.create_user(username, email)
        # Then update user fields with claims
        user = self.map_user_with_claims(user, claims)
        user.full_clean()
        user.save()

        return user

    def map_user_with_claims(self, user, claims):
        if settings.OIDC_OP_USER_ENDPOINT.startswith("https://groepsadmin.scoutsengidsenvlaanderen.be"):
            return self.map_user_with_groepsadmin_claims(user, claims)
        else:
            return self.map_user_with_userinfo_claims(user, claims)

    def map_user_with_userinfo_claims(self, user, claims):
        user.first_name = claims.get("given_name", user.first_name)
        user.last_name = claims.get("family_name", user.last_name)

        roles = claims.get(settings.OIDC_RP_CLIENT_ID, {}).get("roles", [])
        user = self.map_user_roles(user, roles)
        return user

    def map_user_with_groepsadmin_claims(self, user, claims):

        user.first_name = claims.get("vgagegevens", {}).get("voornaam", user.first_name)
        user.last_name = claims.get("vgagegevens", {}).get("achternaam", user.last_name)

        # Everybody gets role user
        roles = ["role_user"]
        # give admin role if in one of the scouts groups
        scouts_groups = claims.get("functies", [])
        admin_scouts_groups = [
            "X0001G",
            "X0002G",
            "X0015G",
            "X1027G",
            "X0010G",
            "X0011G",
            "X0012G",
            "X0013G",
            "X0014G",
            "X0017G",
            "X0018G",
            "X0019G",
            "X0020G",
            "X0021G",
            "X0022G",
            "X0025G",
            "X0027G",
            "X0028G",
            "X0071G",
            "X0053G",
        ]
        for group in scouts_groups:
            if group.get("groep", "") in admin_scouts_groups and not group.get("einde", False):
                roles.append("role_admin")
                break
        user = self.map_user_roles(user, roles)
        return user

    def map_user_roles(self, user, claim_roles):
        # First clear all groups from user and set superuser false
        user.is_superuser = False
        user.groups.clear()
        for role in claim_roles:
            try:
                group = Group.objects.get(name=role)
                user.groups.add(group)
                # Set user super admin if role is super_admin
                if group.name == "role_super_admin":
                    user.is_superuser = True
            except ObjectDoesNotExist as exc:
                pass
        return user


class InuitsOIDCAuthentication(OIDCAuthentication):
    def authenticate(self, request):
        """
        Call parent authenticate but catch HTTPError 401 always even without www-authenticate
        """
        try:
            return super().authenticate(request)
        except HTTPError as exc:
            response = exc.response
            # If oidc returns 401 return auth failed error
            if response.status_code == 401:
                raise exceptions.AuthenticationFailed(response.json().get("error_description", response.text))

            raise
