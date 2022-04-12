import itertools

import sympy
from sympy import Abs, pi, floor
import sympy.ntheory.continued_fraction as cf_mod

S = sympy.sympify

def main():
    N=50
    # pi_list = list(pi_recurrance_1(N))
    # pi_list = list(pi_recurrance_2(N))
    # pi_list = list(pi_bpp(N))
    pi_list = list(pi_bellard(N))
    prev_pi = 0
    for i in range(0, N):
        cur_pi = pi_list[i]
        diff = Abs(cur_pi - prev_pi)
        diff_ln = float(-sympy.ln(diff).evalf())
        diff_log = float(-sympy.ln(diff, 10).evalf())
        print(f"{i}: {cur_pi}, e:{diff_ln:.2f}, 10:{diff_log:.2f}")

        prev_pi = cur_pi

class RequirementError(RuntimeError): pass
def require(cond, msg):
    if not cond:
        raise RequirementError(msg)

bellard_nums  = (-2**5, -1, 2**8, -2**6, -2**2,     -2**2,  1)
bellard_d_mul = (4,     4,  10,     10,     10,     10,     10)
bellard_d_off = (1,     3,  1,      3,      5,      7,      9)
def pi_bellard(n):
    total = 0
    for k in range(n):
        val = 0
        for i in range(7):
            val += S(bellard_nums[i])/S(bellard_d_mul[i]*k + bellard_d_off[i])

        val *= (-1)**n/S(2**(10*n+6))
        total += val
        yield total

bpp_numerators = (4, -2, -1, -1)
bpp_offsets = (1, 4, 5, 6)
def pi_bpp(n):
    total = 0
    for k in range(n):
        denom_base = 8*k
        val = 0
        for i in range(4):
            val += S(bpp_numerators[i])/S(denom_base + bpp_offsets[i])

        val *= 1/S(16**k)

        total += val
        yield total

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

def pi_recurrance_2(n):
    """
    Uses the definition of pi/2 as

    successive an/bn for general continued recurrance

    an   -1 -2*3 -1*2 -4*5 -3*4 -6*7 -5*6

    bn    3    1    3    1    3    1    3
    """

    def num_iter_func():
        yield -1
        for i in itertools.count(start=2, step=2):
            yield -i*(i+1)
            yield -(i-1)*i

    num_iter = iter(num_iter_func())
    den_iter = itertools.cycle([3,1])

    yield from cf_n_recurrance(1, num_iter, den_iter, 200)

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

if __name__ == '__main__':
    main()

