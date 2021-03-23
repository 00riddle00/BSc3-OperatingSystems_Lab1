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
        code_size = None
        data = []
        data_size = None

        if isinstance(file, str):
            with open(file) as fp:
                code_segment = False
                data_segment = False
                for line in fp:

                    if not code_segment and not data_segment and \
                            line == '.code\n':
                        code_segment = True
                        continue
                    elif code_segment and not data_segment and \
                            line == 'HALT\n':
                        code_segment = False
                        continue
                    elif not code_segment and not data_segment and \
                            line.startswith('.data06'):
                        data_segment = True
                        data_size = int(line[5:])
                        continue
                    elif not code_segment and data_segment and \
                            line == '======\n':
                        data_segment = False
                        continue

                    if code_segment:
                        code.append(line)
                    if data_segment:
                        data.append(line)
                code_size = int(ceil(float(len(code)) / BLOCK_SIZE))

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
