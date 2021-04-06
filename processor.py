#!/usr/bin/python

import inspect

from registers import Register, IntegerRegister, HexRegister
from registers import ChoiceRegister, StatusFlagRegister
from registers import hex_to_int

class Commands(object):
    """ Objektas representuojantis komandų sistemą.
    """

    def __init__(self):
        """ Susiindeksuoja visas savo komandas.
        """

        self.commands = dict([
                (name, function) \
                for name, function in \
                inspect.getmembers(self, inspect.isfunction) \
                ])

    def __getitem__(self, command):
        """ Gražina komandų sistemos komandą.
        """

        return self.commands[command]

    @staticmethod
    def LR(proc, x):
        proc.R = proc.virtual_memory_data[hex_to_int(x)]

    @staticmethod
    def LD(proc, x):
        proc.D = proc.virtual_memory_data[hex_to_int(x)]

    @staticmethod
    def PD(proc, x):
        print(proc.virtual_memory_data[hex_to_int(x)])

    @staticmethod
    def HALT(proc):
        print("Program has finished")

    @staticmethod
    def COMP(proc):
        if proc.R > proc.D:
            proc.SF.ZF = 0
            proc.SF.SF = 0
        elif proc.R == proc.D:
            proc.SF.ZF = 1
        else:
            proc.SF.ZF = 0
            proc.SF.SF = 1

    @staticmethod
    def JE(proc, x):
        if proc.SF.ZF == 1:
            proc.IC = x

class Processor(object):
    """ Realios mašinos procesorius.
    """

    IC = HexRegister(3)                 # Nurodo vykdomos komandos adresą
                                        # atmintyje.
    R = Register()                     # Žodžio ilgio bendro naudojimo
                                        # registras.
    D = Register()                     # Žodžio ilgio bendro naudojimo
                                        # registras.
    PLR = HexRegister(2)                # Puslapių lentelės bloko adresas.
    PLBR = HexRegister(2)               # Puslapių lentelės pirmojo baito
                                        # adresas bloke.
    MODE = ChoiceRegister(['N', 'S'])   # Nurodo procesoriaus darbo rėžimą:
                                        # „N“ – naudotojo,
                                        # „S“ – supervizoriaus.
    SF = StatusFlagRegister()           # Aritmetinių operacijų loginės
                                        # reikšmės.

    PI = ChoiceRegister([0, 1])         # Programiniai pertraukimai.
    SI = ChoiceRegister([0, 1])         # Supervizoriniai pertraukimai.
    TI = ChoiceRegister([0, 1])         # Laikrodžio pertraukimai.
    IOI = HexRegister(1)                # Įvedimo / išvedimo pertraukimai.
    CHST = HexRegister(1)               # Kanalų užimtumo registras.

    def __init__(self, real_memory,
            virtual_memory_code=None, virtual_memory_data=None):
        """ Inicializuoja procesorių.

        + ``real_memory`` – realios mašinos atmintis.
        + ``virtual_memory_code`` – virtualios mašinos atmintis, kodo
          segmentas.
        + ``virtual_memory_data`` – virtualios mašinos atmintis, duomenų
          segmentas.
        """

        self.real_memory = real_memory
        self.virtual_memory_code = virtual_memory_code
        self.virtual_memory_data = virtual_memory_data
        self.commands = Commands()

    def set_virtual_memory(self, virtual_memory_code, virtual_memory_data):
        """ Nurodo naudoti ``virtual_memory``, kaip virtualios atminties
        objektą.
        """

        self.virtual_memory_code = virtual_memory_code
        self.virtual_memory_data = virtual_memory_data

    def step(self):
        """ Įvykdo vieną komandą.

        Grąžina ``True`` jei pavyko ir ``False`` kitu atveju.
        """

        # print('Žingsnis:', self.IC, self.virtual_memory_code[self.IC])
        value = self.virtual_memory_code[self.IC]
        # value = 'LR 00a"
        self.IC = self.IC + 1

        if value[0] == 'H':  # meaning 'HALT'
            return False

        self.do(**self.parse_command(value))
        return True

    def parse_command(self, value):
        """ Iš atminties ląstelės reikšmės ``value`` atpažįsta komandos
        pavadinimą ir argumentus.
        Grąžina žodymą ``{'command': <atpažinta komanda>,
        'args': <komandos argumentų sąrašas>}``.
        """

        args = []
        last_symbol = value[3]

        if last_symbol.isdigit() or ord(last_symbol.upper()) in range(65,71):
            command = value[0:2]
            args.append(value[2:4])
        else:
            command = value.strip()

        return {'command': command, 'args': args}

    def do(self, command, args):
        """ Įvykdo komandą ``command`` su argumentais ``args``.
        """

        # print('command: {0} args: {1}'.format(command, args))
        self.commands[command](self, *args)

    def execute(self):
        """ Vykdo tol kol vykdosi.
        """

        while self.step():
            pass
