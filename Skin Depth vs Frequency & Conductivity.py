import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# Constants
mu_0 = 4 * np.pi * 1e-7  # Permeability of free space (H/m)

# Default values
sigma_default = 5.8e7  # Copper (S/m)
f_default = 1e6        # 1 MHz

# Skin depth calculation
def skin_depth(frequency, conductivity):
    omega = 2 * np.pi * frequency
    delta = np.sqrt(2 / (mu_0 * conductivity * omega))
    return delta

# Frequency and conductivity ranges
frequencies = np.logspace(3, 9, 500)       # 1 kHz to 1 GHz
conductivities = np.logspace(6, 8, 500)    # 1e6 to 1e8 S/m

# Set up figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
plt.subplots_adjust(left=0.25, bottom=0.35)

# Initial plots
depths_vs_freq = skin_depth(frequencies, sigma_default)
line1, = ax1.plot(frequencies, depths_vs_freq, color='blue')
ax1.set_xscale('log')
ax1.set_yscale('log')
ax1.set_xlabel('Frequency (Hz)')
ax1.set_ylabel('Skin Depth (m)')
ax1.set_title('Skin Depth vs Frequency')
ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

depths_vs_sigma = skin_depth(f_default, conductivities)
line2, = ax2.plot(conductivities, depths_vs_sigma, color='green')
ax2.set_xscale('log')
ax2.set_yscale('log')
ax2.set_xlabel('Conductivity (S/m)')
ax2.set_ylabel('Skin Depth (m)')
ax2.set_title('Skin Depth vs Conductivity')
ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

# Slider axes
ax_freq_slider = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_sigma_slider = plt.axes([0.25, 0.18, 0.65, 0.03])

# Sliders
s_freq = Slider(ax_freq_slider, 'Frequency (Hz)', 1e3, 1e9, valinit=f_default, valstep=1e5)
s_sigma = Slider(ax_sigma_slider, 'Conductivity (S/m)', 1e6, 6e7, valinit=sigma_default, valstep=1e6)

# Update function
def update(val):
    f = s_freq.val
    sigma = s_sigma.val

    # Update top plot (skin depth vs frequency)
    new_depths_vs_freq = skin_depth(frequencies, sigma)
    line1.set_ydata(new_depths_vs_freq)

    # Update bottom plot (skin depth vs conductivity)
    new_depths_vs_sigma = skin_depth(f, conductivities)
    line2.set_ydata(new_depths_vs_sigma)

    fig.canvas.draw_idle()

# Connect sliders
s_freq.on_changed(update)
s_sigma.on_changed(update)

plt.show()
