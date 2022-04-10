"""
Converting postgres and sqlite url into django database dict.
"""
import re
from decouple import config

DEFAULT_ENV = 'DJANGO_DB_DEFAULT_URL'
SQLITE_DB_NAMES = ['sqlite', 'sqlite3']
POSTGRESQL_DB_NAMES = ['postgres', 'postgresql', 'pgsql']
DB_PROVIDER = POSTGRESQL_DB_NAMES # + SQLITE_DB_NAMES

SQLITE_ENGINE_NAME = 'django.db.backends.sqlite3'
POSTGRESQL_ENGINE_NAME = 'django.db.backends.postgresql_psycopg2'

DatabaseUrlToDictErrorMessage = 'Use Postgresql as DB URL'
class DatabaseUrlToDictError(Exception):
	pass

class DatabaseUrlToDict:
    def __init__(self, *, env, conn_max_age, ssl_require, atomic_requests, engine):
        self._env = env
        self._conn_max_age = conn_max_age
        self._ssl_require = ssl_require
        self._atomic_requests = atomic_requests
        self._engine = engine

    def _find_db(self):
        db_provider, *_ = self._env.split(':')
        if db_provider in DB_PROVIDER:
            return db_provider
        else:
            raise DatabaseUrlToDictError(DatabaseUrlToDictErrorMessage)

    def to_dict(self):
        self.config = {}
        try:
            db_provider = self._find_db()
        except DatabaseUrlToDictError as error:
            return error
        except Exception as e:
            return DatabaseUrlToDictError(e)

        if db_provider in POSTGRESQL_DB_NAMES:
            _, usr_pw_hos_por, name = [x for x in self._env.split('/') if x]
            name = name.split('?')[0] # if ?sslmode=require is set in url
            usr_pw, hos_por = usr_pw_hos_por.rsplit('@', 1)
            user, password = usr_pw.split(':', 1)
            host, port = hos_por.split(':')
            port = int(port)
            self.config['ENGINE'] = POSTGRESQL_ENGINE_NAME

        self.config.update({
            'USER': user,
            'PASSWORD': password,
            'HOST': host,
            'PORT': port,
            'NAME': name
        })

        if self._engine is not None and isinstance(self._engine, str):
            self.config['ENGINE'] = self._engine

        if self._conn_max_age is not None and isinstance(self._conn_max_age, int):
            self.config['CONN_MAX_AGE'] = self._conn_max_age

        if isinstance(self._atomic_requests, bool) and self._atomic_requests:
            self.config['ATOMIC_REQUESTS'] = self._atomic_requests

        if self._ssl_require is not None and isinstance(self._ssl_require, bool):
            if self._ssl_require:
                self.config['OPTIONS'] = {'sslmode': 'require'}

        is_sslmode = re.search(r'sslmode=require', self._env)
        if is_sslmode is not None:
            self.config['OPTIONS'] = {'sslmode': 'require'}
        return self.config

def convert_to_dict(*, env=None, conn_max_age=None, engine=None,
    ssl_require=False, atomic_requests=None
    ):
    if env is None:
        env = config(DEFAULT_ENV)

    return DatabaseUrlToDict(
        env=env, conn_max_age=conn_max_age, engine=engine,
        ssl_require=ssl_require, atomic_requests=atomic_requests
    ).to_dict()
