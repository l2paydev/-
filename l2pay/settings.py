# Django settings for example project.
import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)


DEBUG = True
APPEND_SLASH = False


ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME", "local-l2pay-api"),
        "USER": os.environ.get("DATABASE_USER", "l2pay"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "l2pay"),
        "HOST": os.environ.get("DATABASE_HOST", "100.103.64.65"),
        "PORT": os.environ.get("DATABASE_PORT", "5436"),
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "UTC"
USE_TZ = True

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en"

LANGUAGES = [
    ("ar", "Arabic"),
    ("az", "Azerbaijani"),
    ("bg", "Bulgarian"),
    ("ca", "Catalan"),
    ("cs", "Czech"),
    ("da", "Danish"),
    ("de", "German"),
    ("el", "Greek"),
    ("en", "English"),
    ("es", "Spanish"),
    ("et", "Estonian"),
    ("eu", "Basque"),
    ("fa", "Persian"),
    ("fi", "Finnish"),
    ("fr", "French"),
    ("he", "Hebrew"),
    ("hr", "Croatian"),
    ("hu", "Hungarian"),
    ("id", "Indonesian"),
    ("it", "Italian"),
    ("ja", "Japanese"),
    ("ka", "Georgian"),
    ("ko", "Korean"),
    ("ky", "Kyrgyz"),
    ("lt", "Lithuanian"),
    ("lv", "Latvian"),
    ("mn", "Mongolian"),
    ("nb", "Norwegian Bokmål"),
    ("nl", "Dutch"),
    ("pl", "Polish"),
    ("pt-BR", "Portuguese (Brazil)"),
    ("pt-PT", "Portuguese (Portugal)"),
    ("ro", "Romanian"),
    ("ru", "Russian"),
    ("sk", "Slovak"),
    ("sl", "Slovenian"),
    ("sr", "Serbian"),
    ("sr-Latn", "Serbian (Latin)"),
    ("sv", "Swedish"),
    ("th", "Thai"),
    ("tr", "Turkish"),
    ("uk", "Ukrainian"),
    ("zh-hans", "Chinese (Simplified)"),
    ("zh-hant", "Chinese (Traditional)"),
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ""

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ""

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = "static"

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = "/dstatic/"

# Additional locations of static files
STATICFILES_DIRS = (os.path.join(BASE_DIR / "dstatic"),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = "t8_)kj3v!au0!_i56#gre**mkg0&z1df%3bw(#5^#^5e_64!$_"

# List of callables that know how to import templates from various sources.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "l2pay" / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "allauth.account.middleware.AccountMiddleware",
)

AUTHENTICATION_BACKENDS = ("allauth.account.auth_backends.AuthenticationBackend",)

ROOT_URLCONF = "l2pay.urls"

INSTALLED_APPS = (
    "l2pay.l2pay",
    "drf_spectacular",
    "jazzmin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.humanize",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.admin",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # "allauth.mfa",
    # "allauth.socialaccount.providers.dropbox",
    # "allauth.socialaccount.providers.dingtalk",
    # "allauth.socialaccount.providers.facebook",
    # "allauth.socialaccount.providers.edx",
    # "allauth.socialaccount.providers.evernote",
    "allauth.socialaccount.providers.google",
    "allauth.socialaccount.providers.github",
    # "allauth.socialaccount.providers.linkedin_oauth2",
    # "allauth.socialaccount.providers.mediawiki",
    # "allauth.socialaccount.providers.openid",
    # "allauth.socialaccount.providers.openid_connect",
    # "allauth.socialaccount.providers.pinterest",
    # "allauth.socialaccount.providers.pocket",
    # "allauth.socialaccount.providers.reddit",
    # "allauth.socialaccount.providers.saml",
    # "allauth.socialaccount.providers.shopify",
    # "allauth.socialaccount.providers.slack",
    # "allauth.socialaccount.providers.snapchat",
    # "allauth.socialaccount.providers.soundcloud",
    # "allauth.socialaccount.providers.stackexchange",
    "allauth.socialaccount.providers.telegram",
    # "allauth.socialaccount.providers.twitch",
    "allauth.socialaccount.providers.twitter",
    "allauth.socialaccount.providers.twitter_oauth2",
    # "allauth.socialaccount.providers.vimeo",
    # "allauth.socialaccount.providers.vimeo_oauth2",
    # "allauth.socialaccount.providers.weibo",
    # "allauth.socialaccount.providers.xing",
    "allauth.usersessions",
    "rest_framework",
    "rest_framework_api_key",
)


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 9,
        },
    }
]

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "127.0.0.1,localhost,testnet.l2pay.ing,l2pay.ing,10.10.1.14",
).split(",")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://testnet.l2pay.ing,https://l2pay.ing",
).split(",")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
ACCOUNT_LOGIN_BY_CODE_ENABLED = False

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        "APP": {
            "client_id": "",
            "secret": "",
            "key": "",
        }
    }
}

REST_FRAMEWORK = {
    # YOUR SETTINGS
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "API Docs - L2PAY",
    "DESCRIPTION": "API Docs - L2PAY",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "APPEND_COMPONENTS": {
        "securitySchemes": {
            "Merchant": {
                "type": "apiKey",
                "in": "header",
                "name": "Authorization",
                "description": "Put `Api-Key YOUR_API_KEY` into `Authorization` header",
            }
        }
    },
    # OTHER SETTINGS
}

PRIVATE_KEY = 0x31234


JAZZMIN_SETTINGS = {
    # title of the window (Will default to current_admin_site.site_title if absent or None)
    "site_title": "Dashboard | L2PAY",
    # Title on the login screen (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_header": "Dashboard",
    # Title on the brand (19 chars max) (defaults to current_admin_site.site_header if absent or None)
    "site_brand": "L2PAYING",
    # Logo to use for your site, must be present in static files, used for brand on top left
    "site_logo": "l2pay/logo1.png",
    # Logo to use for your site, must be present in static files, used for login form logo (defaults to site_logo)
    "login_logo": None,
    # Logo to use for login form in dark themes (defaults to login_logo)
    "login_logo_dark": None,
    # CSS classes that are applied to the logo above
    "site_logo_classes": "img-rounded",
    # Relative path to a favicon for your site, will default to site_logo if absent (ideally 32x32 px)
    "site_icon": None,
    # Welcome text on the login screen
    "welcome_sign": "Welcome to the L2PAY",
    # Copyright on the footer
    "copyright": "Acme L2PAY Ltd",
    # List of model admins to search from the search bar, search bar omitted if excluded
    # If you want to use a single search field you dont need to use a list, you can use a simple string
    "search_model": ["auth.User", "auth.Group"],
    # Field name on user model that contains avatar ImageField/URLField/Charfield or a callable that receives the user
    "user_avatar": None,
    ############
    # Top Menu #
    ############
    # Links to put along the top menu
    "topmenu_links": [
        # Url that gets reversed (Permissions can be added)
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        # external url that opens in a new window (Permissions can be added)
        {
            "name": "Support",
            "url": "https://github.com/farridav/django-jazzmin/issues",
            "new_window": True,
        },
        # model admin to link to (Permissions checked against model)
        {"model": "auth.User"},
        # App with dropdown menu to all its models pages (Permissions checked against models)
        {"app": "books"},
    ],
    #############
    # User Menu #
    #############
    # Additional links to include in the user menu on the top right ("app" url type is not allowed)
    "usermenu_links": [
        {
            "name": "Support",
            "url": "https://github.com/farridav/django-jazzmin/issues",
            "new_window": True,
        },
        {"model": "auth.user"},
    ],
    #############
    # Side Menu #
    #############
    # Whether to display the side menu
    "show_sidebar": True,
    # Whether to aut expand the menu
    "navigation_expanded": True,
    # Hide these apps when generating side menu e.g (auth)
    "hide_apps": [],
    # Hide these models when generating side menu (e.g auth.user)
    "hide_models": [],
    # List of apps (and/or models) to base side menu ordering off of (does not need to contain all apps/models)
    "order_with_respect_to": ["auth"],
    # Custom links to append to app groups, keyed on app name
    "custom_links": {
        # "books": [
        #     {
        #         "name": "Make Messages",
        #         "url": "make_messages",
        #         "icon": "fas fa-comments",
        #         "permissions": ["books.view_book"],
        #     }
        # ]
    },
    # Custom icons for side menu apps/models See https://fontawesome.com/icons?d=gallery&m=free&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2
    # for the full list of 5.13.0 free icon classes
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    # Icons that are used when one is not manually specified
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    #################
    # Related Modal #
    #################
    # Use modals instead of popups
    "related_modal_active": False,
    #############
    # UI Tweaks #
    #############
    # Relative paths to custom CSS/JS scripts (must be present in static files)
    "custom_css": None,
    "custom_js": None,
    # Whether to link font from fonts.googleapis.com (use custom_css to supply font otherwise)
    "use_google_fonts_cdn": True,
    # Whether to show the UI customizer on the sidebar
    "show_ui_builder": False,
    ###############
    # Change view #
    ###############
    # Render out the change view as a single form, or in tabs, current options are
    # - single
    # - horizontal_tabs (default)
    # - vertical_tabs
    # - collapsible
    # - carousel
    "changeform_format": "horizontal_tabs",
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    # Add a language dropdown into the admin
    "language_chooser": True,
}


###########################
CELERYD_CONCURRENCY = 3  # Set the number of worker processes to 4
CELERY_BEAT_SCHEDULE = {
    "periodict_track_open_payments": {
        "task": "l2pay.l2pay.core.periodict_track_open_payments",
        "schedule": 10,  # seconds
    },
}
###########################
