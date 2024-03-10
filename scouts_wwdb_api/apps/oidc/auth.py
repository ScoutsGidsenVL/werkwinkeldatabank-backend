"""apps.oidc.auth."""
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from requests.exceptions import HTTPError
from rest_framework import exceptions


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
            "X0001G",  # PCOM
            "X0002G",  # BCOM
            "X0010G",  # Kapoenen
            "X0011G",  # Welpen
            "X0012G",  # Jgvs
            "X0013G",  # Givers
            "X0014G",  # Jins
            "X0015G",  # Vorming
            "X0017G",  # Internationaal
            "X0018G",  # Akabe
            "X0019G",  # Zingeving
            "X0020G",  # Diversiteit
            "X0021G",  # Zeescouts
            "X0022G",  # Groepsleiding
            "X0025G",  # Jamboree
            "X0027G",  # Touwenparcours
            "X0028G",  # Technieken
            "X0053G",  # Vormingsbegeleiding
            "X0056G",  # Ecologie
            "X0057G",  # Lokalen
            "X0059G",  # Structurenteam
            "X0071G",  # Integriteam
            "X1027G",  # Personeel NS
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
