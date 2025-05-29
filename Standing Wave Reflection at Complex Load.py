import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Constants
Z0 = 50  # Characteristic impedance (Ohms)

# Default values
distance_default = 2.0
line_length_default = 1.0
alpha_default = 0.5
R_default = 100.0
X_default = 40.0

# Compute waves
def compute_waves(x, line_length, alpha, R, X):
    k = 2 * np.pi / line_length
    ZL = R + 1j * X
    Gamma = (ZL - Z0) / (ZL + Z0)
    envelope = np.exp(-alpha * x)
    V_total = envelope * np.abs(1 + Gamma * np.exp(-2j * k * x))  # magnitude of standing wave
    V_refl_real = envelope * np.abs(Gamma) * np.cos(2 * k * x + np.angle(Gamma))  # real reflected wave
    return V_total, V_refl_real

# Initial data
x = np.linspace(0, distance_default, 1000)
V_total, V_refl_real = compute_waves(x, line_length_default, alpha_default, R_default, X_default)

# Plot setup
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.65)
[line_total] = ax.plot(x, V_total, lw=2, label='|V(z)| Total Voltage')
[line_refl] = ax.plot(x, V_refl_real, lw=2, linestyle='--', label='Re{Reflected Wave}')
ax.set_xlabel('Distance along line (m)')
ax.set_ylabel('Voltage')
ax.set_title('Standing Wave with Complex Load Impedance')
ax.set_ylim(-2, 2)
ax.grid(True)
ax.legend()

# Sliders
ax_distance = plt.axes([0.25, 0.5, 0.65, 0.03])
ax_length = plt.axes([0.25, 0.45, 0.65, 0.03])
ax_alpha = plt.axes([0.25, 0.4, 0.65, 0.03])
ax_R = plt.axes([0.25, 0.35, 0.65, 0.03])
ax_X = plt.axes([0.25, 0.3, 0.65, 0.03])

slider_distance = Slider(ax_distance, 'Propagation Distance (m)', 0.5, 5.0, valinit=distance_default)
slider_length = Slider(ax_length, 'Line Length (m)', 0.1, 2.0, valinit=line_length_default)
slider_alpha = Slider(ax_alpha, 'Attenuation (Np/m)', 0.0, 2.0, valinit=alpha_default)
slider_R = Slider(ax_R, 'Resistance R (Ω)', 1.0, 200.0, valinit=R_default)
slider_X = Slider(ax_X, 'Reactance X (Ω)', -200.0, 200.0, valinit=X_default)

# Update function
def update(val):
    distance = slider_distance.val
    length = slider_length.val
    alpha = slider_alpha.val
    R = slider_R.val
    X = slider_X.val
    x = np.linspace(0, distance, 1000)
    V_total, V_refl_real = compute_waves(x, length, alpha, R, X)
    line_total.set_xdata(x)
    line_total.set_ydata(V_total)
    line_refl.set_xdata(x)
    line_refl.set_ydata(V_refl_real)
    ax.set_xlim(0, distance)
    fig.canvas.draw_idle()

slider_distance.on_changed(update)
slider_length.on_changed(update)
slider_alpha.on_changed(update)
slider_R.on_changed(update)
slider_X.on_changed(update)

plt.show()
