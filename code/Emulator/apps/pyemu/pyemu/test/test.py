#!/usr/bin/python
# -*- coding: utf-8 -*-

""" Testai.
"""

import unittest
from registers import int_to_hex, hex_to_int
from registers import Cell, Register, IntegerRegister, HexRegister
from registers import ChoiceRegister, StatusFlagRegister

class Utils(unittest.TestCase):
    """ Testai pagalbinėms funkcijoms.
    """
    def test_hex_int(self):

        assert int_to_hex(5) == '5'
        assert int_to_hex(10) == 'a'
        assert int_to_hex(5, 2) == '05'
        assert int_to_hex(32, 2) == '20'

        assert hex_to_int('5') == 5
        assert hex_to_int('a') == 10
        assert hex_to_int('05') == 5
        assert hex_to_int('20') == 32

class Registers(unittest.TestCase):
    """ Testai atminties ląstelėms ir registrams.
    """

    def test_cell(self):

        cell2B = Cell(2)
        assert cell2B.value == '00'
        cell2B.value = 0
        assert cell2B.value == ' 0'
        cell2B.value = 13
        assert cell2B.value == '13'
        cell2B.value = 'ab'
        assert cell2B.value == 'ab'
        cell2B.value = 'b'
        assert cell2B.value == ' b'
        cell2B.value = 'š'
        assert cell2B.value == ' š'
        try:
            cell2B.value = 123
        except ValueError as e:
            assert str(e) == 'Reikšmė netelpa ląstelėje.'
        else:
            self.fail('Turėjo būti išmesta išimtis.')

    def test_register(self):

        class A(object):
            reg2B = Register(2)

        a = A()
        assert a.reg2B == '00'
        assert str(a.reg2B) == '00'

        a.reg2B = 0
        assert a.reg2B == ' 0'
        a.reg2B = 13
        assert a.reg2B == '13'
        a.reg2B = 'ab'
        assert a.reg2B == 'ab'
        a.reg2B = 'b'
        assert a.reg2B == ' b'
        a.reg2B = 'š'
        assert a.reg2B == ' š'
        try:
            a.reg2B = 123
        except ValueError as e:
            assert str(e) == 'Reikšmė netelpa ląstelėje.'
        else:
            self.fail('Turėjo būti išmesta išimtis.')
        assert type(a.reg2B) == str

    def test_integer_register(self):

        ir4B = IntegerRegister(4)
        assert ir4B.value == '  +0'

        ir4B.value = 1
        assert ir4B.value == '  +1'
        ir4B.value = -1
        assert ir4B.value == '  -1'
        ir4B.value = '1'
        assert ir4B.value == '  +1'
        ir4B.value = '-1'
        assert ir4B.value == '  -1'
        try:
            ir4B.value = 'a'
        except ValueError as e:
            assert str(e) == 'invalid literal for int() with base 10: \'a\''
        else:
            self.fail('Turėjo būti išmesta išimtis.')
        try:
            ir4B.value = 1234
        except ValueError as e:
            assert str(e) == 'Reikšmė netelpa ląstelėje.'
        else:
            self.fail('Turėjo būti išmesta išimtis.')

        ir4B.value = 1
        assert int(ir4B) == 1
        assert ir4B + 2 == 3
        assert ir4B - 2 == -1

        ir2B = IntegerRegister(2)
        ir2B.value = -1
        assert ir4B + ir2B == 0
        assert ir4B - ir2B == 2

        class A(object):
            reg4B = IntegerRegister(4)
            reg2B = IntegerRegister(2)

        a = A()
        a.reg4B = -1
        assert a.reg4B == -1
        try:
            a.reg4B = 'a'
        except ValueError as e:
            assert str(e) == 'invalid literal for int() with base 10: \'a\''
        else:
            self.fail('Turėjo būti išmesta išimtis.')
        try:
            a.reg4B = 1234
        except ValueError as e:
            assert str(e) == 'Reikšmė netelpa ląstelėje.'
        else:
            self.fail('Turėjo būti išmesta išimtis.')

        a.reg4B = 1
        assert type(a.reg2B) == int
        assert a.reg4B == 1
        assert a.reg4B + 2 == 3
        assert a.reg4B - 2 == -1

        a.reg2B = -1
        assert a.reg4B + a.reg2B == 0
        assert a.reg4B - a.reg2B == 2

    def test_hex_register(self):

        hr4B = HexRegister(4)
        assert hr4B.value == '   0x0'

        hr4B.value = 1
        assert hr4B.value == '   0x1'
        hr4B.value = '1'
        assert hr4B.value == '   0x1'
        try:
            hr4B.value = -1
        except ValueError as e:
            assert str(e) == 'Turi būti sveikas teigiamas skaičius.'
        else:
            self.fail('Turėjo būti išmesta išimtis.')
        try:
            hr4B.value = 'a'
        except ValueError as e:
            assert str(e) == 'invalid literal for int() with base 10: \'a\''
        else:
            self.fail('Turėjo būti išmesta išimtis.')
        try:
            hr4B.value = 0x12345
        except ValueError as e:
            assert str(e) == 'Reikšmė netelpa ląstelėje.'
        else:
            self.fail('Turėjo būti išmesta išimtis.')

        hr4B.value = 1
        assert int(hr4B) == 1
        assert hr4B + 2 == 3
        assert hr4B - 2 == -1

        ir2B = IntegerRegister(2)
        ir2B.value = -1
        assert hr4B + ir2B == 0
        assert hr4B - ir2B == 2

        class A(object):
            reg4B = HexRegister(4)
            reg2B = IntegerRegister(2)

        a = A()
        a.reg4B = 1
        assert a.reg4B == 1
        try:
            a.reg4B = 'a'
        except ValueError as e:
            assert str(e) == 'invalid literal for int() with base 10: \'a\''
        else:
            self.fail('Turėjo būti išmesta išimtis.')
        try:
            a.reg4B = 0x12345
        except ValueError as e:
            assert str(e) == 'Reikšmė netelpa ląstelėje.'
        else:
            self.fail('Turėjo būti išmesta išimtis.')

        a.reg4B = 1
        assert type(a.reg2B) == int
        assert a.reg4B == 1
        assert a.reg4B + 2 == 3
        assert a.reg4B - 2 == -1

        a.reg2B = -1
        assert a.reg4B + a.reg2B == 0
        assert a.reg4B - a.reg2B == 2

    def test_choice_register(self):

        cr = ChoiceRegister([1, 2])
        assert cr.size == 1
        assert cr.value == '1'
        cr.value = 2
        assert cr.value == '2'
        cr.value = '1'
        assert cr.value == '1'
        try:
            cr.value = 3
        except ValueError as e:
            assert str(e) == 'Nežinomas pasirinkimas.'
        else:
            self.fail('turėjo būti išmesta išimtis.')

        cr = ChoiceRegister(['a', 'bb', 'c'])
        assert cr.size == 2
        assert cr.value == ' a'
        cr.value = 'bb'
        assert cr.value == 'bb'
        cr.value = 'a'
        assert cr.value == ' a'
        cr.value = ' c'
        assert cr.value == ' c'

    def test_status_flag_register(self):

        sf = StatusFlagRegister()
        assert sf.CF == False
        assert sf.ZF == False
        assert sf.SF == False
        assert sf.OF == False
        try:
            sf.NF
        except AttributeError as e:
            assert str(e) == 'Nežinomas požymis.'
        else:
            self.fail('turėjo būti išmesta išimtis.')

        sf.CF = 1
        assert sf.CF == True
        try:
            sf.NF = 1
        except AttributeError as e:
            assert str(e) == 'Nežinomas požymis.'
        else:
            self.fail('turėjo būti išmesta išimtis.')

        class A(object):
            sf = StatusFlagRegister()

        a = A()
        a.sf.CF = 1
        a.sf.ZF = 1
        a.sf.SF = 1
        a.sf.OF = 1
        assert a.sf.CF == 1
        assert a.sf.ZF == 1
        assert a.sf.SF == 1
        assert a.sf.OF == 1

if __name__ == '__main__':
    unittest.main()
