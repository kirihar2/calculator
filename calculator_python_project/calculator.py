import _pydecimal
import sys
import operator
import decimal
from operatorPrecedence import OperatorPrecedence


class Calculator(object):
    def __init__(self, array, precision):
        self._availableOperators = {'+': OperatorPrecedence(operator.add, 1), '-': OperatorPrecedence(operator.sub, 1),
                                    '*': OperatorPrecedence(operator.mul, 2),
                                    '/': OperatorPrecedence(operator.truediv, 2)}
        self._array = array
        try:
            self._precision = int(precision)
            _pydecimal.setcontext(_pydecimal.Context(prec=precision, rounding=_pydecimal.ROUND_HALF_UP))
            _pydecimal.getcontext().clear_flags()
        except ValueError:
            print("Please enter valid precision for decimals. Your value was: " + precision)

    def is_operator(self, ch):
        return ch in self._availableOperators

    def operator_precedence_not_greater(self, operator_input):
        try:
            if operator_input in self._availableOperators and len(self._array) > 0:
                if self._array[-1] in self._availableOperators:
                    return True if self._availableOperators[operator_input] <= self._availableOperators[
                        self._array[-1]] else False
        except IndexError:
            print("index error raised, array has size equal to 0")
            raise IndexError
        except KeyError:
            print("Operator " + operator_input + " not found in the comparison")
            raise KeyError

    def pop_array(self):
        try:

            return self._array.pop()
        except IndexError:
            raise IndexError

    def convert_infix_to_postfix(self, infix):
        ret = []
        prev_was_number = False
        for ind in range(len(infix)):
            ch = infix[ind]
            if '-' == ch:
                if ind + 1 < len(infix):
                    # if next value is a number then part of negative number
                    if not self.is_operator(infix[ind + 1]):
                        # interpret as a multiplication with -1
                        ret.append('-1')
                        self._array.append('*')
                # invalid placement of - at the end of the expression
                else:
                    print("invalid placement of - at the end of the expression")
                    raise Exception
            elif '.' is ch or not self.is_operator(ch):
                if prev_was_number:
                    ret[-1] = ret[-1] + ch
                else:
                    ret.append(ch)
                prev_was_number = True

            else:
                try:
                    while not len(self._array) == 0 and self.operator_precedence_not_greater(ch):
                        ret.append(self.pop_array())
                    self._array.append(ch)
                except IndexError:
                    self.clean_up()
                    raise IndexError
                except KeyError:
                    self.clean_up()
                    raise KeyError
                prev_was_number = False

        while not len(self._array) == 0:
            # length of _array checked in the loop after each pop index exception will not be raised here
            ret.append(self.pop_array())
        return ret

    @staticmethod
    def is_number(value):
        try:
            float(value)
        except ValueError:
            return False
        return True

    # value is inputted as a Decimal
    def rounding_up(self, value):
        return str(round(value, self._precision))

    # value is inputted as a Decimal
    @staticmethod
    def rounding_to_general(value):
        return '{0:g}'.format(value)

    def rounding(self, value):
        decimal_rounding = self.rounding_up(value)
        general_rounding = self.rounding_to_general(float(decimal_rounding))
        if float(value) == float(general_rounding):
            return general_rounding
        return decimal_rounding

    def calculate_postfix(self, postfix_list):
        number_list = []
        for ch in postfix_list:
            if self.is_number(ch):
                number_list.append(ch)
            else:
                try:
                    a = float(number_list.pop())
                    b = float(number_list.pop())
                    number_list.append(decimal.Decimal(self._availableOperators[ch](b, a)))
                except IndexError:
                    self.clean_up()
                    print("Invalid syntax detected")
                    raise IndexError
                except KeyError:
                    self.clean_up()
                    print("Invalid operator detected: "+ch)
                    raise KeyError
        try:
            return self.rounding(number_list[-1])
        except IndexError:
            self.clean_up()
            print("Invalid syntax detected, no number returned")
            raise IndexError

    def evaluate(self,calc,input_to_calculate):
        if "q" == input_to_calculate.lower():
            print("Exiting...")
            sys.exit()
        else:
            if '=' not in input_to_calculate or input_to_calculate.index('=') < len(input_to_calculate) - 1:
                print('Enter = operator at the end')
                raise ValueError
            # Any whitespace in between formula or preceding whitespace ignored
            input_to_calculate = ''.join(input_to_calculate.strip().split(' '))
            input_to_calculate = input_to_calculate[:-1]
            try:
                print(calc.calculate_postfix(calc.convert_infix_to_postfix(input_to_calculate)))
            except IndexError:
                raise IndexError
            except ValueError:
                raise ValueError
            except KeyError:
                raise KeyError

    def clean_up(self):
        if len(self._array) > 0:
            self._array = []


def main():
    precision = 16
    calc = Calculator([], precision)
    while True:
        # Trailing white space removed
        input_to_calculate = input().strip()

        if input_to_calculate is None:
            print("Please enter valid formula to evaluate")
            continue
        try:
            print(calc.evaluate(calc,input_to_calculate))
        except IndexError:
            continue
        except ValueError:
            continue
        except KeyError:
            continue



if __name__ == "__main__":
    main()
