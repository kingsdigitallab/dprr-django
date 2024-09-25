# -----------------------------------------------------------------------------
# http://pythonhosted.org/django-auth-ldap/
# -----------------------------------------------------------------------------

import ldap
from django_auth_ldap.config import LDAPSearch, PosixGroupType

LDAP_BASE_DC = "dc=dighum,dc=kcl,dc=ac,dc=uk"
LDAP_BASE_OU = "ou=groups," + LDAP_BASE_DC

# Baseline configuration
AUTH_LDAP_SERVER_URI = "ldap://ldap1.cch.kcl.ac.uk"
AUTH_LDAP_BIND_DN = ""
AUTH_LDAP_BIND_PASSWORD = ""
AUTH_LDAP_USER_DN_TEMPLATE = "uid=%(user)s,ou=people," + LDAP_BASE_DC

# Set up the basic group parameters
AUTH_LDAP_GROUP_SEARCH = LDAPSearch(
    LDAP_BASE_OU, ldap.SCOPE_SUBTREE, "(objectClass=posixGroup)"
)
AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr="cn")

# Simple group restrictions
# TODO: Set this value in the project settings
AUTH_LDAP_REQUIRE_GROUP = ""

# Populate the Django user from the LDAP directory
AUTH_LDAP_USER_ATTR_MAP = {
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    "is_active": "cn=confluence-users," + LDAP_BASE_OU,
    "is_staff": "cn=ddh-staff," + LDAP_BASE_OU,
    "is_superuser": "cn=sysadmin," + LDAP_BASE_OU,
}

AUTH_LDAP_PROFILE_FLAGS_BY_GROUP = {}

# This is the default, but I like to be explicit
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

AUTHENTICATION_BACKENDS = (
    "django_auth_ldap.backend.LDAPBackend",
    "django.contrib.auth.backends.ModelBackend",
)
