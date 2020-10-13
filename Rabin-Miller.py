def millerT(n):

    d = n - 1
    c = 0

    while d%2 == 0:
        d = d/2
        c = c + 1


    import random as r
    import math as m

    a = r.randint(2, n-2)
    x = m.pow(a,d) % n

    if(x == 1 or x == n - 1):
        return False
    else:
        for i in range(0,c):
            x = m.pow(x,2) % n
            if(x == n - 1):
                return False
        return True
        
def millerR (n, s):
    for i in range(1, s):
        if millerT(n):
            return False
    return False
    
millerR (31,5)
