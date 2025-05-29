import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Frequency range (log scale)
frequencies = np.logspace(3, 9, 500)  # 1 kHz to 1 GHz

# Constants
mu_0 = 4 * np.pi * 1e-7  # Permeability of free space
sigma_default = 5e3    # Conductivity of copper (S/m)
mu_r_default = 1         # Relative permeability (non-magnetic material)
thickness_default = 0.001  # 1 mm

# Shielding Effectiveness formula (simplified)
def calculate_se(f, sigma, mu_r, t):
    mu = mu_0 * mu_r
    delta = np.sqrt(2 / (mu * sigma * 2 * np.pi * f))  # Skin depth
    A = t / delta  # Absorption loss
    SE = 8.7 * A  # in dB
    return SE

# Initial calculation
se_values = calculate_se(frequencies, sigma_default, mu_r_default, thickness_default)

# Plot
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.35)
line, = ax.plot(frequencies, se_values, lw=2)
ax.set_xscale('log')
ax.set_xlabel('Source Frequency (Hz)')
ax.set_ylabel('Shielding Effectiveness (dB)')
ax.set_title('EMI Shielding Effectiveness vs Frequency')
ax.grid(True)

# Slider Axes
ax_sigma = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_mu_r = plt.axes([0.25, 0.20, 0.65, 0.03])
ax_thickness = plt.axes([0.25, 0.15, 0.65, 0.03])

# Sliders
s_sigma = Slider(ax_sigma, 'Conductivity (S/m)', 1e6, 1e8, valinit=sigma_default, valstep=1e6)
s_mu_r = Slider(ax_mu_r, 'Relative Permeability', 1, 1000, valinit=mu_r_default, valstep=1)
s_thickness = Slider(ax_thickness, 'Thickness (m)', 0.0001, 0.01, valinit=thickness_default, valstep=0.0001)

# Update Function
def update(val):
    sigma = s_sigma.val
    mu_r = s_mu_r.val
    thickness = s_thickness.val
    new_se = calculate_se(frequencies, sigma, mu_r, thickness)
    line.set_ydata(new_se)
    fig.canvas.draw_idle()

# Connect sliders
s_sigma.on_changed(update)
s_mu_r.on_changed(update)
s_thickness.on_changed(update)

plt.show()
