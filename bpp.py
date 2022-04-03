import sympy
import mpmath
import fractions
import math

PRINT_ON=False
def LOG(*args, **kwargs):
    if PRINT_ON:
        print(*args, **kwargs)

def main():
    for n in range(0, 30):
        print('{}-th hex digit of pi is {:x}'.format(n, pi_hex_digit(n)))

def pi_hex_digit(n):
    total = 0
    for i in range(4):
        next_val = sigma_multiples[i] * sigma(n-1, i)
        total += next_val
    LOG(f'total for {n}-th digit: {total}')
    hex_digit = math.floor(16*(total % 1))
    return hex_digit

sigma_offsets = (1, 4, 5, 6)
sigma_multiples = (4, -2, -1, -1)

def sigma(n, sum_i, extra_terms=2):
    k = 0
    total = 0
    offset = sigma_offsets[sum_i]
    while k <= n:
        denom = 8*k+offset
        next_term = fractions.Fraction(pow(16, n-k, denom), denom)
        total += next_term
        LOG(next_term, total)
        k += 1
    LOG('-- next terms')
    while k <= n + extra_terms:
        next_term = fractions.Fraction(1, (8*k+offset)*pow(16, k-n))
        total += next_term
        LOG(next_term, total)
        k += 1
    total += next_term
    LOG('--total:', total)
    return total
    

if __name__ == '__main__':
    main()
