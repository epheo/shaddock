#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pprint
pp = pprint.PrettyPrinter()

class View(object):

    def service_list(self, service_list):
        print('service LIST:')
        for service in service_list:
            print(service)
        print('')

    def service_information(self, action, name, *argv):
        print('%s service %s with arguments:' % (action, name) )
        for arg in argv:
            print(arg)
        print('')

    def service_not_found(self, name):
        print('The service "%s" does not exist' % name)

    def command_not_found(self, name):
        print('The command "%s" does not exist' % name)
        print('Available commands are: build, create or start')

    def display_stream(self, line):
        stream = str(line)
        pp.pprint(stream)

    def usage():
        print('Commands are: build, run, rm, ip, ')

    def stopping(self, tag):
        print('Stoping container %s ...' % (tag))

    def removing(self, tag):
        print('Removing container %s ...' % (tag))

    def notlaunched(self, tag):
        print('Services %s not launched' % (tag))

    def ip(self, tag, ipaddr):
        print('Container %s on IP: %s' % (tag, ipaddr))