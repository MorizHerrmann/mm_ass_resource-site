import numpy as np
import pandas as pd

def weibull_pdf(u, a, k):
    f1 = np.divide(k,a)
    f2 = np.divide(u,a)
    f3 = np.power(f2,k-1)
    f4 = np.power(f2,k)
    f5 = np.exp(-f4)

    out1 = np.multiply(f1,f3)
    out = np.multiply(out1,f5)
    return out


def load_data(file):
  data = pd.read_csv(file)

  wb_A = np.array(data['A'])
  wb_k = np.array(data['k'])
  f = np.array(data['f'])

  return wb_A, wb_k, f


def weibull_parameter_method(A, k, c_ie):
    """

    :param A: weibull scale parameter
    :param k: weibull shape parameter
    :param c_ie: number of independent events
    :return: alpha, beta (gumbel parameters)
    """
    beta = np.multiply(A, np.log10(c_ie) ** (1/k))
    alpha = np.divide(np.multiply(A, np.log10(c_ie) ** (1/(k-1))), k)
    return alpha, beta