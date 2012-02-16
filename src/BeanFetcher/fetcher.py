'''
Created on Feb 16, 2012

@author: cebka
'''

import signal
import os
import logging
import logging.handlers
from BeanFetcher import config, loop
from optparse import OptionParser

class BeanFetcher(object):
    '''
    Main fetching class
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.parse_args()
        # Init signals
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        
        # Init logger
        logger = logging.getLogger("bean-fetcher")
        self.handler = logging.handlers.SysLogHandler()
        formatter = logging.Formatter("%(name)s[%(process)d]: %(message)s")
        self.handler.setFormatter(formatter)
        self.handler.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
        logger.addHandler(self.handler)
        self.logger = logger
        
        # Read init file
        cfg = config.BeanConfig(self.options.config)
        self.workers = []
        
        # Start workers
        for (name,instance) in cfg.instances.iteritems():
            instance_loop = loop.FetchLoop(instance)
            self.workers = self.workers + instance_loop.workers
        
        try:
            # Infinite wait loop
            for worker in self.workers:
                worker.join()
        finally:
            logging.info('Terminating, no jobs')
    
    def parse_args(self):
        usage = "usage: %prog [-c config_file]"
        parser = OptionParser(usage=usage, version="%prog 1.0")
        parser.add_option("-c", "--config", dest="config", help="use specified configuration", default="/usr/local/etc/bean-fetcher.ini")
        (options, args) = parser.parse_args()
        self.options = options
    
    def cleanup(self, signum, frame):
        # Terminate all workers
        for worker in self.workers:
            os.kill(worker.pid, signal.SIGTERM)