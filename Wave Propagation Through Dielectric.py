# Needs work. Does not accept all frequencies or sigma values.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Constants
c = 3e8
f = 50e9
omega = 2 * np.pi * f
epsilon_0 = 8.854e-12
mu_0 = 4 * np.pi * 1e-7

# Initial Values
eps_r1_init = 1.0
eps_r2_init = 6.0
eps_r3_init = 1.0
thickness_mm_init = 2.0
sigma1_init = 0
sigma2_init = 1e-12
sigma3_init = 0

# Complex wave number
def complex_k(epsilon_r, sigma):
    epsilon_c = epsilon_0 * (epsilon_r - 1j * sigma / (omega * epsilon_0))
    return omega * np.sqrt(mu_0 * epsilon_c)

# Complex impedance
def complex_eta(epsilon_r, sigma):
    epsilon_c = epsilon_0 * (epsilon_r - 1j * sigma / (omega * epsilon_0))
    return np.sqrt(mu_0 / epsilon_c)

# Compute E-field
def compute_total_field(eps_r1, eps_r2, eps_r3, thickness_mm, sigma1, sigma2, sigma3):
    thickness_m = thickness_mm / 1000
    x = np.linspace(-0.01, 0.03, 2000)
    E = np.zeros_like(x, dtype=complex)

    k1 = complex_k(eps_r1, sigma1)
    eta1 = complex_eta(eps_r1, sigma1)

    k2 = complex_k(eps_r2, sigma2)
    eta2 = complex_eta(eps_r2, sigma2)

    k3 = complex_k(eps_r3, sigma3)
    eta3 = complex_eta(eps_r3, sigma3)

    Gamma12 = (eta2 - eta1) / (eta2 + eta1)
    T12 = 2 * eta2 / (eta2 + eta1)

    Gamma23 = (eta3 - eta2) / (eta3 + eta2)
    T23 = 2 * eta3 / (eta3 + eta2)

    for i, xi in enumerate(x):
        if xi < 0:
            phi = np.pi / 2
            A = 2.0
            E[i] = A * (np.exp(1j * (k1 * xi + phi)) + Gamma12 * np.exp(-1j * (k1 * xi + phi)))
        elif xi <= thickness_m:
            A = T12
            B = Gamma23 * A * np.exp(2j * k2 * thickness_m)
            E[i] = A * np.exp(1j * k2 * xi) + B * np.exp(-1j * k2 * xi)
        else:
            A = T12 * T23 * np.exp(1j * (k2 - k1) * thickness_m)
            E[i] = A * np.exp(1j * k3 * xi)

    return x * 1000, np.real(E)

fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.55)

x_vals, E_vals = compute_total_field(eps_r1_init, eps_r2_init, eps_r3_init, thickness_mm_init, sigma1_init, sigma2_init, sigma3_init)
line, = ax.plot(x_vals, E_vals, lw=2, label='Re{E(x)}')
ax.set_xlabel("Distance (mm)")
ax.set_ylabel("Re{E(x)}")
ax.set_title("Wave Propagation Through Dielectric")
ax.grid(True)

region1 = ax.axvspan(-10, 0, color='lightblue', alpha=0.2)
region2 = ax.axvspan(0, thickness_mm_init, color='orange', alpha=0.2)
region3 = ax.axvspan(thickness_mm_init, 30, color='lightblue', alpha=0.2)

ax_eps_r1 = plt.axes([0.25, 0.45, 0.65, 0.03])
ax_eps_r2 = plt.axes([0.25, 0.40, 0.65, 0.03])
ax_eps_r3 = plt.axes([0.25, 0.35, 0.65, 0.03])
ax_thick = plt.axes([0.25, 0.30, 0.65, 0.03])
ax_sig1 = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_sig2 = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_sig3 = plt.axes([0.25, 0.15, 0.65, 0.03])

slider_eps_r1 = Slider(ax_eps_r1, 'εr₁', 1.0, 12.0, valinit=eps_r1_init)
slider_eps_r2 = Slider(ax_eps_r2, 'εr₂', 1.0, 12.0, valinit=eps_r2_init)
slider_eps_r3 = Slider(ax_eps_r3, 'εr₃', 1.0, 12.0, valinit=eps_r3_init)
slider_thick = Slider(ax_thick, 'Thickness (mm)', 0.1, 20.0, valinit=thickness_mm_init)
slider_sig1 = Slider(ax_sig1, 'σ₁', 0.0, 1e4, valinit=sigma1_init)
slider_sig2 = Slider(ax_sig2, 'σ₂', 0.0, 1e4, valinit=sigma2_init)
slider_sig3 = Slider(ax_sig3, 'σ₃', 0.0, 1e4, valinit=sigma3_init)

def update(val):
    x, E = compute_total_field(slider_eps_r1.val, slider_eps_r2.val, slider_eps_r3.val,
                               slider_thick.val, slider_sig1.val, slider_sig2.val, slider_sig3.val)
    line.set_ydata(E)
    line.set_xdata(x)

    region2.set_xy([[0, -100], [slider_thick.val, -100], [slider_thick.val, 100], [0, 100]])
    region3.set_xy([[slider_thick.val, -100], [x[-1], -100], [x[-1], 100], [slider_thick.val, 100]])

    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

slider_eps_r1.on_changed(update)
slider_eps_r2.on_changed(update)
slider_eps_r3.on_changed(update)
slider_thick.on_changed(update)
slider_sig1.on_changed(update)
slider_sig2.on_changed(update)
slider_sig3.on_changed(update)

plt.legend()
plt.show()
