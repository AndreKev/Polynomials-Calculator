# Built-in modules
from math import sqrt as sq, pow
from decimal import Decimal

# User defined modules
from config import var, digits, inf
from config import R, E


"""def get_error(key, error_type):
        if error_key == "mul":
            if erroy_key in "-+/*":
                pass"""
# Our main class exceptions
class PolynomialException(Exception):
    def __init__(self, error_key=None):
        self.error_message = ""
        self.error_key = error_key
            
# Our derived Exceptions
class InvalidPolynomialAdditionError(Exception):
    def __init__(self):
        super().__init__(self)
        self.error_key = 0
class AdditionError(InvalidPolynomialAdditionError):
    def __init__(self):
        super().__init__(self)


class InvalidPolynomialMultiplicationError(Exception):
    def __init__(self):
        super().__init__(self)
        self.error_key = 1
class MultiplicationError(InvalidPolynomialMultiplicationError):
    def __init__(self):
        super().__init__(self)

class InvalidPolynomialPowerError(Exception):
    def __init__(self):
        super().__init__(self)
        self.error_key = 2
class Powererror(InvalidPolynomialPowerError):
    def __init__(self):
        super().__init__(self)

# The Polynomial class
class Polynomial():
    def __init__(self, val=0, deg=0, _next=None):
        self.val = val
        self.deg = deg
        self.next = _next

    def check(self):
        if not (isnumber(self.val) and isinstance(self.deg, int) and ((self.next == None) or isinstance(self.next, Polynomial))):
            return 0
        elif self.next is None:
            return 1
        return self.next.check()

    def create_next(self, val=0, deg=0, _next=None):
        self.next = Polynomial(val, deg, _next)

    def set_val(self, val):
        self.val = val

    def set_deg(self, deg):
        self.deg = deg

    def set_vd(self, val, deg):
        self.val = val
        self.deg = deg

    def apply(self, x):
        if self.next is None:
            if self.deg == 0:
                return self.val
            else:
                return self.val*(x**self.deg)
        else:
            return self.val*(x**self.deg) + self.next.apply(x)

    def copy(self):
        p = Polynomial(self.val, self.deg)
        if self.next is not None:
            p.next = self.next.copy()
        return p

    def mul_copy(self, coef):
        p = Polynomial(coef*self.val, self.deg)
        if self.next is not None:
            p.next = self.next.mul_copy(coef)
        return p

    def is_null(self):
        if self.val != 0:
            return 0
        elif self.next is None:
            return 1
        else:
            return self.next.is_null()

    def degree(self):
        if self.is_null():
            return -255
        elif self.next is None :
            return self.deg
        else:
            return max(self.deg, self.next.degree())

    def divise(self, other):
        if isinstance(other, Polynomial):
            if self.deg == other.deg:
                if self.next is None and other.next is None:
                    return 1 if self.val % other.val == 0 else 0
                elif self.val % other.val == 0:
                    return (self.next.divise(other.next))
                else:
                    return 0
            else:
                return 0
        elif isnumber(other):
            if self.next is None:
                return 1 if self.val % other == 0 else 0
            elif self.val % other == 0:
                return self.next.divise(other)
            else:
                return 0
        else:
            return 0

    def factorise(self, mode = "compact"):
        solutions = self.roots()
        if solutions == E or solutions == R:
            return self.__repr__()
        elif mode.strip() == "extend":
            factorised_form = ''
            for i in solutions:
                if i < 0:
                    factorised_form += f"({var} + {abs(i)})"
                elif i == 0:
                    factorised_form += f"({var})"
                else:
                    factorised_form += f"({var} - {abs(i)})"
            factorised_form = factorised_form.replace('(', '{')
            factorised_form = factorised_form.replace(')', '}') 
            return str(self.val) + factorised_form if self.val != 1 else factorised_form          # a(x+a)(x+b)
        elif mode.strip() == "compact":
            uniques = list(set(solutions))
            sol_deg = {}
            factorised_form = ""
            i=0
            while i < len(uniques):
                sol = uniques[i]
                deg = solutions.count(sol)
                if isinstance(sol, complex):
                    if uniques[i+1] == sol.conjugate():
                        SOR = 2 * sol.real
                        POR = sol.real**2 + sol.imag**2
                        if SOR > 0:
                            if POR != 0:
                                factorised_form += f"({var}^2 + {SOR}{var} + {POR})"
                            else:
                                factorised_form += f"({var}^2 + {SOR}{var})"
                        elif SOR == 0:
                            factorised_form += f"({var}^2 + {POR})"  # if SOR == 0 the POR can not equal 0 since the roots are complex
                        else:
                            factorised_form += f"(({var}^2 - {abs(SOR)}{var} + {POR})^{deg})"
                        i +=1 
                    else:
                        raise Exception(" Roots problems ")
                else:
                    if sol < 0:
                        factorised_form += f"({var} + {abs(sol)})"
                    elif sol == 0:
                        factorised_form += f"({var})"
                    else:
                        factorised_form += f"({var} - {abs(sol)}"
                    if deg != 1:
                        factorised_form += f"^{deg}"
                        factorised_form =  f"({factorised_form})"
                i+=1
            factorised_form = factorised_form.replace('(', '{')
            factorised_form = factorised_form.replace(')', '}') 
            return factorised_form
        

    def roots(self):
        # If we are asked to determine Pol1 == Pol2 we instead look for Pol1 - Pol2 == 0
        deg = self.degree()
        solutions = []
        if deg == 0:
            if self.val == 0:
                return R
            else:
                return solutions
        elif deg == 1:
            if self.next is None:
                solutions.append(0)
                return solutions
            else:
                solutions.append((-self.next.val)/self.val)
                return solutions
        elif deg == 2:
            if self.next is None:
                solutions.append(0); solutions.append(0)
                return solutions
            else:
                if self.next.next is None:
                    if degree(self.next) == 1:
                        solutions.append(0)     # Complete the division function
                        p = Polynomial()
                        p = p.insert(self.val, self.deg-1)
                        p = p.insert(self.next.val, self.next.deg-1)
                        solutions.extend(p.roots())
                        return solutions
                    else:
                        div = (-self.next.val)/self.val
                        solutions.extend([sqrt(div), -sqrt(div)])
                        return solutions
                else:
                    a, b, c = self.val, self.next.val, self.next.next.val
                    delta = b*b -4*a*c
                    if delta < 0:
                        re = -b/(2*a)
                        im = sqrt(-delta)/(2*a)
                        im = round(im, 4)
                        solutions.append(complex(re, im))
                        solutions.append(complex(re, -im))
                        return solutions
                    else:
                        x1 = (-b+sqrt(delta))/(2*a)
                        x2 = (-b-sqrt(delta))/(2*a)
                        solutions.extend([x1, x2])
                        return solutions
        elif deg == 3:
            if self.next is None:
                return [0, 0, 0]
            if degree(self.next) == 2:
                if self.next.next is None:
                    print(self/(Polynomial(1,1)**2))
                    return (self/(Polynomial(1,1)**2))[0].roots() + [0, 0]
                elif degree(self.next.next) == 1:
                    if self.next.next.next is None:
                        return (self/Polynomial(1,1))[0].roots()+[0]
                    else:
                        print('Case all coefficients are not null : ', self)
                        p = self/self.val
                        a, b, c = p.next.val, p.next.next.val ,p.next.next.next.val
                        k = a/3
                        r, q = b-((a**2)/(3)), c - b*k + 2*(a**3)/(27)
                        print('k', k, 'r', r, 'q', q)
                        y = (Polynomial(1,1)**3 + r*Polynomial(1,1) + q)
                        print("The polynomial is converted to : ", y)
                        y = y.roots()[0]
                        print('y is', y, 'k is', k)
                        print('The real root is :', y-k)
                        return [y-k] + (p/(Polynomial(1,1)-(y-k))).roots()
                else:
                    q = self.copy()
                    print(q)
                    q.next.next = Polynomial(0, 1, q.next.next)
                    print(q, 'null inserted', q.val, q.next.val, q.next.next.val, q.next.next.next.val)
                    return q.roots()
            elif degree(self.next) == 1:
                if self.next.next is None:
                    print("Case : ax^3 + bx, exiting...")
                    return (self/Polynomial(1,1)).roots() + [0]
                else:
                    p = self.copy()/self.val
                    print(p, 'csse : ax^3+bx+c')
                    b = p.next.val
                    c = p.next.next.val
                    delta = (c**2)+((4*b**3)/27)
                    print('delta', delta)
                    if delta >= 0:
                        print("Case delta positive")
                        y= cbrt((-c-sqrt(delta))/2)+cbrt((-c+sqrt(delta))/2)
                        print('y', y)
                        # If y is real then continue else conjugate
                        if isinstance(y, complex):
                            print(y, 'and', y**3)
                        else:
                            print(p/(Polynomial(1,1)-y))
                            return [y] + (p/(Polynomial(1,1)-y)).roots()
                    else:
                        print('Case delta negative')
                        x1 = cbrt((-c-complex(0, sqrt(-delta)))/2) + cbrt((-c+complex(0, sqrt(-delta)))/2)
                        x2 = x1.conjugate()
                        SOR  = (x1+x2).real
                        POR  = (x1*x2).real
                        print('Somme of roots', SOR, 'Product of roots', POR)
                        y = Polynomial(1,1)**2 - (SOR)*Polynomial(1,1) + POR
                        return (p/y).roots() + [x1, x2]
            else:
                p = self/self.val
                print(p)
                return [cbrt(-p.next.val) for _ in range(3)]
        elif (degree(self) == 2*degree(self.next)) and degree(self.next.next) == 0:
            power = degree(self)/2
            y = Polynomial(self.val, 2) + Polynomial(self.next.val, 1) + self.next.next.val
            print("The y is", y)
            print("The solutions of the polynomial y is", y.roots())
            solutions.extend(y.roots())
            for i in range(len(solutions)):
                solutions[i] = solutions[i]**(1/power)
            print("The solutions are :", solutions)
            return solutions
        else:
            return None
            
    def __repr__(self):
        """
        (None) -> None
        Description:
            The representation of the monomial class
        """
        deg, val = self.deg, self.val
        if val == 0:
            output = '0'
        elif val == 1:
            if deg == 1 : 
                output = f'{var}'
            elif deg == 0:
                output = '1'
            else:
                output = f'{var}^{deg}'
        elif val == -1:
            if deg == 1 : 
                output = f'-{var}'
            elif deg == 0:
                output = '-1'
        else:
            if deg == 0 :
                if int(val) != val:
                    output = '%f'%val
                else:
                    output = '%d'%val
            else:
                if int(val) != val:
                    output = f'%.{digits}f{var}'%val if deg == 1 else f'%.{digits}f%s^%d'%(val, var, deg)
                else:
                    output = '%d%s'%(val, var) if deg == 1 else '%d%s^%d'%(val, var, deg)
        if self.next is not None:
            if self.next.val == 0:
                if self.next.next is None:
                    pass
                else:
                    output += ' + ' + self.next.next.__repr__()
            else:
                output += ' + ' + self.next.__repr__()
        del deg, val
        output = output.split(" ")
        i = 0
        length = len(output)
        while i < length:
            if output[i][0] == '-' and i>1:
                if output[i-1] == '+':
                    output[i-1] = '-'
                    output[i] = output[i][1:]
            i += 1
        return " ".join(output)

    def insert(self, val, deg=0, acceptNull=False):
        """
            DESCR: Insert a tuple of (val, degree) is the Polynomial
        """
        assert deg >= 0 and isnumber(val) and isinstance(deg, int)
        if val == 0 and not acceptNull: return self.copy()
        _self = self.copy()
        if _self.deg == deg:
            _self.val += val
        elif _self.deg > deg:
            if _self.next is None:
                _self.create_next(val, deg)
            else:
                _self.next = self.next.insert(val, deg)
        else:
            _self = Polynomial(val, deg, _next=self.copy())
        return _self.copy()

    def ninsert(self, val, deg=0):
        return self.insert(val, deg, True)

    def __len__(self):
        length = 0
        p = self
        while p is not None:
            length += 1
            p = p.next
        return length
    
    def clean(self):
        p = self.copy()
        while p.val == 0:
            p = p.next
            if p is None: break
        if p is not None:
            q = Polynomial(p.val, p.deg)
            p = p.next
            while p is not None:
                if p.val != 0:
                    q = q.insert(p.val, p.deg)
                p = p.next
        else:
            q = Polynomial()
        return q
            
    def __add__(self, other):
        
        if other is None:
            return self.copy()
        elif isinstance(other, Polynomial):
            _self = self.copy()
            _self = _self.insert(other.val, other.deg) + other.next
            return _self.clean()
        elif isinstance(other, float) or isinstance(other, int):
            return self.copy().insert(val=other, deg=0).clean()
        else:
            print("InvalidPolynomialAdditionError : Cannot add with {} of {}".format(other, type(other)))
            raise InvalidPolynomialAdditionError
    def __radd__(self, other):
        return self.__add__(other)
    def __iadd__(self, other):
        return self.__add__(other)
    def __pos__(self):
        return self.copy()
    
    def __sub__(self, other):
        """
            DESCR :
                Overloading the - operator of substraction
                Substraction of two monomials.
                    Polynomial - Polynomial -> Polynomial
        """
        if other is None:
            return self.copy().clean()
        elif isinstance(other, Polynomial):
            _self = self.copy()
            _self = _self.insert(-other.val, other.deg) - other.next
            return _self.clean()
        elif isinstance(other, float) or isinstance(other, int):
            return self.copy().insert(val=-other, deg=0).clean()
        else:
            print("InvalidPolynomialAdditionError : Cannot add with {} of {}".format(other, type(other)))
            raise InvalidPolynomialAdditionError
    def __rsub__(self, other):
        return -self.__sub__(other)
    def __isub__(self, other):
        return self.__sub__(other)
    def __neg__(self):
        return self.mul_copy(-1)

    def __mul__(self, other):
        if other is None:
            return None
        elif isinstance(other, int) or isinstance(other, float):
            return self.mul_copy(other)
        elif isinstance(other, Polynomial):
            if self.is_null() or other.is_null():
                return Polynomial()
            else:
                p = self.copy()
                new_mono = Polynomial()
                while p is not None:
                    q = other.copy()
                    while q is not None:
                        new_mono = new_mono.insert(p.val*q.val, p.deg+q.deg)
                        q = q.next
                    p = p.next
                if p is None: return new_mono
        else:
            print(f"Multiplication of Polynomials and Monomials with type {type(other)} : {other} is not supported")
            raise InvalidPolynomialMultiplicationError 
        return other
    def __rmul__(self, other):
        return self.__mul__(other)
    def __imul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not (isinstance(other, int) or isinstance(other, float)):
            print("Dividing polynomial", self, "by", other)
            g = self.copy()
            f = other.copy()
            q = Polynomial(0,0)
            print(f, g)
            while degree(f) <= degree(g):
                print(f.degree(), g.degree())
                q = q.insert(g.val/f.val, g.degree()-f.degree())
                g = g - f*(g.val/f.val)*Polynomial(1, g.degree()-f.degree())
            print('Result of division of', self, 'by', other,' is ', q, 'remainder', g)
            #return [ q, g, f]          # Will be used when implementing fractions
            return q
        else:
            return self.mul_copy(1/other)

    def integrate(self):
        q = Polynomial()
        p = self.copy()
        while p is not None:
            if p.val!= 0:
                q = q.insert(p.val/(p.deg+1), p.deg+1)
            p = p.next
        return q

    def differentiate(self):
        q = Polynomial()
        p = self.copy()
        while p is not None:
            if p.deg != 0:
                q = q.insert(p.val*p.deg, p.deg-1)
            p = p.next
        return q

    def __pow__(self, other):
        if not (isinstance(other, int) or isinstance(other, float)):
            print("You can only raise a polynomial to a real number power")
            raise InvalidPolynomialPowerError
        elif other == 0:
            if self.is_null():
                print("You cannot raise the null polynomial to the zero power")
                raise InvalidPolynomialPowerError
            else:
                return Polynomial(1)
        else:
            _self = self.copy()
            result = self.copy()
            i = other-1
            while (i > 0):
                result = result * _self
                i -= 1
            return result
    def __ipow__(self, other):
        return self.__pow__(other)
        
    def __eq__(self, other):
        if isinstance(other, Polynomial):
            if self.val != other.val or self.deg != other.deg:
                return False
            else:
                return self.next == other.next
        elif (isinstance(other, int) or isinstance(other, float)) and self.degree()==0:
            return self.val == other
        else:
            return False
        
    def __neq__(self, other):
        return not self.__eq__(other)

def isnumber(object):
    if isinstance(object, float) or isinstance(object, int):
        return 1
    else:
        return 0

def ispolynomial(object):
    return isinstance(object, Polynomial)
    
def degree(object):
    if object is None:
        return inf
    elif isnumber(object):
        return 0 if object != 0 else inf
    elif isinstance(object, Polynomial):
        return object.degree()
    else:
        return None

def cbrt(object):
    if not isnumber(object) and not isinstance(object, complex):
        raise Exception(f"Cannont compute the cube root of a non number of type {type(object)}")
    else:
        if isinstance(object, complex): return object**(1/3)
        return object**(1/3) if object >= 0 else -(abs(object)**(1/3))
def sqrt(object):
    if isnumber(object):
        return sq(object) if object >= 0 else complex(0, sq(abs(object)))
    elif isinstance(object, complex):
        if object.imag == 0:
            return sq(object.real)
        else:
            a = object.real
            b = object.imag
            p = (a+sq(a*a+b*b))
            if p < 0:
                p = (a-sq(a*a+b*b))
            a = sq(p/2)
            b = b/(2*a)
            return complex(a, b)
    
# Polynomial constants
X = Polynomial(1, 1)
def roots(polynomial):
    return polynomial.roots()
    
if __name__ == "__main__":
     one = Polynomial(1, 2)
     one = one.insert(2, 1)
     one = one.insert(1)
     two = Polynomial(5, 1)
     #one = 1.0*X**3 -24.0*X -72.0
     #one = X**3 + 3*X**2 - 21*X - 95
     one = (X**3 + 1.5000*X**2 + -6*X + -6.500000)
     x = X
     p = 2*x**6-2*x**3+1
     print(p.roots())
