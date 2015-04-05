#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pprint import pprint
from shaddock import model

class ModelTests(unittest.TestCase):

    def testService_dic(self):
        self.containerconfig = model.ContainerConfig('nova')


def main():
    unittest.main()

if __name__ == '__main__':
    main()