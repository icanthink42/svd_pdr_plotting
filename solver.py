import numpy as np
from numpy.linalg import norm
from scipy.optimize import root


def solve_range(mu, r1, r2, t0, tf, tguess, iter, n):
    c = norm(r2 - r1)
    times1 = np.linspace(tguess, tf, iter)
    times2 = np.linspace(tguess, t0, iter)

    def lambert_equations(vars):
        a, alpha, beta = vars
        s = (norm(r1) + norm(r2) + c) / 2
        eq1 = -dt + np.sqrt(a**3 / mu) * (
            2 * np.pi * n + (alpha - beta) - (np.sin(alpha) - np.sin(beta))
        )
        eq2 = -np.sin(alpha / 2) + np.sqrt(s / (2 * a))
        eq3 = -np.sin(beta / 2) + np.sqrt((s - c) / (2 * a))
        return [eq1, eq2, eq3]

    out1 = []
    out2 = []

    guess = [(norm(r1) + norm(r2)) / 2, np.pi / 2, np.pi / 2]
    for dt in times1:
        sol = root(
            lambert_equations,
            guess,
            method="lm",
        )
        guess = sol.x
        out1.append([dt, *sol.x])
    for dt in times2:
        sol = root(
            lambert_equations,
            guess,
            method="lm",
        )
        guess = sol.x
        out2.append([dt, *sol.x])
    out2.reverse()
    out = out2[:-1] + out1
    return np.array(out)


def auto_solve(mu, r1, r2, t0, tf, step):
    c = norm(r2 - r1)

    def lambert_equations(vars):
        a, alpha, beta = vars
        s = (norm(r1) + norm(r2) + c) / 2
        eq1 = -dt + np.sqrt(a**3 / mu) * (
            (alpha - beta) - (np.sin(alpha) - np.sin(beta))
        )
        eq2 = -np.sin(alpha / 2) + np.sqrt(s / (2 * a))
        eq3 = -np.sin(beta / 2) + np.sqrt((s - c) / (2 * a))
        return [eq1, eq2, eq3]

    out1 = []
    out2 = []
    dt = (tf - t0) / 2

    guess = [(norm(r1) + norm(r2)) / 2, np.pi / 2, np.pi / 2]
    while dt < tf:
        sol = root(
            lambert_equations,
            guess,
            method="lm",
        )
        guess = sol.x
        dt += step
        out1.append([dt, *sol.x])

    dt = (tf - t0) / 2
    while dt < tf:
        sol = root(
            lambert_equations,
            guess,
            method="lm",
        )
        guess = sol.x
        dt -= step
        out2.append([dt, *sol.x])

    out2.reverse()
    out = out2[:-1] + out1
    return np.array(out)


def solve_velocities(mu, r1, r2, a, alpha, beta):
    r_c = (r2 - r1) / norm(r2 - r1)
    z = np.sqrt(mu / (4 * a)) / np.tan(beta / 2)
    y = np.sqrt(mu / (4 * a)) / np.tan(alpha / 2)

    v1 = (z + y) * r_c + (z - y) * r1 / norm(r1)
    v2 = (z + y) * r_c - (z - y) * r2 / norm(r2)

    return v1, v2
