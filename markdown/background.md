## Background

The damped harmonic oscillator is the prototypical linear second‑order dynamical system that appears in virtually every field dealing with vibratory phenomena.  Its governing equation  

\[
m\,\ddot{x}(t)+c\,\dot{x}(t)+k\,x(t)=0,
\]

relates the inertial force \(m\ddot{x}\), the viscous damping force \(c\dot{x}\), and the restoring spring force \(kx\).  Here \(m>0\) denotes the mass, \(c\ge 0\) the damping coefficient, \(k>0\) the stiffness, and \(x(t)\) the displacement as a function of time.  The equation is linear with constant coefficients, which makes it amenable to analytical treatment while still capturing the essential physics of energy dissipation and resonance.

### Classical Solution and Damping Regimes  

Introducing the natural (undamped) angular frequency  

\[
\omega_{0}= \sqrt{\frac{k}{m}},
\]

and the dimensionless damping ratio  

\[
\zeta = \frac{c}{2\,m\,\omega_{0}},
\]

the characteristic polynomial of the ODE is  

\[
\lambda^{2}+2\zeta\omega_{0}\lambda+\omega_{0}^{2}=0.
\]

Its roots  

\[
\lambda_{1,2}= -\zeta\omega_{0}\pm\omega_{0}\sqrt{\zeta^{2}-1}
\]

determine the qualitative behaviour:

* **Underdamped (\(0\le\zeta<1\))** – Complex conjugate roots lead to oscillatory motion with exponentially decaying amplitude:  

  \[
  x(t)=A\,e^{-\zeta\omega_{0}t}\cos(\omega_{d}t)+B\,e^{-\zeta\omega_{0}t}\sin(\omega_{d}t),
  \]
  where \(\omega_{d}= \omega_{0}\sqrt{1-\zeta^{2}}\) is the damped natural frequency.

* **Critically damped (\(\zeta=1\))** – Repeated real root \(\lambda=-\omega_{0}\) yields the fastest non‑oscillatory return to equilibrium:  

  \[
  x(t)= (A+Bt)\,e^{-\omega_{0}t}.
  \]

* **Over‑damped (\(\zeta>1\))** – Two distinct negative real roots produce a slow, non‑oscillatory decay:  

  \[
  x(t)=A\,e^{\lambda_{1}t}+B\,e^{\lambda_{2}t},
  \]
  with \(\lambda_{1,2}<0\).

These analytic expressions provide reference solutions against which any numerical method can be benchmarked.  They also reveal why the problem can become stiff: when \(\zeta\) is large, one eigenvalue may be much more negative than the other, causing rapid transients that demand small time steps for explicit integrators to remain stable.

### First‑Order Formulation  

Numerical ODE solvers in most software libraries accept a system of first‑order equations.  By defining the velocity variable  

\[
v(t)=\dot{x}(t),
\]

the second‑order equation is rewritten as  

\[
\frac{d}{dt}\begin{bmatrix}x\\ v\end{bmatrix}
=
\begin{bmatrix}
v\\[4pt]
-\dfrac{c}{m}\,v-\dfrac{k}{m}\,x
\end{bmatrix}
\equiv f\bigl(t,\mathbf{y}\bigr),
\qquad
\mathbf{y}(t)=\begin{bmatrix}x(t)\\ v(t)\end{bmatrix}.
\]

The vector field \(f\) is linear in \(\mathbf{y}\) and its Jacobian is constant:

\[
J = \frac{\partial f}{\partial \mathbf{y}}=
\begin{bmatrix}
0 & 1\\[4pt]
-\dfrac{k}{m} & -\dfrac{c}{m}
\end{bmatrix}.
\]

The eigenvalues of \(J\) coincide with the characteristic roots \(\lambda_{1,2}\) above, linking the continuous‑time dynamics directly to the stability properties of discrete integration schemes.

### Numerical Integration Basics  

Standard explicit Runge–Kutta (RK) methods approximate the solution by a weighted combination of stage evaluations of \(f\).  An \(s\)-stage RK method advances the state from \(t_{n}\) to \(t_{n+1}=t_{n}+h\) via  

\[
\mathbf{y}_{n+1}= \mathbf{y}_{n}+h\sum_{i=1}^{s}b_{i}\,k_{i},
\qquad
k_{i}=f\!\Bigl(t_{n}+c_{i}h,\,
\mathbf{y}_{n}+h\sum_{j=1}^{i-1}a_{ij}k_{j}\Bigr).
\]

The order of accuracy \(p\) indicates that the local truncation error scales as \(\mathcal{O}(h^{p+1})\) and the global error as \(\mathcal{O}(h^{p})\).  The Dormand–Prince pair (often called RK45) provides a fifth‑order estimate together with an embedded fourth‑order estimate; the difference between them is used to control the step size adaptively.

Adaptive step‑size control selects \(h\) so that an estimate of the local error \(\epsilon\) satisfies  

\[
\epsilon \le \max\bigl(\text{rtol}\,| \mathbf{y}_{n}|,\;\text{atol}\bigr),
\]

where `rtol` and `atol` are user‑specified relative and absolute tolerances.  If the error exceeds the tolerance, the step is rejected and a smaller \(h\) is tried; otherwise the step is accepted and a possibly larger \(h\) is proposed for the next interval.  This mechanism automatically refines the mesh in regions of rapid change (e.g., the initial transient of an over‑damped system) while coarsening it when the solution varies slowly (e.g., the slowly decaying tail of an under‑damped response).

### Error, Stability, and Stiffness  

For linear systems the stability of an explicit RK method can be examined via its stability function \(R(z)\), where \(z = \lambda h\) and \(\lambda\) is an eigenvalue of the Jacobian.  The method is stable if \(|R(z)|\le 1\).  Because the over‑damped regime yields eigenvalues with large negative real parts, the product \(|\lambda|h\) can quickly leave the stability region unless \(h\) is reduced dramatically.  Implicit methods (e.g., backward Euler or implicit RK) possess larger stability regions that include much of the left half‑plane, making them attractive for stiff problems but at the cost of solving nonlinear algebraic equations each step.

In the context of the research question—producing a single, reproducible workflow that works across all damping ratios—understanding these stability and error concepts is essential.  A robust approach must either employ an adaptive explicit scheme with sufficiently stringent tolerances to handle the stiff over‑damped case, or switch to an implicit method when stiffness is detected.  Moreover, the conversion to a first‑order system, the use of eigenvalue analysis to anticipate stiffness, and the interpretation of local error estimates all form the theoretical backbone that guides the design of the computational pipeline described in the remainder of the paper.