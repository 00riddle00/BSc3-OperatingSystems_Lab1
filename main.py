#!/usr/bin/python

from realmachine import RealMachine

file = 'test_program_1'
rm = RealMachine()
rm.load_virtual_machine(file)
rm.processor.execute()
