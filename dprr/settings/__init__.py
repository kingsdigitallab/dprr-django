# -----------------------------------------------------------------------------
# Import the settings here according to the environment. Options are dev, stg,
# and liv.
#
# If a local settings file is present (local.py), it will override the settings
# imported here. Use it for settings specific to the installation and do not
# commit to version control.
# -----------------------------------------------------------------------------
import os
path = os.getcwd()

if '/dev/' in path or '/vagrant' in path:
    from dev import *  # noqa
elif 'stg' in path:
    from stg import *  # noqa
else:
    from liv import *  # noqa