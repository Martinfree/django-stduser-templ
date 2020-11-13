import os
import logging as log
from settings.base import setup_logger

"""If you must to debug your project import this file 'from logger import LOG' and all ready to work"""

class Logger:
    BASE_DIR = '/opt/proj/api/'
    conf = {
    'version': 1,
    'disable_existing_loggers': False,}
    filters = {'filters': {

        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },}
              }

    formatter = {'formatters': {
        'debug': {
            'format' : ('TEST_LOGGER\n[{levelname}]\n{message}'),
            'style': '{',},}}
    
    handlers = {'handlers': {
         'debug': {
            'level': 'DEBUG', 
            'class': 'logging.StreamHandler',
            'formatter': 'debug',},}
         }

    loggers = {'loggers':{
        'django':{
            'handlers': ['debug'],
            'level': 'DEBUG',
            'propagate': True,},
            }
             }

    def __init__(self):
        self.conf.update(self.filters)
        self.conf.update(self.formatter)
        self.conf.update(self.handlers)
        self.conf.update(self.loggers)
        return None

log = Logger()
LOG = setup_logger(config=Logger.conf)
