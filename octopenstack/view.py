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
        print('The command "%s" does not exist' % action)
        print('Available commands are: build, create or start')
