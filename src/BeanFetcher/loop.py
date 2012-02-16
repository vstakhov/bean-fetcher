'''
Created on Feb 16, 2012

@author: cebka
'''

import config
import logging
import beanstalkc
import signal
import subprocess
import shlex
import time
import sys
import fcntl
import os
import pwd
from multiprocessing import Process

class FetchWorker(Process):
    
    def __init__(self, instance):
        self.instance = instance

        self.wanna_die = False
        super(FetchWorker, self).__init__()
    
    
    def parse_arg(self, arg):
        '''
        Read a single argument for a 'magic' value
        '''
        if arg == '%t':
            return time.strftime('format')
        return arg
    
    def run(self):
        signal.signal(signal.SIGINT, self.set_wanna_die)
        signal.signal(signal.SIGTERM, self.set_wanna_die)
        if 'user' in self.instance and os.getuid() == 0:
            # Drop priv
            (uid,gid) = pwd.getpwnam(self.instance['user'])[2:4]
            os.setuid(uid)
            #os.setgid(gid)
        if 'command' in self.instance:
            args = filter(self.parse_arg, shlex.split(self.instance['command']))
        while not self.wanna_die:
            fnull = open(os.devnull, 'w')
            # Fetch forever
            try:
                beanstalk = beanstalkc.Connection(host=self.instance['host'],
                                              port=self.instance['port'],
                                              parse_yaml=False)
                job = beanstalk.reserve()
                if 'command' in self.instance:
                    # Execute command
                    prg = subprocess.Popen(args, stdin=subprocess.PIPE,stdout=fnull,stderr=fnull)
                    prg.communicate(job.body)
                elif 'file' in self.instance:
                    # Append to file
                    with open(self.instance['file'], 'a') as f:
                        fcntl.lockf(f.fileno(), fcntl.LOCK_EX)
                        f.write(job.body)
                        fcntl.lockf(f.fileno(), fcntl.LOCK_UN)
                job.delete()
                beanstalk.close()
            except beanstalkc.BeanstalkcException as e:
                logging.error('Catched beanstalk exception while running: %s, sleeping' % str(e))
                time.sleep(5)
            except Exception as e:
                logging.error('Catched exception while running: %s' % str(e))
                
    def set_wanna_die(self, signum, frame):
        sys.exit()
                
class FetchLoop(object):
    '''
    Fetching loop
    '''
    def __init__(self, instance):
        '''
        Constructor
        '''
        self.workers = []
        for i in xrange(instance['workers']):
            worker = FetchWorker(instance)
            self.workers.append(worker)
            worker.start()