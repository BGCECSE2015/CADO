import numpy as np
import math


def bincoeff_array(k, n):
    # calculates binomial coefficient: n!
    # n and k are numpy arrays
    # assert (n >= k).all(), "n has to be greater or equal to k! "

    assert (n >= 0).all() and (k >= 0).all(), "n and k both have to be positive!"
    assert n.min() >= k.max(), "every element of n has to be greater or equal to k "

    b = np.zeros((n.size, k.size))

    for i in range(n.size):
        for j in range(k.size):
            b[i, j] = math.factorial(n[i]) / math.factorial(k[j]) \
                                     / math.factorial(n[i] - k[j])
    return b


def bincoeff(k, n):
    # calculates binomial coefficient: n!
    # n and k are scalars

    assert n >= k, "n has to be greater or equal to k!"
    assert n >= 0 and k >= 0, "n and k both have to be positive!"

    b = math.factorial(n) / math.factorial(k) / math.factorial(n - k)

    return b


def bernstein(i, n, t):
    # Calculates the i-th bernstein polynomial of degree n at t
    # i, n ,t are numpy arrays
    # Formula: bincoeff(n,i) * t^i * (1-t)^(n-i)

    t_power_i = np.power(t, i)
    t_power_n_i = np.power(np.ones((t.size,)) - t, n - i)
    B = np.multiply(np.multiply(bincoeff(i, n), t_power_i), t_power_n_i)
    return B


def bezier(P, h):
    # Returns x,y values of a bezier-curve with the given
    # control points P , stepwidth h
    # P is a matrix (2 x n),  h is a scalar

    t = np.arange(0, 1 + h, h)
    [u, v] = np.meshgrid(t, t)
    x = np.zeros(u.shape)
    y = np.zeros(u.shape)
    z = np.zeros(u.shape)
    n = P.shape(1)
    m = P.shape(2)

    for i in range(n):
        for j in range(m):
            x = x + np.multiply(bernstein(i, n, u), bernstein(j, m, v)) * P[0, i, j]
            y = y + np.multiply(bernstein(i, n, u), bernstein(j, m, v)) * P[1, i, j]
            z = z + np.multiply(bernstein(i, n, u), bernstein(j, m, v)) * P[2, i, j]