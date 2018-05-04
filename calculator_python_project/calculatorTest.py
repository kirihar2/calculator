import unittest
from calculator import Calculator


class CalculatorTest(unittest.TestCase):
    precision = 16
    calc = Calculator([], precision)

    def test_operator_precedence_through_operatorPrecedenceNotGreater(self):
        temp_calc = Calculator(["+"], self.precision)
        self.assertFalse(temp_calc.operator_precedence_not_greater('*'))
        self.assertFalse(temp_calc.operator_precedence_not_greater('/'))
        self.assertTrue(temp_calc.operator_precedence_not_greater('-'))
        self.assertTrue(temp_calc.operator_precedence_not_greater('+'))

    def test_simple_addition_convertingInfixToPostfix(self):
        returned_postfix = self.calc.convert_infix_to_postfix("12+2")
        self.assertEqual(returned_postfix, ["12", "2", "+"])
        self.assertEqual(self.calc.calculate_postfix(returned_postfix), '14')

    def test_negative_number_intake(self):
        returned_postfix = self.calc.convert_infix_to_postfix("-12+-2")
        self.assertEqual(returned_postfix, ["-1", "12", "*", "-1", "2", "*", "+"])
        self.assertEqual(self.calc.calculate_postfix(returned_postfix), '-14')

    def test_decimal_in_convertingInfixToPostfix(self):
        self.assertEqual(self.calc.convert_infix_to_postfix("12.0+2"), ["12.0", "2", "+"])

    def test_decimal_correctly_converted_to_integer(self):
        returned_postfix = self.calc.convert_infix_to_postfix("12.0+2")
        evaluated_answer = self.calc.calculate_postfix(returned_postfix)
        self.assertEqual(evaluated_answer, '14')

    def test_decimal_correctly_rounded_to_sixteen_decimal_places(self):
        returned_postfix = self.calc.convert_infix_to_postfix("12.0+0.49999999999999999")
        evaluated_answer = self.calc.calculate_postfix(returned_postfix)
        self.assertEqual(evaluated_answer, '12.5')

    def test_decimal_correctly_rounded_to_sixteen_decimal_places_then_to_integer(self):
        returned_postfix = self.calc.convert_infix_to_postfix("12.0+0.99999999999999999")
        evaluated_answer = self.calc.calculate_postfix(returned_postfix)
        self.assertEqual(evaluated_answer, '13')

    def test_decimal_correctly_keep_up_to_sixteen_decimal_places(self):
        returned_postfix = self.calc.convert_infix_to_postfix("-5*5/3")
        evaluated_answer = self.calc.calculate_postfix(returned_postfix)
        self.assertEqual(evaluated_answer, '-8.3333333333333339')
        # Due to decimal precision in python cannot accurately express decimals to 16 digits

    def test_simple_precedence_convertingInfixToPostfix(self):
        self.assertEqual(self.calc.convert_infix_to_postfix("A*B+C/D"), ["A", "B", "*", "C", "D", "/", "+"])

        # def test_raised_KeyError_With_InvalidOperator(self):
        #     with self.assertRaises(KeyError) as context:
        #         self.calc.convert_infix_to_postfix("(")
        #     self.assertTrue(context.exception,KeyError)


if __name__ == '__main__':
    unittest.main()
