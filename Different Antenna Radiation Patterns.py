import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, RadioButtons

# ----- Radiation Pattern Models -----
def isotropic(theta, freq):
    return np.ones_like(theta)

def dipole(theta, freq):
    wavelength = 3e8 / freq
    k = 2 * np.pi / wavelength
    return np.abs(np.sin(theta))  # normalized pattern for short dipole

def yagi(theta, freq):
    return np.abs(np.cos(theta) * np.sin(2 * theta))**2  # toy model for directional beam

# ----- Mapping Types -----
antenna_models = {
    'Isotropic': isotropic,
    'Dipole': dipole,
    'Yagi-style': yagi,
}

# ----- Initial Parameters -----
initial_freq = 1e9  # 1 GHz
initial_type = 'Dipole'
theta = np.linspace(0, 2 * np.pi, 360)

# ----- Plot Setup -----
fig = plt.figure(figsize=(8, 6))
ax = plt.subplot(111, polar=True)
plt.subplots_adjust(left=0.25, bottom=0.25)

# Initial plot
pattern = antenna_models[initial_type](theta, initial_freq)
line, = ax.plot(theta, pattern)
ax.set_title("Antenna Radiation Pattern", va='bottom')

# ----- Sliders and Radio Buttons -----
# Frequency slider
axfreq = plt.axes([0.25, 0.1, 0.65, 0.03])
sfreq = Slider(axfreq, 'Frequency (Hz)', 100e6, 10e9, valinit=initial_freq, valstep=1e6)

# Antenna type radio buttons
axtype = plt.axes([0.025, 0.5, 0.15, 0.25])
rtype = RadioButtons(axtype, ('Isotropic', 'Dipole', 'Yagi-style'), active=1)

# ----- Update Function -----
def update(val):
    freq = sfreq.val
    ant_type = rtype.value_selected
    new_pattern = antenna_models[ant_type](theta, freq)
    line.set_ydata(new_pattern)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()

sfreq.on_changed(update)
rtype.on_clicked(update)

plt.show()
