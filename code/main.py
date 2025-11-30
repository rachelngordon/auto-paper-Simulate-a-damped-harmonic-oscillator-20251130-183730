import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

def damped_oscillator(t, y, m, c, k):
    x, v = y
    return [v, -(c/m)*v - (k/m)*x]

def simulate(m, c, k, x0, v0, t_span, t_eval):
    sol = solve_ivp(damped_oscillator, t_span, [x0, v0], t_eval=t_eval, args=(m, c, k))
    return sol.t, sol.y[0], sol.y[1]

def main():
    m = 1.0
    k = 1.0
    omega0 = np.sqrt(k / m)
    zetas = [0.5, 1.0, 2.0]
    colors = ['b', 'g', 'r']
    labels = ['Underdamped (ζ=0.5)', 'Critically damped (ζ=1)', 'Overdamped (ζ=2)']
    t_eval = np.linspace(0, 20, 2000)

    # Displacement vs time plot
    plt.figure()
    for zeta, color, label in zip(zetas, colors, labels):
        c = 2 * zeta * m * omega0
        t, x, v = simulate(m, c, k, 1.0, 0.0, (t_eval[0], t_eval[-1]), t_eval)
        plt.plot(t, x, color=color, label=label)
    plt.xlabel('Time (s)')
    plt.ylabel('Displacement')
    plt.title('Displacement vs Time for Different Damping Regimes')
    plt.legend()
    plt.grid(True)
    plt.savefig('displacement_vs_time.png')
    plt.close()

    # Phase space plot
    plt.figure()
    for zeta, color, label in zip(zetas, colors, labels):
        c = 2 * zeta * m * omega0
        t, x, v = simulate(m, c, k, 1.0, 0.0, (t_eval[0], t_eval[-1]), t_eval)
        sc = plt.scatter(x, v, c=t, cmap='viridis', s=1, label=label)
    plt.xlabel('Displacement')
    plt.ylabel('Velocity')
    plt.title('Phase Space Trajectories')
    plt.legend()
    plt.grid(True)
    plt.savefig('phase_space.png')
    plt.close()

    # Final numeric answer
    print('Answer:', omega0)

if __name__ == '__main__':
    main()
