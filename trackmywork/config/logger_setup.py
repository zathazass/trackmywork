LOCAL_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname}::{message}::{asctime}::{module}::{funcName}::{lineno:d}',
            'style': '{',
        },
        'advanced': {
            'format': '{levelname}::{message}::{asctime}::{module}::{funcName}::{lineno:d}::{process:d}::{thread:d}',
            'style': '{'
        }
    },
    'handlers': {
        'request_file': {
            'level': 'DEBUG',
            'formatter': 'advanced',
            'class': 'logging.FileHandler',
            'filename': 'logs/request.log',
        },
        'server_file': {
            'level': 'DEBUG',
            'formatter': 'advanced',
            'class': 'logging.FileHandler',
            'filename': 'logs/server.log',
        },
        'security_file': {
            'level': 'DEBUG',
            'formatter': 'advanced',
            'class': 'logging.FileHandler',
            'filename': 'logs/security.log',
        },
        'template_file': {
            'level': 'DEBUG',
            'formatter': 'advanced',
            'class': 'logging.FileHandler',
            'filename': 'logs/template.log',
        },
        'common_file': {
            'level': 'WARNING',
            'formatter': 'advanced',
            'class': 'logging.FileHandler',
            'filename': 'prod_logs/common.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['request_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['server_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.security.*': {
            'handlers': ['security_file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['template_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'common': {
            'handlers': ['common_file'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}

PRODUCTION_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '{levelname}::{message}::{asctime}::{module}::{funcName}::{lineno:d}',
            'style': '{',
        },
        'advanced': {
            'format': '{levelname}::{message}::{asctime}::{module}::{funcName}::{lineno:d}::{process:d}::{thread:d}',
            'style': '{'
        }
    },
    'handlers': {
        'request_file': {
            'level': 'ERROR',
            'formatter': 'advanced',
            'class': 'logging.FileHandler',
            'filename': 'prod_logs/request.log',
        },
        'server_file': {
            'level': 'ERROR',
            'formatter': 'advanced',
            'class': 'logging.FileHandler',
            'filename': 'prod_logs/server.log',
        },
        'security_file': {
            'level': 'ERROR',
            'formatter': 'advanced',
            'class': 'logging.FileHandler',
            'filename': 'prod_logs/security.log',
        },
        'template_file': {
            'level': 'ERROR',
            'formatter': 'advanced',
            'class': 'logging.FileHandler',
            'filename': 'prod_logs/template.log',
        },
        'common_file': {
            'level': 'WARNING',
            'formatter': 'advanced',
            'class': 'logging.FileHandler',
            'filename': 'prod_logs/common.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['request_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.server': {
            'handlers': ['server_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security.*': {
            'handlers': ['security_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.template': {
            'handlers': ['template_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'common': {
            'handlers': ['common_file'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}
