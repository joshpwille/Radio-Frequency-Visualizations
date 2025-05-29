import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Constants
c = 3e8  # Speed of light in m/s

# Free-space path loss function (in dB)
def fspl(distance, frequency):
    wavelength = c / frequency
    return 20 * np.log10(distance) + 20 * np.log10(frequency) - 147.55  # FSPL in dB

# Initial parameters
distance_range = np.linspace(1, 1000, 1000)  # 1 m to 1000 m
initial_frequency = 1e9  # 1 GHz

# Calculate initial attenuation
initial_attenuation = fspl(distance_range, initial_frequency)

# Plotting setup
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.25)
line, = ax.plot(distance_range, initial_attenuation, lw=2)
ax.set_xlabel('Distance (m)')
ax.set_ylabel('Attenuation (dB)')
ax.set_title('RF Attenuation vs Distance')
ax.grid(True)

# Slider axis and widget
ax_freq = plt.axes([0.25, 0.1, 0.65, 0.03])
slider_freq = Slider(ax_freq, 'Frequency (GHz)', 0.1, 10.0, valinit=initial_frequency / 1e9)

# Update function
def update(val):
    freq_hz = slider_freq.val * 1e9
    new_atten = fspl(distance_range, freq_hz)
    line.set_ydata(new_atten)
    fig.canvas.draw_idle()

slider_freq.on_changed(update)

plt.show()
