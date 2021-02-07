#!/usr/bin/python3

import pexpect
import re
import sys
import logging

#logging.basicConfig(filename='cleanup.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

class sshConn():

    def __init__(self, machineIp):

        self.machineIp = machineIp

        try:
            self.sshLine = 'ssh root@' + self.machineIp

            child = pexpect.spawn(self.sshLine, timeout=2)

            child.expect("password")

            logging.debug('Got PASSWORD prompt for machine with IP ({})'.format(self.machineIp))
            child.sendline('password')
            child.expect('#')

            self.child = child

            op = self.sendcmd('cd /tmp', '#')
            logging.debug(op)

            op = self.sendcmd('pwd', '#')
            logging.debug(op)

            op = self.sendcmd('ls -lrta', '#')
            logging.debug(op)

            op = self.sendcmd('rm -f *; ls -lrta', '#')
            logging.debug(op)

        except pexpect.exceptions.TIMEOUT as e:

            logging.debug('Then machine {} is not reachable: {}'.format(self.machineIp, e))

    def sendcmd(self, line, expect):

        self.child.sendline(line)
        self.child.expect(expect)
        return self.child.before

