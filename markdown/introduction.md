## Introduction

Vibrations of mechanical systems are encountered in virtually every engineering discipline, from civil structures that must withstand wind‑induced sway to precision instruments whose performance hinges on the suppression of unwanted motion.  The simplest yet most representative model of such phenomena is the single‑degree‑of‑freedom mass–spring–damper, whose dynamics are governed by a second‑order linear ordinary differential equation.  Understanding how energy is dissipated through damping, how natural frequencies are altered, and how transient responses evolve is essential for designing safe buildings, reliable automotive suspensions, high‑performance aerospace components, and a host of other technologies.  Moreover, the damped harmonic oscillator serves as a canonical testbed for numerical integration techniques, control‑system synthesis, and educational demonstrations of fundamental concepts such as eigenvalue analysis and phase‑space trajectories.

Despite its apparent simplicity, the accurate simulation of a damped oscillator poses several subtle challenges.  The governing equation  

\[
m\ddot{x}(t) + c\dot{x}(t) + k\,x(t) = 0
\]

contains parameters that can span several orders of magnitude, leading to stiff dynamics in the overdamped regime and rapid oscillations in the underdamped regime.  A numerical method that works well for one set of parameters may become inefficient or even unstable for another.  Consequently, a key research question addressed in this paper is:

**How can a single, reproducible computational workflow reliably simulate the transient response of a linear damped harmonic oscillator across the full spectrum of damping ratios, while maintaining accuracy and computational efficiency?**

To answer this question we adopt a high‑level strategy that leverages well‑established tools from the scientific Python ecosystem.  The second‑order equation is first recast as a first‑order system by introducing the velocity variable, enabling the use of generic initial‑value problem solvers.  An adaptive explicit Runge–Kutta method of order 5(4) (the Dormand–Prince scheme) is employed to automatically adjust step sizes according to prescribed error tolerances, thereby handling both stiff and non‑stiff regimes without manual tuning.  The workflow is organized into modular components: a function that evaluates the right‑hand side of the ODE, a thin wrapper that invokes the integrator, and a driver script that selects representative damping ratios, runs the simulations, and produces both displacement‑time and phase‑space visualizations.  By keeping the implementation deliberately lightweight and by relying on dense output for uniform post‑processing, the approach remains accessible to students and practitioners while still being suitable for more advanced investigations.

What distinguishes the present work from textbook treatments of the damped oscillator is threefold.  First, we provide a fully reproducible, open‑source script that integrates the model, performs parameter sweeps, and generates publication‑quality figures in a single execution, thereby eliminating the fragmented, hand‑crafted examples commonly found in textbooks.  Second, we explicitly compare the numerical trajectories against their analytical counterparts for each damping regime, quantifying the error introduced by the adaptive solver and demonstrating that default tolerance settings are sufficient for visual fidelity.  Third, the modular design isolates the physics from the numerical engine, making it straightforward to substitute alternative integrators (e.g., implicit methods for highly stiff cases) or to extend the model to include forcing terms, nonlinear springs, or stochastic disturbances.  This flexibility is rarely emphasized in pedagogical expositions, which tend to focus on a single analytical solution or a fixed numerical scheme.

In summary, the contribution of this paper is a concise yet comprehensive demonstration of how modern scientific computing tools can be harnessed to simulate a classic dynamical system across its full range of behavior, with an emphasis on reproducibility, validation, and extensibility.

### Contributions

This work makes the following contributions:
- A self‑contained Python implementation that defines the damped harmonic oscillator as a first‑order system, integrates it with an adaptive Runge–Kutta solver, and produces both time‑domain and phase‑space visualizations.
- A systematic validation framework that juxtaposes numerical results with closed‑form analytical solutions for underdamped, critically damped, and overdamped regimes, reporting error metrics that confirm solver adequacy.
- An open‑source, modular code architecture that separates model definition, integration, and post‑processing, facilitating easy replacement of the numerical method or extension to more complex dynamics.
- A reproducible research pipeline that can be directly reused in educational settings, laboratory assignments, or as a baseline for research on forced, nonlinear, or stochastic extensions of the oscillator model.