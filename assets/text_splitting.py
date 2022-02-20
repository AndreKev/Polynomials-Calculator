# ipmort digits from the string module for character recognization
from string import digits as dg

from polynomials import Polynomial, X
from config import variables

import operator
"""
BODMAS
Explain the priority of BODMAS
    
"""

numerals = dg + '.'

braces = [ '{', '}' ]
precedence = {
    '-' : 0,
    '+' : 0,
    '*' : 1,
    '/' : 1,
    '^' : 2
}

operation = {
    '+' : operator.add,
    '-' : operator.sub,
    '*' : operator.mul,
    '^' : operator.pow,
    '/' : operator.truediv
}

def normalize(string):
    copy = string[::]
    string = string.replace(' ', '')
    string = string.replace('--', '+')
    string = string.replace('++', '+')
    string = string.replace('-+', '-')
    string = string.replace('+-', '-')
    return string if string == copy else normalize(string)
def tokenizer(string):
    string = normalize(string)
    stack = ''
    star = False
    current = 0
    length = len(string)
    """if length:
                    if string[0] in '+-':
                        yield '0'"""
    while(current < length):
        if isbinaryOperator(string[current]) or string[current] in braces:
            if stack != '':
                yield stack
                stack = ''
                if string[current] == braces[0]:
                    yield '*'
                elif string[current] == braces[1]:
                    if current+1 < length and not isbinaryOperator(string[current+1]) and string[current+1] != braces[1]:
                        star = True
            if current and string[current] in '+-':
                if string[current-1] in (braces[0]+'+'):
                    yield '0'
                elif string[current-1] in '-':
                    yield '1'
                    yield '*'
            else:
                if string[current] in '+-':
                    yield '0'
            yield string[current]
            if star: 
                yield '*'
                star = False
        elif (string[current] in numerals):
            stack += string[current]
        elif (string[current] in variables):
            if stack != '':
                yield stack
                yield '*'
                yield string[current]
                stack = ''
            elif current!=0 and (string[current-1] in variables):
                yield '*'
                yield string[current]
            else : stack += string[current]
        current += 1
    if stack != '':
        yield stack

def infix_to_postfix(tokens):
    sOperators = []
    sOperands  = []
    for token in tokens:
        if (isdigit(token)) or (token in variables):
            sOperands.append(token)
        elif isbinaryOperator(token):
            if not len(sOperators) == 0:
                while (
                        sOperators[-1] != braces[0] and
                        (
                            precedence.get(sOperators[-1], -1) > precedence.get(token, -1) or
                            (
                                precedence.get(sOperators[-1]) == precedence.get(token, -1) and
                                isleftAssociative(token)
                            )
                        )
                ):
                    sOperands.append(sOperators.pop())
                    if len(sOperators) == 0: break
            sOperators.append(token)
        elif token == braces[0]:
            sOperators.append(braces[0])
        elif token == braces[1]:
            while (sOperators[-1] != braces[0]):
                assert not len(sOperators) == 0
                sOperands.append(sOperators.pop())
            del sOperators[-1]
    while not len(sOperators) == 0:
        sOperands.append(sOperators.pop())
    return sOperands

def evaluate_postfix(postfix):
    #print('the postfix is ', postfix)
    expression = postfix.copy()
    expression = computerise(expression)
    #print(expression, '**')
    current = 0
    while len(expression) != 1 and current < len(expression):
        if isbinaryOperator(expression[current]):
            #print(expression[current])
            expression[current] = operation[expression[current]](expression[current -2], expression[current-1])
            del expression[current -1]
            del expression[current -2]
            #print(expression)
            current -= 2
        else:
            current += 1
    return expression[0] if isinstance(expression[0], Polynomial) else Polynomial(expression[0])

def computerise(expression0):
    expression = expression0.copy()
    i = 0
    length = len(expression)
    while i < length:
        if expression[i] in variables:
            expression[i] = X
        elif isbinaryOperator(expression[i]) or expression[i] in braces:
            pass
        else:
            try:
                expression[i] = float(expression[i])
            except Exception:
                raise Exception("Expression not computerisable")
        i += 1
    return expression 

def isleftAssociative(operator):
    return True if operator != '^' else False

def isbinaryOperator(object):
    return True if object in list(operation.keys()) else 0  # In case we receive a non hashable object

def isdigit(object):
    try:
        cast = float(object)
        return 1
    except:
        return 0

if __name__ == '__main__':
    # to test tje parser effectiveness
    braces = [ '(', ')' ]
    test = ['(1-25X+9 - 69/69.0)', '1-(1+2)+13X', '2x-45(45+98x^89)X', 'XX', '2x + 3y']
    test0 = ['-X+-3']
    def test_on(test):
        for string in test:
            print("Test :", string, '=', end=' ')
            output = []
            for i in tokenizer(string):
                print(i, end=' ')
            print()
            for i in tokenizer(string):
                output.append(i)
            print("\nTokenized : ", output)
            postfix = infix_to_postfix(output)
            print("Postfix : ",postfix)
            result = evaluate_postfix(postfix)
            print(result)
            print()

    test_on(test0)
