import re
from copy import deepcopy

# regex to match polynomial terms.
REGEX = r'((?P<sign>[+-]?\s?)(?P<number>[0-9]+.[0-9]+)x\^(?P<exponent>[0-9]+))+'


class ParseError(Exception):
    """Triggered when we have a parse error"""


class PolynomialTerm():
    def __init__(self, sign='', number=0, exponent=1):
        self.number = f'{sign.strip()}{number}'
        self.exponent = exponent
        
    @property
    def number(self):
        return self._number
    
    @number.setter
    def number(self, value):
        self._number = float(value)
        
    @property
    def exponent(self):
        return self._exponent
    
    @exponent.setter
    def exponent(self, value):
        value = value.strip()
        self._exponent = value
        
    def __str__(self):
        sign = '+' if self.number >= 0 else ''
        return f'{sign}{self.number}x^1{self.exponent}'
    
    def __repr__(self):
        return str(self)

    def __add__(self, t):
        if self.exponent != t.exponent:
            raise ValueError('Can not add two terms with different exponents')

        return PolynomialTerm(
            '', 
            self.number + t.number, 
            self.exponent
        )

    def __sub__(self, t):
        if self.exponent != t.exponent:
            raise ValueError('Can not substract two terms with different exponents')

        return PolynomialTerm(
            '', 
            self.number - t.number, 
            self.exponent
        )

    def __mul__(self, t):
        return PolynomialTerm(
            '', 
            self.number * t.number, 
            self.exponent + t.exponent
        )

    __rmul__ = __mul__


class Polynomial():
    def __init__(self, terms=[]):
        self.terms = terms

    def contains_exponent(self, exponent):
        for term in self.terms:
            if term.exponent == exponent:
                return True

        return False

    def exponent_index(self, exponent):
        for index, term in enumerate(self.terms):
            if term.exponent == exponent:
                return index

        return None

    def __add__(self, another_polynomial):
        result = deepcopy(self)
        for term in another_polynomial.terms:
            if result.contains_exponent(term.exponent):
                term_index = result.exponent_index(term.exponent)

                if not term_index:
                    # Code should not enter this branch.
                    continue

                result.terms[term_index] += term

            else:
                result.terms.append(term)

        return result

    def __sub__(self, another_polynomial):
        result = deepcopy(self)
        for term in another_polynomial.terms:
            if result.contains_exponent(term.exponent):
                term_index = result.exponent_index(term.exponent)

                if not term_index:
                    # Code should not enter this branch.
                    continue

                result.terms[term_index] -= term

            else:
                result.terms.append(term)

        return result

    def __mul__(self, another_polynomial):
        result = Polynomial()

        for first_term in self.terms:
            for second_term in another_polynomial.terms:
                term_result = first_term * second_term
                sub_polynomial = Polynomial(terms=[term_result])
                result += sub_polynomial

        return result

    __rmul__ = __mul__

    def __str__(self):
        return ' '.join(str(term) for term in self.terms)

    def __repr__(self):
        return ' '.join(str(term) for term in self.terms)


def parse_polynomial(expression):
    """Parse polynomial terms from expression.

    Args:
        expression (str)

    Raises:
        ParseError: raised if we have empty expression
        ParseError: raised if we have unparsed sub expression

    Returns:
        [list of PolynomialTerm]: terms
    """
    matches = re.findall(REGEX, expression)

    if not matches:
        raise ParseError('No terms found')

    terms = []

    for match in matches:
        sub_expression, sign, number, exponent = match

        # Delete parsed sub expression.
        expression = expression.replace(sub_expression, '').strip()

        terms.append(PolynomialTerm(sign, number, exponent))

    # Check we don't have any unparsed sub-expression.
    if expression:
        raise ParseError(f'Unrecognized character combination {expression}')

    return terms


def main():
    # Welcome message.
    print('Program: Welcome to the polynomial calculator.')

    first_polynomial = False
    second_polynomial = False

    # Parsing phase.
    while not (first_polynomial and second_polynomial):
        try:
            # The user did not input yet a valid first polynomial.
            if not first_polynomial:
                print('\nPlease enter the first polynomial')
                expression = input('User: ')
                first_polynomial = parse_polynomial(expression)

            # The user did not input yet a valid second polynomial.
            if not second_polynomial:
                print('\nPlease enter the second polynomial')
                expression = input('User: ')
                second_polynomial = parse_polynomial(expression)

        except Exception as e:
            print(f' Program: ERROR: {e}')

    # Choosing operation.
    exit_program = False

    while not exit_program:
        print(
            '\nProgram: Choose operation: '
            '+ (addition), '
            '- (subtraction), '
            '* (multiplication), '
            'x (exit program)'
        )
        command = input('User: ')
        command = command.lower()

        if command not in ('+', '-', '*', 'x'):
            print('Invalid command')

        if command == 'x':
            exit_program = True
            continue
            
        elif command ==  '+':
            result = Polynomial(first_polynomial) + Polynomial(second_polynomial)
        
        elif command ==  '-':
            result = Polynomial(first_polynomial) - Polynomial(second_polynomial)

        elif command ==  '*':
            result = Polynomial(first_polynomial) * Polynomial(second_polynomial)

        print(f'\nProgram: result= {result}')

    print('Program: Bye')


if __name__ == '__main__':
    main()
