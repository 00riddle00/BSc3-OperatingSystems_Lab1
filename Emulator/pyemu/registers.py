#!/usr/bin/python
# -*- coding: utf-8 -*-


""" Modulis, kuriame realizuotos klasės registrų ir atminties ląstelių
emuliacijai.
"""


WORD_SIZE = 8                           # Žodžio dydis yra 8 baitai.


class Cell(object):
    """ Atminties ląstelė. Turi dydį išreikštą simboliais.
    """

    def __init__(self, size=WORD_SIZE):
        """ ``size`` – ląstelės dydis baitais.
        """

        self.size = size
        self._format = '{{: >{0}}}'.format(self.size)
        self._value = '0'*self.size

    def set_value(self, value):
        """ Patikrina ar reikšmė telpa atminties ląstelėje ir jei taip,
        tai ją priskiria. Jei ne tai išmeta ``ValueError``.
        """
        # TODO: Pridėti pranešimo išsiuntimą, jog reikšmė pasikeitė.
        # Tam, kad būtų paprasčiau parašyti grafinę sąsają.

        value = str(value)
        if len(value) <= self.size:
            self._value = self._format.format(value)

        else:
            raise ValueError('Reikšmė netelpa ląstelėje.')
        return self

    def get_value(self):
        """ Grąžina ląstelėje saugomą reikšmę.
        """

        return self._value

    def __str__(self):
        """ Grąžina ląstelėje saugomą reikšmę, kaip ``str`` tipo objektą.
        """

        return str(self._value)

    value = property(get_value, set_value)


class Register(Cell):
    """ Bendro pobūdžio registras.
    """

    def __get__(self, obj, objtype):
        """ Getter'is išorinei klasei. (Žr. „Python descriptor“)
        """

        return self._value

    def __set__(self, obj, value):
        """ Setter'is išorinei klasei. (Žr. „Python descriptor“)
        """

        self.value = value
        return self


class IntegerRegister(Register):
    """ Registras skirtas sveikiesiems skaičiams su ženklu saugoti.
    """

    def __init__(self, size=WORD_SIZE):
        """ ``size`` – registro dydis baitais.
        """

        super(IntegerRegister, self).__init__(size)
        self._format = '{{0:>+{0}}}'.format(self.size)
        self.value = 0

    def set_value(self, value):
        """ Patikrina ar reikšmė yra sveikas skaičius ir ar ji telpa. Tada
        ją priskiria. Klaidos atveju išmeta ``ValueError``.
        """

        value_as_integer = int(value)
        value_as_string = self._format.format(value_as_integer)
        if len(value_as_string) <= self.size:
            self._value = value_as_string
        else:
            raise ValueError('Reikšmė netelpa ląstelėje.')
        return self

    def __int__(self):
        """ Gražina registro reikšmę, kaip sveikąjį skaičių.
        """

        return int(self._value)

    def __add__(self, number):
        """ Gautą skaičių ``number`` sudeda su registro reikšme ir grąžina
        rezultatą.
        """

        return int(self) + int(number)

    def __sub__(self, number):
        """ Gautą skaičių ``number`` atima iš registro reikšmės ir grąžina
        rezultatą.
        """

        return int(self) - int(number)

    def __get__(self, obj, objtype):
        """ Getter'is išorinei klasei. (Žr. „Python descriptor“)
        """

        return int(self)

    value = property(Register.get_value, set_value)


class HexRegister(Register):
    """ Registras skirtas sveikiems neneigiamiems šešioliktainiams
    skaičiams saugoti.
    """

    def __init__(self, size=WORD_SIZE):
        """ ``size`` – registro dydis baitais.
        """

        super(HexRegister, self).__init__(size + 2)
                                        # Kompensuojamas „0x“ dydis.
        self.size = size
        self.value = 0

    def set_value(self, value):
        """ Patikrina ar reikšmė yra sveikas teigiamas skaičius ir ar ji
        telpa. Tada ją priskiria. Klaidos atveju išmeta ``ValueError``.
        """

        value_as_integer = int(value)
        if value_as_integer < 0:
            raise ValueError('Turi būti sveikas teigiamas skaičius.')
        value_as_string = self._format.format(hex(value_as_integer))
        if len(value_as_string) <= self.size + 2:
                                        # Kompensuojamas „0x“ dydis.
            self._value = value_as_string
        else:
            raise ValueError('Reikšmė netelpa ląstelėje.')
        return self

    def __int__(self):
        """ Grąžina registro reikšmę, kaip sveikąjį skaičių.
        """

        return int(self._value, 16)

    def __add__(self, number):
        """ Gautą skaičių ``number`` sudeda su registro reikšme ir grąžina
        rezultatą.
        """

        return int(self) + int(number)

    def __sub__(self, number):
        """ Gautą skaičių ``number`` atima iš registro reikšmės ir grąžina
        rezultatą.
        """

        return int(self) - int(number)

    def __get__(self, obj, objtype):
        """ Getter'is išorinei klasei. (Žr. „Python descriptor“)
        """

        return int(self)

    value = property(Register.get_value, set_value)
