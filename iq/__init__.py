from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
# uncomment to use celery
# from .celery import app as celery_app

# User/Group Permissions
LOGIN_GROUPS = ("arc", "arcsystems", "arcstaff")
STAFF_GROUP = "arcstaff"
