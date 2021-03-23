
from realmachine import RealMachine

# file = 'test_program_1'
file = 'test_program_2'

rm = RealMachine()
rm.load_virtual_machine(file)
rm.processor.execute()
