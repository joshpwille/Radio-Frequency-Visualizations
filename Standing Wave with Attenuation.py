import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Reflection coefficient (fixed)
Gamma = 0.5  # Partial reflection

# Default values
distance_default = 2.0  # meters
line_length_default = 1.0  # meters (wavelength-scale)
alpha_default = 0.5  # Np/m (attenuation constant)

# Standing wave function with attenuation
def standing_wave(x, line_length, alpha):
    k = 2 * np.pi / line_length
    envelope = np.exp(-alpha * x)
    interference = np.abs(1 + Gamma * np.exp(-2j * k * x))
    return envelope * interference

# Initial values
x = np.linspace(0, distance_default, 1000)
y = standing_wave(x, line_length_default, alpha_default)

# Plot setup
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.45)
[line] = ax.plot(x, y, lw=2)
ax.set_xlabel('Distance along line (m)')
ax.set_ylabel('Voltage Magnitude |V(z)|')
ax.set_title('Standing Wave Pattern with Attenuation')
ax.grid(True)

# Sliders
ax_distance = plt.axes([0.25, 0.3, 0.65, 0.03])
ax_length = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_alpha = plt.axes([0.25, 0.2, 0.65, 0.03])

slider_distance = Slider(ax_distance, 'Propagation Distance (m)', 0.5, 5.0, valinit=distance_default)
slider_length = Slider(ax_length, 'Line Length (m)', 0.1, 2.0, valinit=line_length_default)
slider_alpha = Slider(ax_alpha, 'Attenuation (Np/m)', 0.0, 2.0, valinit=alpha_default)

# Update function
def update(val):
    distance = slider_distance.val
    length = slider_length.val
    alpha = slider_alpha.val
    x = np.linspace(0, distance, 1000)
    y = standing_wave(x, length, alpha)
    line.set_xdata(x)
    line.set_ydata(y)
    ax.set_xlim(0, distance)
    ax.set_ylim(0, 2)
    fig.canvas.draw_idle()

slider_distance.on_changed(update)
slider_length.on_changed(update)
slider_alpha.on_changed(update)

plt.show()
