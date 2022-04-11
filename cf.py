import itertools

import sympy
from sympy import Abs, pi, floor
import sympy.ntheory.continued_fraction as cf_mod

def main():
    N=200
    pi_cf_list = list(pi_recurrance_1(N))
    prev_pi_cf = 0
    for i in range(0, N):
        cur_pi_cf = pi_cf_n(i)
        diff = Abs(cur_pi_cf - prev_pi_cf)
        diff_ln = -sympy.ln(diff).evalf()
        diff_log = -sympy.ln(diff, 10).evalf()
        print(f"{i}: {cur_pi_cf}, {pi_cf_list[i]}, e:{diff_ln:.2f}, 10:{diff_log:.2f}")

        prev_pi_cf = cur_pi_cf

class RequirementError(RuntimeError): pass
def require(cond, msg):
    if not cond:
        raise RequirementError(msg)

def pi_cf_n(n):
    """
    Uses the definition of pi as

        inf
    3 + K   (2x-1)**2/6
        x=1

    but generates and returns the values where instead of an infinite
    continued fraction, it is a finite continued fraction with n terms
    """
    require(n >= 0, f'failed: n:{n} >= 0')
    
    sub_frac = 0
    for x in range(n,0,-1):
        denom = 6 + sub_frac

        numer = (2*x - 1)**2
        sub_frac = numer/denom

    return 3 + sub_frac

def pi_cf_n_recurrance(n):
    """
    Uses the definition of pi as

        inf
    3 + K   (2x-1)**2/6
        x=1

    and the general continued fraction recurrance
    """
    A_prev = 1
    B_prev = 0
    B_cur = 1
    A_cur = 3
    yield A_cur/B_cur
    for i in range(1, n):
        a_next = (2*i-1)**2
        b_next = 6
        A_next = b_next*A_cur+a_next*A_prev
        B_next = b_next*B_cur+a_next*B_prev
        A_prev = A_cur
        B_prev = B_cur
        A_cur = A_next
        B_cur = B_next
        yield A_cur/B_cur

def pi_recurrance_1(n):
    """
    Uses the definition of pi as

        inf
    3 + K   (2x-1)**2/6
        x=1

    and the general continued fraction recurrance
    """
    def num_iter_func():
        for i in itertools.count(start=1):
            yield (2*i-1)**2

    num_iter = iter(num_iter_func())
    den_iter = itertools.repeat(6)

    yield from cf_n_recurrance(3, num_iter, den_iter, n)
    

def cf_n_recurrance(start_val, a_iter, b_iter, n):
    A_prev = 1
    B_prev = 0
    A_cur = start_val
    B_cur = 1
    yield A_cur/B_cur
    for i in range(1,n):
        a_next = next(a_iter)
        b_next = next(b_iter)
        A_next = b_next*A_cur+a_next*A_prev
        B_next = b_next*B_cur+a_next*B_prev
        A_prev = A_cur
        B_prev = B_cur
        A_cur = A_next
        B_cur = B_next
        yield A_cur/B_cur

def pi_cf_n_recurrance_2(n):
    """
    Uses the definition of pi/2 as

    successive an/bn for general continued recurrance

    an   1 -2*3 -1*2 -4*5 -3*4

    bn   3    1    3    1    3
    """

if __name__ == '__main__':
    main()

