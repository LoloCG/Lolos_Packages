import logging.config

logger = logging.getLogger(__name__)

# example logging config
logging_config = {
	'version': 1,
	'disable_existing_loggers': False, # False allows third party logs
	# 'filters': {},
	'formatters': {
		'datetimesecs': {
            'format': "{asctime} - {levelname}: {message}",
            'style': "{",
            'datefmt': "%Y-%m-%d %H:%M:%S",
		}
	},
	'handlers': {
		'stdout': {
			'class':'logging.StreamHandler', 
			'formatter': 'datetimesecs',
			'stream' : 'ext://sys.stdout', # external ???
		}
	},
	'loggers': {
		'root': {
			'level': 'DEBUG',
			'handlers': ['stdout'],
		}
	},
}

logging.config.dictConfig(config=logging_config)
logger.warning("debug mesg")