import math
from Tkinter import *
import numpy as np
import scipy.stats as sps


# A naive pricing method of binomial tree
def BinomialPrice(n, stock, k, u, d, t, r):
    q = (math.exp(r * t) - d) / (u - d)
    e1 = 0
    e2 = 0
    for i in range(0, n):
        w = math.pow(q, n - i) * math.pow((1 - q), i)
        p = stock * math.pow(u, n - i) * math.pow(d, i) - k
        bio = math.factorial(n) / (math.factorial(i) * math.factorial(n - i))
        if p > 0:
            e1 = e1 + bio * w * p
        else:
            e2 = e2 - bio * w * p
    print "Call Option:", e1 * math.exp(-r * n * t)
    print "Put Option:", e2 * math.exp(-r * n * t)
    return 0


'''
Create a class of option
S0: the initial price of underlying assets
K: the exercise price
t: time to maturity
rf: risk free rate
sigma: volatility
dv: dividend
'''


class Option:
    def __init__(self, type, S0, K, t, rf, sigma, dv=0):
        self.type = 'Call' if (type == 'C' or type == 'c') else 'Put'
        self.type_sign = 1.0 if self.type == 'Call' else -1.0
        self.S0 = S0 * 1.0
        self.K = K * 1.0
        self.t = t * 1.0
        self.sigma = sigma * 1.0
        self.rf = rf * 1.0
        self.dv = dv * 1.0
        self.d_1 = (np.log(self.S0 / self.K) + (
        self.rf - self.dv + .5 * self.sigma ** 2) * self.t) / self.sigma / np.sqrt(self.t)
        self.d_2 = self.d_1 - self.sigma * np.sqrt(self.t)


    #Use B-S-M formula to prcie
    def BlackScholesMerton(self):
        return self.type_sign * self.S0 * np.exp(-self.dv * self.t) * sps.norm.cdf(self.type_sign * self.d_1) \
               - self.type_sign * self.K * np.exp(-self.rf * self.t) * sps.norm.cdf(self.type_sign * self.d_2)

    #Use Mente Carlo to simulate
    def MenteCarlo(self, iteration=1000000):
        zt = np.random.normal(0, 1, iteration)
        st = self.S0 * np.exp((self.rf - self.dv - .5 * self.sigma ** 2) * self.t + self.sigma * self.t ** .5 * zt)
        p = []
        for St in st:
            p.append(max(self.type_sign * (St - self.K), 0))
        return np.average(p) * np.exp(-self.rf * self.t)


def calculate():
    vlist = []
    for e in elist:
        try:
            q = float(e.get())
            vlist.append(q)
        except:
            answ.config(text='Invalid Input(s). Please input correct parameter(s)', fg='red')
            e.delete(0, len(e.get()))
            return 0

    for i in range(6):
        if i != 3 and vlist[i] < 0:
            answ.config(text='Invalid Input(s). Please input correct parameter(s)', fg='red')
            elist[i].delete(0, len(elist[i].get()))
            return 0

    vlist[6] = int(vlist[6])
    if vlist[6] < 500:
        vlist[6] = 500
        elist[6].delete(0, len(elist[6].get()))
        elist[6].insert(0, '500')
    elif vlist[6] > 12000000:
        vlist[6] = 12000000
        elist[6].delete(0, len(elist[6].get()))
        elist[6].insert(0, '12000000')

    o = Option(cp.get(), vlist[0], vlist[1], vlist[2] / 365, vlist[3], vlist[4], vlist[5])
    answ.config(text='The result is as follows:', fg='black')
    bs.config(text=str("%.8f" % o.BlackScholesMerton()))
    mc.config(text=str("%.8f" % o.MenteCarlo(iteration=vlist[6])))


# the GUI part


root = Tk()
root.wm_title('=w= Option Pricer')
Label(root, text='Enter parameters, '
                 'and click "Calculate" button.').grid(row=0, column=0, columnspan=3)
Label(root, text='Saito Asuka is the BEST --- XGS').grid(columnspan=3)
cp = StringVar()
Label(root, text='Type').grid(row=2, column=0, sticky=W)
Radiobutton(root, text='Call', variable=cp, value='c').grid(row=2, column=1)
Radiobutton(root, text='Put', variable=cp, value='p').grid(row=2, column=2)
plist = ['Current Price', 'Strike Price', 'Days to Maturity',
         'Risk-free Rate', 'Volatility', 'Continuous Dividend Rate', 'MC Iteration']
elist = []
r = 3  # r start from 0 and now is 3
for param in plist:
    Label(root, text=param).grid(column=0, sticky=W)
    e = Entry(root)
    e.grid(row=r, column=1, columnspan=2, sticky=W + E)
    elist.append(e)
    r += 1
Button(root, text='Calculate', command=calculate).grid(row=r)
r += 1

answ = Label(root, text='The result is as follows:')
answ.grid(row=r, columnspan=3)
r += 1

bs = Label(root)
mc = Label(root)
bs.grid(row=r, columnspan=2, sticky=E)
mc.grid(row=r + 1, columnspan=2, sticky=E)

Label(root, text='BlackScholes formula: ').grid(row=r, sticky=W)
Label(root, text='MC simulation: ').grid(row=r + 1, sticky=W)

root.mainloop()