"""
Django settings for sharemyhealth project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import dj_database_url
from django.contrib.messages import constants as messages
from getenv import env
from django.utils.translation import ugettext_lazy as _

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '@+ttixefm9-bu1eknb4k^5dj(f1z0^97b$zan9akdr^4s8cc54'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*', ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'rest_framework',
    'apps.home',
    'apps.wellknown',
    'apps.verifymyidentity',
    'apps.accounts',
    'apps.testclient',
    'apps.api',  # Dummy CDA App for now
    'apps.fhirproxy',
    'apps.hixny',
    # 3rd Party ---------------------
    'corsheaders',
    'bootstrapform',
    'social_django',  # Python Social Auth
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]


ROOT_URLCONF = 'sharemyhealth.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django_settings_export.settings_export',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'sharemyhealth.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        default=env('DATABASES_CUSTOM',
                    'sqlite:///{}/db.sqlite3'.format(BASE_DIR))
    ),
}

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'UserAttributeSimilarityValidator')
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'MinimumLengthValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'CommonPasswordValidator'),
    },
    {
        'NAME': ('django.contrib.auth.password_validation.'
                 'NumericPasswordValidator'),
    },
]

LOGOUT_REDIRECT_URL = 'home'


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'sitestatic'),
]

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'collectedstatic')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

APPLICATION_TITLE = "HIXNY FHIR Server"

# AWS Credentials need to support SES, SQS and SNS
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID', 'change-me')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY', 'change-me')


AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOpenId',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.google_openidconnect.GoogleOpenIdConnect',
    'social_core.backends.instagram.InstagramOAuth2',
    'apps.verifymyidentity.authentication.SocialCoreOpenIdConnect',
    'django.contrib.auth.backends.ModelBackend',

)

CORS_ORIGIN_ALLOW_ALL = True

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.mail.mail_validation',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'apps.accounts.pipeline.oidc.save_profile',
    'social_core.pipeline.debug.debug'
)

SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_KEY = env(
    'SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_KEY',
    'sharemyhealth')
SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_SECRET = env(
    'SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_SECRET',
    'sharemyhealth-secret-change-me')
SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_SCOPE = ['openid', ]
SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_OIDC_ENDPOINT = env(
    'SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_OIDC_ENDPOINT',
    'http://localhost:8000')

DATE_INPUT_FORMATS = ['%Y-%m-%d']  # , '%d-%m-%Y']

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = '/social-auth/login/vmi'

EXTERNAL_AUTH_NAME = "Google"

APPLICATION_TITLE = env('DJANGO_APPLICATION_TITLE',
                        'HIXNY OAuth2 Provider')
ORGANIZATION_TITLE = env(
    'DJANGO_ORGANIZATION_TITLE',
    'Alliance for Better Health')
ORGANIZATION_URI = env('DJANGO_ORGANIZATION_URI', 'https://abhealth.us')
POLICY_URI = env(
    'DJANGO_POLICY_URI',
    'https://abhealth.us')
POLICY_TITLE = env('DJANGO_POLICY_TITLE', 'Privacy Policy')
TOS_URI = env('DJANGO_TOS_URI', 'https://abhealth.us')
TOS_TITLE = env('DJANGO_TOS_TITLE', 'Terms of Service')
TAG_LINE_1 = env('DJANGO_TAG_LINE_1', 'Share your health data')
TAG_LINE_2 = env('DJANGO_TAG_LINE_2',
                 'with applications, organizations, and people you trust.')
EXPLAINATION_LINE = 'This service allows Medicare beneficiaries to connect their health data to applications of their choosing.'  # noqa
EXPLAINATION_LINE = env('DJANGO_EXPLAINATION_LINE ', EXPLAINATION_LINE)
USER_DOCS_URI = "https://abhealth.us"
USER_DOCS_TITLE = "User Documentation"
USER_DOCS = "USer Docs"
# LINKS TO DOCS
DEVELOPER_DOCS_URI = "https:/abhealth.us"
DEVELOPER_DOCS_TITLE = "Developer Documentation"
DEVELOPER_DOCS = "Developer Docs"
DEFAULT_DISCLOSURE_TEXT = """
    This system may be monitored, recorded and
    subject to audit. Improper use of this system or
    its data may result in civil and criminal penalties.
    """

DISCLOSURE_TEXT = env('DJANGO_PRIVACY_POLICY_URI', DEFAULT_DISCLOSURE_TEXT)

HOSTNAME_URL = env('HOSTNAME_URL', 'http://sharemyhealth:8001')

VMI_SIGNUP_URL = "%s/accounts/create-account/%s/?next=%s" % \
                 (SOCIAL_AUTH_VERIFYMYIDENTITY_OPENIDCONNECT_OIDC_ENDPOINT,
                  APPLICATION_TITLE,
                  HOSTNAME_URL)

# DOT +
GRANT_AUTHORIZATION_CODE = "authorization-code"
GRANT_IMPLICIT = "implicit"
# GRANT_PASSWORD = "password"
# GRANT_CLIENT_CREDENTIALS = "client-credentials"
GRANT_TYPES = (
    (GRANT_AUTHORIZATION_CODE, _("Authorization code")),
    # (GRANT_IMPLICIT, _("Implicit")),
    # (GRANT_PASSWORD, _("Resource owner password-based")),
    # (GRANT_CLIENT_CREDENTIALS, _("Client credentials")),
)


CALL_MEMBER = "member"
CALL_MEMBER_PLURAL = "members"
CALL_ORGANIZATION = "organization"
CALL_ORGANIZATION_PLURAL = "organizations"

# FHIR Server to Proxy (Default) - with trailing slash

DEFAULT_FHIR_SERVER = "http://fhir-test.sharemy.health:8080/fhir/baseDstu3/"
DEFAULT_OUT_FHIR_SERVER = HOSTNAME_URL + "/fhir/baseDstu3"


FHIR_RESOURCES_SUPPORTED = ('Patient', 'Observation', 'Condition', 'Medication',
                            'MedicationStatement', 'MedicationOrder',
                            'AllergyIntolerance', 'DiagnosticReport',
                            'Procedure', 'CarePlan', 'Immunization',
                            'Device', 'Goal', 'Coverage', 'ExplanationOfBenefit')

DEFAULT_SAMPLE_FHIR_ID = "472"


SETTINGS_EXPORT = [
    'DEBUG',
    'ALLOWED_HOSTS',
    'APPLICATION_TITLE',
    'STATIC_URL',
    'STATIC_ROOT',
    'DEVELOPER_DOCS_URI',
    'DEVELOPER_DOCS_TITLE',
    'ORGANIZATION_TITLE',
    'POLICY_URI',
    'POLICY_TITLE',
    'DISCLOSURE_TEXT',
    'TOS_URI',
    'TOS_TITLE',
    'TAG_LINE_1',
    'TAG_LINE_2',
    'EXPLAINATION_LINE',
    'EXTERNAL_AUTH_NAME',
    'USER_DOCS_URI',
    'USER_DOCS',
    'DEVELOPER_DOCS',
    'USER_DOCS_TITLE',
    'VMI_SIGNUP_URL',
    'CALL_MEMBER',
    'CALL_MEMBER_PLURAL',
    'CALL_ORGANIZATION',
    'CALL_ORGANIZATION_PLURAL'
]


HIXNY_TOKEN_API_URI = env('HIXNY_TOKEN_API_URI',
                          'https://integration.hixny.com:6443/')
HIXNY_PATIENT_API_URI = env('HIXNY_PATIENT_API_URI',
                            'https://integration.hixny.com:5443')
HIXNY_PHRREGISTER_API_URI = "%s/PHRREGISTER" % (HIXNY_PATIENT_API_URI)
HIXNY_ACTIVATESTAGEDUSER_API_URI = "%s/ACTIVATESTAGEDUSER" % (
    HIXNY_PATIENT_API_URI)
HIXNY_CONSUMERDIRECTIVE_API_URI = "%s/CONSUMERDIRECTIVE" % (
    HIXNY_PATIENT_API_URI)
HIXNY_GETDOCUMENT_API_URI = "%s/GETDOCUMENT" % (HIXNY_PATIENT_API_URI)
HIXNY_WORKBENCH_USERNAME = env('HIXNY_WORKBENCH_USERNAME', '')
HIXNY_WORKBENCH_PASSWORD = env('HIXNY_WORKBENCH_PASSWORD', '')
HIXNY_BASIC_AUTH_PASSWORD = env('HIXNY_BASIC_AUTH_PASSWORD', '')
