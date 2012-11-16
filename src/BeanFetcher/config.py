'''
Created on Feb 16, 2012

@author: cebka
'''

import ConfigParser
import logging

class BeanConfig(object):
    '''
    Parse configuration file
    '''


    def __init__(self, confname='/usr/local/etc/bean-fetcher.ini'):
        '''
        Constructor
        '''
        self.confname = confname
        self.instances = {}
        self.load()
    
    def load(self):
        '''
        Load configuration
        '''
        config = ConfigParser.SafeConfigParser()
        config.read(self.confname)
        for s in config.sections():
            if config.has_option(s, 'host') or config.has_option(s, 'port'):
                instance = {'host': 'localhost',
                            'port': 11300,
                            'workers': 1,
                            'file': '/dev/null'}
                if config.has_option(s, 'host'):
                    instance['host'] = config.get(s, 'host')
                if config.has_option(s, 'tube'):
                    instance['tube'] = config.get(s, 'tube')
                if config.has_option(s, 'port'):
                    instance['port'] = int(config.getint(s, 'port'))
                if config.has_option(s, 'workers'):
                    instance['workers'] = int(config.getint(s, 'workers'))
                if config.has_option(s, 'command'):
                    instance['command'] = config.get(s, 'command')
                if config.has_option(s, 'smtp'):
                    instance['smtp'] = config.get(s, 'smtp')
                    del instance['file']
                    if config.has_option(s, 'smtp_from'):
                        instance['smtp_from'] = config.get(s, 'smtp_from')
                    else:
                        instance['smtp_from'] = 'beanstalk@example.com'
                    if config.has_option(s, 'smtp_rcpt'):
                        instance['smtp_rcpt'] = config.get(s, 'smtp_rcpt')
                    else:
                        instance['smtp_rcpt'] = 'postmaster@localhost'
                        
                if config.has_option(s, 'user'):
                    instance['user'] = config.get(s, 'user')
                if config.has_option(s, 'file'):
                    instance['file'] = config.get(s, 'file')
                self.instances[s] = instance
            else:
                logging.error('Bad section, need host or port defined: %s' % s)
