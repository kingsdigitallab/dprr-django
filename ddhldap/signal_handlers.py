from django_auth_ldap.backend import populate_user


def populate_user_signal_handler(user, ldap_user, **kwargs):
    # Converts the user to an LDAP user
    user.set_unusable_password()


def register_signal_handlers():
    populate_user.connect(populate_user_signal_handler)
