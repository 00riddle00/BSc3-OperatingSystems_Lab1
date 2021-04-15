#!/usr/bin/python

""" Modulis, kuriame realizuotos klasės mašinos atminties emuliacijos
realizacijai.
"""

import re

from math import ceil, floor

from registers import WORD_SIZE
from registers import int_to_hex, hex_to_int
from registers import Cell

BLOCKS = 96
BLOCK_SIZE = 16
# WORD_SIZE = 4
PAGER_SIZE = 16

def ih(number):
    """ Gautąjį ``number`` konvertuoja į šešioliktainį skaičių
    dviejuose baituose.
    """
    string = int_to_hex(number, 2)
    assert len(string) == 2
    return string

class Pager(object):
    """ Pagalbinis objektas tvarkymuisi su puslapiavimo mechanizmu.
    """

    def __init__(self, memory, address=None, C=None, D=None):
        """ Jei ``address`` nėra None, tai puslapiavimo mechanizmą nuskaito
        iš atminties. Kitu atveju jį sukuria pagal gautuosius ``C`` ir
        ``D``.
        + ``memory`` – realios mašinos atmintis.
        + ``address`` – pirmo baito, kuriuo prasideda puslapiavimo įrašas
          atmintyje adresas.
        + ``C`` – kodo segmento dydis blokais.
        + ``D`` – duomenų segmento dydis blokais.
        """

        self.PLR = None
        self.PLBR = None
        self.memory = memory

        if address is not None:
            self.read(address)
        else:
            self.create(D)

    def create(self, D):
        """ Sukuria virtualios mašinos puslapiavimo lentelę. Nustato
        PLR ir PLBR.
        """

        self.PLR = 0
        self.PLBR = 0

        data = []
        # if D < 1:
        #     raise ValueError('Kodo segmento dydis turi būti didesnis už 1.')
        # else:
        #     data.append(ih(D))
        # if D < 0:
        #     raise ValueError('Duomenų segmento dydis turi būti teigiamas.')
        # else:
        #     data.append(ih(D))
        for i in range(PAGER_SIZE, PAGER_SIZE + D):
            data.append(ih(i))
        # for i in range(PAGER_SIZE + C, PAGER_SIZE + C + D):
        #     data.append(ih(i))
        # data.append('0'*0)

        self.memory.put_data(
                self.PLR * BLOCK_SIZE + self.PLR, ''.join(data))

    def read(self, address):
        """ Nuskaito iš atminties virtualios mašinos puslapiavimo lentelę.
        """
        self.PLR, self.PLBR = self.memory.get_address_tuple(address)

    def get_byte(self, offset):
        """ Gražina puslapiavimo lentelės baitą, pasislinkusį nuo pradžios
        per ``offset``.
        """
        return self.memory.get_byte((self.PLR, self.PLBR), offset)

    # def get_code_cell_address(self, virtual_address):
    #     """ Apskaičiuoja realų ląstelės adresą pagal kodo segmento
    #     virtualų adresą.
    #     """
    #
    #     virtual_address = self.memory.get_address_int(virtual_address)
    #     C = hex_to_int(self.get_byte(0) + self.get_byte(1))
    #
    #     min_address = 0
    #     max_address = C * BLOCK_SIZE
    #     if not (min_address <= virtual_address <= max_address):
    #         raise ValueError('Virtualus adresas nepriklauso kodo segmentui.')
    #     virtual_block, cell = self.memory.get_address_tuple(virtual_address)
    #
    #     block = hex_to_int(
    #             self.get_byte(4 + 2 * virtual_block) +
    #             self.get_byte(4 + 2 * virtual_block + 1))
    #     return block, cell

    def get_data_cell_address(self, virtual_address):
        """ Apskaičiuoja realų ląstelės adresą pagal duomenų segmento
        virtualų adresą.
        """
        virtual_address = self.memory.get_address_int(virtual_address)
        D = 16

        min_address = 0
        max_address = D * BLOCK_SIZE
        if not (min_address <= virtual_address <= max_address):
            raise ValueError('Virtualus adresas nepriklauso duomenų segmentui.')
        virtual_block, cell = self.memory.get_address_tuple(virtual_address)
        block = hex_to_int(self.get_byte(2 * (virtual_block)) + self.get_byte(2 * (virtual_block) + 1))
        return block, cell

class RealMemory(object):
    """ Realios mašinos atmintis.
    """

    def __init__(self):
        """ Inicializuoja tuščią atmintį.

          ląstelės reikšmė. Sintaksė: (<blokas>, <ląstelės adresas bloke>).
        """

        self._cells = []
        for i in range(BLOCKS):
            block = []
            for j in range(BLOCK_SIZE):
                block.append(Cell())
            self._cells.append(block)
            #        for i in range(BLOCKS):
            # block = []
            # for j in range(BLOCK_SIZE):
            #     for k in range(WORD_SIZE):
            #         block.append(Cell())
            #     self._cells.append(block)

    def get_address_tuple(self, address):
        """ Grąžina bloko ir elemento bloke adresus.

        Jei ``address`` yra ``tuple`` tipo objektas, tai laikoma, kad
        pirmas elementas ir bloko adresas, o ląstelės bloke. Jei
        ``address`` yra ``int`` tipo objektas, tai bloko adresas
        apskaičiuojamas ``address // BLOCK_SIZE``, o ląstelės bloke
        ``address % BLOCK_SIZE``.
        """


        if isinstance(address, int):
            block = address // BLOCK_SIZE
            cell = address % BLOCK_SIZE
            # print('b', block)
            # print('c', cell)
            # print('a', address)
        else:

            # print('add', address)
            block, cell = address
        return block, cell

    def get_address_int(self, address):
        """ Grąžina globalų adresą.
        Ši funkcija yra atvirkštinė funkcijai ``get_address_tuple``
        """

        if not isinstance(address, int):
            block, cell = address
            address = block * BLOCK_SIZE + cell
        return address

    def _get_cell(self, address):
        """ Grąžina atminties ląstelę, kuri yra nurodyta adresu.
        """

        block, cell = self.get_address_tuple(address)
        # print(block, cell)
        return self._cells[block][cell]

    def __getitem__(self, address):
        """ Grąžina adresu nurodytos ląstelės reikšmę.
        """

        return self._get_cell(address).value

    def __setitem__(self, address, value):
        """ Priskiria adresu nurodytai ląstelei nurodytą reikšmę.
        """
        # print(address, value)
        self._get_cell(address).value = value

    def put_data(self, address, data):
        """ Nurodytu adresu į atmintį pakrauna duomenis ``data``.
        + Jei duomenys netelpa į tą patį bloką, išmeta išimti
          ``ValueError``.
        + Jei duomenys nesidalina lygiai į žodžius, tai lygiuoja
          į kairę ir trūkstamą dalį užpildo tarpais.
        """

        block, cell = self.get_address_tuple(address)
        # Apvalina iki žodžių.
        size = float(len(data))
        fill = int(
                (ceil(size / WORD_SIZE) -
                    floor(size / WORD_SIZE)) * WORD_SIZE)
        data = data + ' ' * fill
        words = [
                data[i:i+WORD_SIZE] for i in range(0, len(data), WORD_SIZE)]
        for i, word in enumerate(words):
            try:
                self[block, cell + i] = word
            except IndexError:
                raise ValueError('Duomenys netelpa į bloką.')

    def get_data(self, address, size):
        """ Grąžina duomenis nuo nurodyto adreso.
        ``size`` – kiek baitų gražinti.
        """

        address = self.get_address_int(address)

        words = size // WORD_SIZE        # Kiek sveikų žodžių reikia
                                        # grąžinti.
        data = []
        for i in range(address, address + words):
            data.append(self[i])
        if words * WORD_SIZE < size:
            # Jei reikia gražinti dar žodžio dalį.
            word = self[address + words]
            data.append(word[:size - words * WORD_SIZE])
        return ''.join(data)

    def get_byte(self, address, offset):
        """ Grąžina baitą, kuris yra nuo žodžio nurodyto ``address``
        paslinktas per ``offset`` baitų.
        """

        address = self.get_address_int(address) + offset // WORD_SIZE
        offset %= WORD_SIZE

        return self[address][offset]

    def set_byte(self, address, offset, value):
        """ Pakeičia baito, kuris yra nuo žodžio nurodyto ``address``
        paslinktas per ``offset`` baitų, reikšmę.
        """

        address = self.get_address_int(address) + offset // WORD_SIZE
        offset %= WORD_SIZE

        word = self[address]
        self[address] = word[0:offset] + value + word[offset+1:]

    def create_virtual_memory(self, code, data, data_size):
        """ Išskiria virtualią atmintį ir į ją įkelia kodą bei duomenis.
        """

        pager = Pager(self, D=data_size)
        # Įkeliamas kodo segmentas.
        vmdata = VirtualMemory(self, pager)

        # print(vmdata)
        clean_code = []
        for i, line in enumerate(code):
            command = line
            clean_code.append(command.strip())

        for i, command in enumerate(clean_code):
            command = command
            command += ' ' * (WORD_SIZE - len(command))
            vmdata[i] = command
            # print(i)

        # # Įkeliamas duomenų segmentas.
        # vmdata = VirtualMemory(self, pager)

        for block in data.keys():
            for word, line in enumerate(data[block]):
                hex_address = f'{block}{word}'
                address = hex_to_int(hex_address)
                line = line.replace('\n', '')
                vmdata[address] = line
            #     print(hex_address)
            # print(block)


        return vmdata



class VirtualMemory(object):
    """ Virtualios mašinos atmintis, duomenų segmentas.
    """

    def __init__(self, memory, pager):
        # memory - paduosime RealMacihne() klases objekta
        # pager - puslapiavimo objektas

        """
        + ``memory`` – realios mašinos atmintis.
        + ``pager`` – puslapiavimo mechanizmo objektas.
        """

        self.memory = memory
        self.pager = pager

    def __getitem__(self, address):
        """ Grąžina adresu nurodytos kodo segmento ląstelės adresą.
        """

        return self.memory[self.pager.get_data_cell_address(address)]

    def __setitem__(self, address, value):
        """ Priskiria adresu nurodytai ląstelei nurodytą reikšmę.
        """

        # print(f's={self.pager.get_data_cell_address(address)}')
        # print('address' , address, value)
        self.memory[self.pager.get_data_cell_address(address)] = value
