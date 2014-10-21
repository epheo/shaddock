#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

class FooTests(unittest.TestCase):

    def testFoo(self):
        self.failUnless(True)

def main():
    unittest.main()

if __name__ == '__main__':
    main()