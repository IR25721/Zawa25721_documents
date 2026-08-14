import matplotlib.pyplot as plt
import numpy as np
from scipy.special import digamma, gammaln

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

def calc_elbo(X, mu_N, lambda_N, a_N, b_N, mu_0, lambda_0, a_0, b_0):
    N = len(X)
    E_tau = a_N / b_N
    E_ln_tau = digamma(a_N) - np.log(b_N)
    
    # E[ln p(X | mu, tau)]
    E_sq_diff_X = np.sum((X - mu_N)**2) + N / lambda_N
    E_ln_p_X = (N / 2) * E_ln_tau - (N / 2) * np.log(2 * np.pi) - 0.5 * E_tau * E_sq_diff_X
    
    # E[ln p(mu)]
    E_sq_diff_mu = (mu_N - mu_0)**2 + 1 / lambda_N
    E_ln_p_mu = 0.5 * np.log(lambda_0) - 0.5 * np.log(2 * np.pi) - 0.5 * lambda_0 * E_sq_diff_mu
    
    # E[ln p(tau)]
    E_ln_p_tau = a_0 * np.log(b_0) - gammaln(a_0) + (a_0 - 1) * E_ln_tau - b_0 * E_tau
    
    # - E[ln q(mu)]
    H_q_mu = 0.5 * (1 + np.log(2 * np.pi) - np.log(lambda_N))
    
    # - E[ln q(tau)]
    H_q_tau = a_N - np.log(b_N) + gammaln(a_N) + (1 - a_N) * digamma(a_N)
    
    elbo = E_ln_p_X + E_ln_p_mu + E_ln_p_tau + H_q_mu + H_q_tau
    return elbo

if __name__ == "__main__":
    X = np.array([1.2, 1.8, 2.2, 2.8, 3.0])
    mu_0, lambda_0 = 0.0, 1.0
    a_0, b_0 = 1.0, 1.0

    E_tau = a_0 / b_0
    
    # To store ELBO values
    elbos = []

    for i in range(15):
        mu_N, lambda_N = vb_e_step(X, E_tau, mu_0, lambda_0)
        a_N, b_N, E_tau = vb_m_step(X, mu_N, lambda_N, a_0, b_0)
        
        elbo = calc_elbo(X, mu_N, lambda_N, a_N, b_N, mu_0, lambda_0, a_0, b_0)
        elbos.append(elbo)

    plt.figure(figsize=(8, 5))
    plt.plot(range(1, 16), elbos, marker='o', linestyle='-', color='b')
    plt.title("Evidence Lower Bound (ELBO) across Iterations")
    plt.xlabel("Iteration")
    plt.ylabel("ELBO")
    plt.grid(True)
    plt.savefig('elbo_plot.png')
    plt.show()
