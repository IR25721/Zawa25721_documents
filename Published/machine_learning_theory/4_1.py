import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gamma, norm


def vb_e_step(X, E_tau, mu_0, lambda_0):
    N = len(X)
    lambda_N = lambda_0 + N * E_tau
    mu_N = (lambda_0 * mu_0 + E_tau * np.sum(X)) / lambda_N
    return mu_N, lambda_N


def vb_m_step(X, mu_N, lambda_N, a_0, b_0):
    N = len(X)
    a_N = a_0 + N / 2.0
    b_N = b_0 + 0.5 * np.sum((X - mu_N) ** 2) + N / (2.0 * lambda_N)
    E_tau = a_N / b_N
    return a_N, b_N, E_tau


def plot_results(X, mu_N, lambda_N, a_N, b_N):
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    mu_axis = np.linspace(
        mu_N - 4 / np.sqrt(lambda_N), mu_N + 4 / np.sqrt(lambda_N), 500
    )
    axes[0].plot(mu_axis, norm.pdf(mu_axis, mu_N, 1 / np.sqrt(lambda_N)))
    axes[0].set_title("q(mu)")

    tau_axis = np.linspace(
        max(0.01, a_N / b_N - 4 * np.sqrt(a_N) / b_N),
        a_N / b_N + 4 * np.sqrt(a_N) / b_N,
        500,
    )
    axes[1].plot(tau_axis, gamma.pdf(tau_axis, a_N, scale=1 / b_N))
    axes[1].set_title("q(tau)")

    x_axis = np.linspace(min(X) - 2, max(X) + 2, 500)
    E_tau = a_N / b_N
    std_dev = 1 / np.sqrt(E_tau)
    axes[2].plot(x_axis, norm.pdf(x_axis, mu_N, std_dev), label='Estimated dist')
    axes[2].scatter(X, np.zeros_like(X), color='red', marker='x', label='Data X')
    axes[2].set_title("Data and Estimated Distribution")
    axes[2].legend()

    plt.show()


X = np.array([1.2, 1.8, 2.2, 2.8, 3.0])
mu_0, lambda_0 = 0.0, 1.0
a_0, b_0 = 1.0, 1.0

E_tau = a_0 / b_0

for _ in range(10):
    mu_N, lambda_N = vb_e_step(X, E_tau, mu_0, lambda_0)
    a_N, b_N, E_tau = vb_m_step(X, mu_N, lambda_N, a_0, b_0)

plot_results(X, mu_N, lambda_N, a_N, b_N)
