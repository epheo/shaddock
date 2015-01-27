#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pprint import pprint
from octopenstack import model

class ModelTests(unittest.TestCase):

    def testService_dic(self):
    	self.model = model.Model()
    	service_dic = self.model.services
        pprint(service_dic)
        
        exit(0)


def main():
    unittest.main()

if __name__ == '__main__':
    main()