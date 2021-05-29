from math import floor


def gcd(a: int, b: int) -> int:
    if b > a:
        return gcd(b, a)
    q = 0
    while (q + 1) * b <= a:
        q += 1
    r = a - (q * b)
    if r == 0:
        return b
    # # optimization
    if r > b // 2:
        q += 1
        r = b - r
    print(a, b)
    return gcd(b, r)


def fullRange(r1, r2):
    return range(min(r1, r2), max(r1, r2) + 1)


def sumRange(i, j1, j2, s1, s2, Sorted=False):
    # jMin = min(j1,j2)
    # jMax = max(j1,j2)
    # sMin = min(s1,s2)-i
    # sMax = max(s1,s2)-i
    if Sorted:
        return range(max(j1, s1 - i), min(j2, s2 - i) + 1)
    return range(max(min(j1, j2), min(s1, s2) - i), min(max(j1, j2), max(s1, s2) - i) + 1)


def nonZeroRange(r):
    if r <= 0:
        return range(r, 0)
    return range(1, r + 1)


def roundUp(n):
    return floor(n + .5)


def toInt(Str, default=0):
    try: 
        i = int(Str)
        return i
    except ValueError:
        return default


def even(x):
    if x % 2 == 0:
        return x
    elif x < 0:
        return x - 1
    else:
        return x + 1
def odd(x):
    if x % 2 == 1:
        return x
    elif x < 0:
        return x - 1
    else:
        return x + 1
# print(gcd(34873,178))
    
