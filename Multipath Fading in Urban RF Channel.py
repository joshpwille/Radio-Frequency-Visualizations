import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Constants
frequency = 2.4e9  # Frequency in Hz (e.g., 2.4 GHz for Wi-Fi)
c = 3e8  # Speed of light (m/s)
wavelength = c / frequency

# Initial parameters
num_paths_init = 12
distance_init = 200  # in meters

# Multipath fading simulation
def multipath_fading(num_paths, distance):
    np.random.seed(42)
    path_amplitudes = np.random.rayleigh(scale=0.5, size=num_paths)
    path_phases = np.random.uniform(0, 2 * np.pi, num_paths)
    path_delays = np.random.uniform(0, distance / c, num_paths)
    
    t = np.linspace(0, 1e-6, 1000)
    signal = np.zeros_like(t, dtype=complex)

    for amp, phase, delay in zip(path_amplitudes, path_phases, path_delays):
        signal += amp * np.exp(1j * (2 * np.pi * frequency * (t - delay) + phase))

    return t * 1e6, 20 * np.log10(np.abs(signal))

# Plot setup
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.3)
t, magnitude = multipath_fading(num_paths_init, distance_init)
line, = ax.plot(t, magnitude, label='Received Signal Magnitude')

ax.set_xlabel('Time (μs)')
ax.set_ylabel('Magnitude (dB)')
ax.set_title('Multipath Fading in Urban RF Channel')
ax.grid(True)
ax.legend()

# Slider setup
ax_paths = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_distance = plt.axes([0.25, 0.1, 0.65, 0.03])

slider_paths = Slider(ax_paths, 'Num Paths', 1, 20, valinit=num_paths_init, valstep=1)
slider_distance = Slider(ax_distance, 'Distance (m)', 10, 500, valinit=distance_init)

# Update function
def update(val):
    num_paths = int(slider_paths.val)
    distance = slider_distance.val
    t, magnitude = multipath_fading(num_paths, distance)
    line.set_data(t, magnitude)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

slider_paths.on_changed(update)
slider_distance.on_changed(update)

plt.show()
