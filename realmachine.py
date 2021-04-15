#!/usr/bin/python

from math import ceil

from processor import Processor
from memory import RealMemory

CODE_SIZE = 6
DATA_SIZE = 8

class RealMachine(object):
    """ Realią mašiną simuliuojantis objektas.
    """

    def __init__(self):
        """ Inicializuoja mašinos objektą.
        """

        self.real_memory = RealMemory()
        self.processor = Processor(self.real_memory)
        self.virtual_memory = None


    def load_virtual_machine(self, file):
        """ Pakrauna virtualią mašiną.
        """

        code = []
        code_size = CODE_SIZE
        data = {}
        data_size = 16
        block_no = 0
        words_in_block = 0

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

                    if code_segment:
                        code.append(line)
                    if data_segment:
                        if line.startswith('.data'):
                            block_no = int(line[5:])
                            data[block_no] = []
                            words_in_block = 0
                        else:
                            if words_in_block < 16:
                                data[block_no].append(line)
                                words_in_block += 1

            self.virtual_memory  = self.real_memory.create_virtual_memory(code, data, data_size)



            self.processor.PLR = self.virtual_memory.pager.PLR
            self.processor.PLBR = self.virtual_memory.pager.PLBR
            self.processor.set_virtual_memory(
                    self.virtual_memory)
            self.processor.IC = 0
            # TODO: Atidaryti išorinius failus.
        else:
            # Šitas if iš esmės skirtas tam, jei kartais butų visgi
            # nuspręsta pasinaudoti „#!/usr/bin/pyemu“ funkcionalumu.
            raise Exception('Not implemented!')
