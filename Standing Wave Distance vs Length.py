import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Constants
wavelength = 1.0  # normalized λ
Z_L = 0.5  # reflection coefficient magnitude (for partial reflection)

# Initial parameters
distance_default = 2.0  # meters
line_length_default = 1.0  # meters

# Standing wave function
def standing_wave(x, line_length):
    k = 2 * np.pi / line_length
    return np.abs(1 + Z_L * np.exp(-2j * k * x))

# Initial spatial domain
x = np.linspace(0, distance_default, 1000)
y = standing_wave(x, line_length_default)

# Set up figure
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.35)
[line] = ax.plot(x, y, lw=2)
ax.set_xlabel('Distance along line (m)')
ax.set_ylabel('Voltage Magnitude |V(z)|')
ax.set_title('Standing Wave Pattern')
ax.grid(True)

# Sliders
ax_distance = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_length = plt.axes([0.25, 0.15, 0.65, 0.03])

slider_distance = Slider(ax_distance, 'Propagation Distance (m)', 0.5, 5.0, valinit=distance_default)
slider_length = Slider(ax_length, 'Line Length (λ or m)', 0.1, 2.0, valinit=line_length_default)

# Update function
def update(val):
    distance = slider_distance.val
    length = slider_length.val
    x = np.linspace(0, distance, 1000)
    y = standing_wave(x, length)
    line.set_xdata(x)
    line.set_ydata(y)
    ax.set_xlim(0, distance)
    ax.set_ylim(0, 2)
    fig.canvas.draw_idle()

slider_distance.on_changed(update)
slider_length.on_changed(update)

plt.show()
