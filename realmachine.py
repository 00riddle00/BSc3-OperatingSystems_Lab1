#!/usr/bin/python

from math import ceil

from processor import Processor
from memory import RealMemory
from memory import BLOCK_SIZE

class RealMachine(object):
    """ Realią mašiną simuliuojantis objektas.
    """

    def __init__(self):
        """ Inicializuoja mašinos objektą.
        """

        self.real_memory = RealMemory()
        self.processor = Processor(self.real_memory)
        self.virtual_memory_data = None
        self.virtual_memory_code = None

    def load_virtual_machine(self, file):
        """ Pakrauna virtualią mašiną.
        """

        code = []
        code_size = 6
        data = []
        data_size = None
        data = {}
        block_nr = 0

        if isinstance(file, str):
            with open(file) as fp:
                code_segment = False
                data_segment = False
                for line in fp:

                    if line == '\n':
                        continue
                    elif not data_segment and line == '.code\n':
                        code_segment = True
                        continue
                    elif line.startswith('.data'):
                        code_segment = False
                        data_segment = True
                        data_size = 8

                    if code_segment:
                        code.append(line)
                    if data_segment:
                        if line.startswith('.data'):
                            block_nr = int(line[5:])
                            data[block_nr] = []
                        else:
                            # TODO check for max 16 words
                            data[block_nr].append(line)

            self.virtual_memory_code, self.virtual_memory_data = \
                    self.real_memory.create_virtual_memory(
                            code, code_size, data, data_size)


            self.processor.PLR = self.virtual_memory_code.pager.PLR
            self.processor.PLBR = self.virtual_memory_code.pager.PLBR
            self.processor.set_virtual_memory(
                    self.virtual_memory_code, self.virtual_memory_data)
            self.processor.IC = 0
            # TODO: Atidaryti išorinius failus.
        else:
            # Šitas if iš esmės skirtas tam, jei kartais butų visgi
            # nuspręsta pasinaudoti „#!/usr/bin/pyemu“ funkcionalumu.
            raise Exception('Not implemented!')
