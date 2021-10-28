"""Logging configuration"""

MAX_QUEUE_SIZE = 1000

# https://docs.python.org/3/library/logging.html#logrecord-attributes
DEFAULT = '%(asctime)s - %(thread)d - %(levelname)s - %(message)s'
CODE_INFO = ' [in %(pathname)s:%(lineno)d in %(funcName)s]'


def get_configuration(
        logger_name,
        debug_console_level='DEBUG',
        debug_file_level='DEBUG',
        debug_file_location=None,
        error_file_level='ERROR',
        error_file_location=None):
    """
    Logging configuration

    Console logs are in plain text format, everything else is configured
    to output to JSON. Makes it easier to integrate with 3rd party tools
    """
    debug_console_level = debug_console_level.upper()
    debug_file_level = debug_file_level.upper()
    error_file_level = error_file_level.upper()
    return {
        'version': 1,
        'disable_existing_loggers': True,
        'objects': {
            'queue': {
                'class': 'queue.Queue',
                'maxsize': MAX_QUEUE_SIZE
            }
        },
        'formatters': {
            'default': {
                'format': DEFAULT,
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'verbose': {
                'format': DEFAULT + CODE_INFO,
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'default_json': {
                'format': DEFAULT + CODE_INFO,
                'class': 'pythonjsonlogger.jsonlogger.JsonFormatter'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': debug_console_level,
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'debug_file_handler': {
                'class': 'logging.handlers.WatchedFileHandler',
                'level': debug_file_level,
                'formatter': 'default_json',
                'filename': debug_file_location,
                'encoding': 'utf8'
            },
            'error_file_handler': {
                'class': 'logging.handlers.WatchedFileHandler',
                'level': error_file_level,
                'formatter': 'default_json',
                'filename': error_file_location,
                'encoding': 'utf8'
            },
            # 'log_queue_listener': {
            #     'class': 'src.configuration.modules.logger.QueueListenerHandler',
            #     'handlers': [
            #         'cfg://handlers.console',
            #         'cfg://handlers.debug_file_handler',
            #         'cfg://handlers.error_file_handler'
            #     ],
            #     'queue': 'cfg://objects.queue'
            # },
        },
        'loggers': {
            logger_name + '.console': {
                'level': debug_console_level,
                'handlers': ['console'],
                'propagate': False
            },
            # logger_name + '.debug': {
            #     'level': debug_file_level,
            #     'handlers': ['log_queue_listener'],
            #     'propagate': False,
            #     'qualname': logger_name + '.debug'
            # },
            # logger_name + '.error': {
            #     'level': error_file_level,
            #     'handlers': ['log_queue_listener'],
            #     'propagate': False,
            #     'qualname': logger_name + '.error'
            # },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console', 'debug_file_handler', 'error_file_handler']
        }
    }
