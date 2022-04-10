import os
from decouple import config, Choices, Csv
from trackmywork.db_url import convert_to_dict

PROJECT_CONFIG_PATH = 'trackmywork.config'

BASE = f'{PROJECT_CONFIG_PATH}.base'
LOCAL = f'{PROJECT_CONFIG_PATH}.local'
DEPLOY = f'{PROJECT_CONFIG_PATH}.deploy'
PRODUCTION = f'{PROJECT_CONFIG_PATH}.production'

CONFIG_CHOICES = [
	BASE, LOCAL, DEPLOY, PRODUCTION
]

def setup_env():
	os.environ.setdefault(
		'DJANGO_SETTINGS_MODULE',
		config(
			'DJANGO_SETTINGS_MODULE',
			cast=Choices(CONFIG_CHOICES),
			default=BASE
		)
	)

__all__ = ['config', 'Choices', 'Csv', 'convert_to_dict']


# Django Database URL Configurations Help
'''
from dj_database_url import config as db_config

db_config(env=DEFAULT_ENV, default=None, engine=None, conn_max_age=0, ssl_require=False)
'''
