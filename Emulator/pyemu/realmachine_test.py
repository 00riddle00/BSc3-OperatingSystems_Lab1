#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Testai.
"""

import unittest

from realmachine import RealMachine
from memory import RealMemory
from processor import Processor

class RealMachineTest(unittest.TestCase):
    """ Testai pagalbinėms funkcijoms.
    """

    def test_init_memory(self):

        r_mem = RealMemory()
        assert r_mem[356] == '00000000'
        r_mem[12, 11] = 'ačiū'
        assert r_mem[203] == '    ačiū'
                                        # 12 * 16 + 11 == 203

    def test_init_processor(self):

        r_mem = RealMemory()
        processor = Processor(r_mem)

    def test_init_real_machine(self):

        rm = RealMachine()

if __name__ == '__main__':
    unittest.main()
