import math


def price(n, stock, k, u, d, t, r):
    q = (math.exp(r*t)-d)/(u-d)
    e1 = 0
    e2 = 0
    for i in range (0,n):
        w = math.pow(q, n-i) * math.pow((1 - q), i)
        p = stock * math.pow(u,n-i)*math.pow(d,i)- k
        bio = math.factorial(n)/(math.factorial(i) * math.factorial(n - i))
        if p > 0:
            e1 = e1 + bio * w * p
        else:
            e2 = e2 - bio * w * p
    print("Call Option:",e1*math.exp(-r*n*t))
    print("Put Option:", e2*math.exp(-r*n*t))
    return 0


price(3,100,105,1.2,0.8,0.5,0.1)