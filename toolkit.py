import numpy as np
import pandas as pd
from scipy.special import gamma
import scipy.optimize as opt


def weibull_pdf(u, a, k):
    f1 = np.divide(k, a)
    f2 = np.divide(u, a)
    f3 = np.power(f2, k-1)
    f4 = np.power(f2, k)
    f5 = np.exp(-f4)

    out1 = np.multiply(f1, f3)
    out = np.multiply(out1, f5)
    return out


def load_akf(file):
  data = pd.read_csv(file)

  a = np.array(data['A'])
  k = np.array(data['k'])
  f = np.array(data['f'])

  return a, k, f


def load_ak(file):
    data = pd.read_csv(file)

    a = np.array(data['A'])
    k = np.array(data['k'])

    return a, k


def find_weibull(u):

    mu = np.mean(u)
    mu_3 = np.mean(np.power(u, 3))

    perc_mu = (len(u[u <= mu])) / len(u)

    def loss(ak):
        a = ak[0]
        k = ak[1]

        out1 = -mu_3 + a ** 3 * gamma(1 + 3 / k)
        out2 = -perc_mu + (1 - np.exp(-(mu / a) ** k))

        return out1, out2

    init = np.array([7, 1])
    [a, k] = opt.fsolve(loss, init)

    return a, k
