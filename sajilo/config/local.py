import os
from .common import Common
from .common import env

class Local(Common):
    DEBUG = False

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # Testing
    INSTALLED_APPS = Common.INSTALLED_APPS
    INSTALLED_APPS += ('django_nose',)
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [
        BASE_DIR,
        '-s',
        '--nologcapture',
        '--with-coverage',
        '--with-progressive',
        '--cover-package=sajilo'
    ]

    # Mail
    EMAIL_HOST = 'localhost'
    EMAIL_PORT = 1025
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    SECRET_KEY = env(
        "DJANGO_SECRET_KEY",
        default="bwW661eOlSKqpjLYUJLxF50mbqIPReLv9dMpR8kHevF4RvBvoxrW8rLc4POYK1JK",
    )