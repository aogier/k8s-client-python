'''
Created on 21 mar 2018

@author: oggei
'''

from kubernetes import config
import os
import logging as log
from kubernetes.config.config_exception import ConfigException


def load():

    log.debug('Trying to sense my environment ...')

    if all(map(os.environ.get,
               [config.incluster_config.SERVICE_HOST_ENV_NAME,
                config.incluster_config.SERVICE_PORT_ENV_NAME])):
        try:
            config.load_incluster_config()
            log.debug('Loaded incluster_config.')
        except Exception as e:
            raise ConfigException('error loading incluster config:'
                                  ' {}'.format(e))
    else:
        try:
            config.load_kube_config()
            log.debug('Loaded kube_config.')
        except Exception as e:
            raise ConfigException('error loading kube config:'
                                  ' {}'.format(e))
