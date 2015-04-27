import os
from fnmatch import fnmatch
from django.conf import global_settings
from django.core.urlresolvers import reverse_lazy
from django.contrib.messages import constants as messages
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP, LOGGING, AUTHENTICATION_BACKENDS
from varlet import variable
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError: # pragma: no cover
    pass

here = lambda *path: os.path.normpath(os.path.join(os.path.dirname(__file__), *path))
ROOT = lambda *path: here("../../", *path)

DEBUG = variable("DEBUG", default=False)
TEMPLATE_DEBUG = DEBUG

# Redirects users upon login/logout to main question list page
#LOGIN_URL = reverse_lazy("questions-list")
#LOGIN_REDIRECT_URL = reverse_lazy("questions-list")
#LOGOUT_URL = reverse_lazy("questions-list")


# [LDAP Settings]
# if you're having trouble connecting to LDAP set this to True so you can login
# to track, bypassing LDAP group checks
LDAP_DISABLED = variable("LDAP_DISABLED", default=False)

LDAP = {
    'default': {
        'host': "ldap://ldap-login.oit.pdx.edu",
        'username': 'iq',
        'password': '',
        'search_dn': 'dc=pdx,dc=edu'
    }
}

ADMINS = variable("ADMINS", [])
MANAGERS = ADMINS

# [MYSQL Settings]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'iq',           # variable("DB_NAME", 'iq'),
        'USER': 'root',         # variable("DB_USER", 'root'),
        'PASSWORD': '',         # variable("DB_PASSWORD", 'vagrant'),
        'HOST': '',             # variable("DB_HOST", ''),
        'PORT': '',
    }
}

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# Allow the use of wildcards in the INTERAL_IPS setting
class IPList(list):
    # do a unix-like glob match
    # E.g. '192.168.1.100' would match '192.*'
    def __contains__(self, ip): # pragma: no cover
        for ip_pattern in self:
            if fnmatch(ip, ip_pattern):
                return True
        return False

INTERNAL_IPS = IPList(['10.*', '192.168.*'])

# [CAS Settings]
# for django-cas to work, it needs HttpRequest.get_host(), which requires this setting
# https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['.pdx.edu']
CAS_SERVER_URL = 'https://sso.pdx.edu/cas/login'
CAS_ADMIN_PREFIX = '/admin/'
CAS_AUTO_CREATE_USERS = True


INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'arcutils',
    'iq',
    'iq.categories',
    'iq.categories.templatetags',
    'iq.questions',
    'iq.tags',
    'iq.utils',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'djangocas.middleware.CASMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'iq.backends.PSUBackend',
)

ROOT_URLCONF = 'iq.urls'

WSGI_APPLICATION = 'iq.wsgi.application'

# [Internationalization]
# https://docs.djangoproject.com/en/1.6/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = False

USE_L10N = False

USE_TZ = True

# [Static files]
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'

STATIC_ROOT = ROOT("static")

STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    here("static"),
)

MEDIA_URL = '/media/'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"

MEDIA_ROOT = ROOT("media")

TMP_ROOT = ROOT("tmp")

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    here("templates"),
    #ROOT("iq", "templates"),
)

SECRET_KEY = variable("SECRET_KEY", default=os.urandom(64).decode("latin1"))
