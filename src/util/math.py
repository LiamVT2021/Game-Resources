from math import floor

def gcd(a: int, b: int) -> int:
    if b > a :
        return gcd(b, a)
    q = 0
    while (q+1) * b <= a:
        q += 1
    r = a - (q*b)
    if r == 0:
        return b
    ## optimization
    if r > b//2:
        q += 1
        r = b-r
    print(a,b)
    return gcd(b,r)


def fullRange(r1, r2):
    return range(min(r1, r2), max(r1, r2) + 1)

def nonZeroRange(r):
    if r <= 0:
        return range(r, 0)
    return range(1,r+1)

def roundUp(n):
    return floor(n+.5)

def toInt(Str, default = 0):
    try: 
        i = int(Str)
        return i
    except ValueError:
        return default

# print(gcd(34873,178))
    