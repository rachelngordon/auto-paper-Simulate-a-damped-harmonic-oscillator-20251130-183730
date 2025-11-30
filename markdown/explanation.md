The script defines the ordinary differential equation for a damped harmonic oscillator  

\[
\ddot x + \frac{c}{m}\dot x + \frac{k}{m}x = 0 ,
\]

implemented in `damped_oscillator`. The helper `simulate` integrates this ODE with `scipy.integrate.solve_ivp` for given parameters (mass \(m\), damping coefficient \(c\), spring constant \(k\)), initial displacement \(x_0\) and velocity \(v_0\).

In `main` the natural frequency \(\omega_0=\sqrt{k/m}\) is computed (with \(k=m=1\) this equals 1). Three damping ratios \(\zeta = c/(2m\omega_0)\) are chosen: 0.5 (underdamped), 1 (critical), and 2 (over‑damped). For each \(\zeta\) the corresponding damping coefficient \(c = 2\zeta m\omega_0\) is calculated, the system is simulated from \(t=0\) to \(t=20\) s, and the results are plotted:

* **Displacement vs. time** for the three regimes (saved as *displacement_vs_time.png*).
* **Phase‑space trajectories** (displacement vs. velocity) colored by time (saved as *phase_space.png*).

Finally the script prints the natural frequency:

```
Answer: 1.0
```

**Answer:** The natural angular frequency \(\omega_0 = \sqrt{k/m}\) for the given parameters is **1.0**. No errors occurred.