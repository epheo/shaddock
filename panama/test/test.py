#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pprint import pprint
from panama import model

class ModelTests(unittest.TestCase):

    def testService_dic(self):
        self.dico = model.Dico('nova')


def main():
    unittest.main()

if __name__ == '__main__':
    main()