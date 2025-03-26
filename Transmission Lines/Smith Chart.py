import numpy as np         # for numerical operations and arrays
import matplotlib.pyplot as plt  # for plotting
import cmath               # for complex math (e.g., tanh)

def z2gamma(z):
    """
    Convert impedance to reflection coefficient.
    For a given impedance z, the reflection coefficient gamma is:
         gamma = (z - 1) / (z + 1)
    """
    return (z - 1) / (z + 1)

def realcirc(r, ax=None):
    """
    Draw a circle of constant real part (a resistance circle) on the Smith Chart.
    The circle is defined by:
         a = 1/(1 + r)
         center = (r/(1 + r), 0)
    and plotted as z = a*cos(theta) + center.
    Parameters:
      r  : resistance value (real, normalized)
      ax : matplotlib axes (optional). If None, uses current axes.
    """
    if ax is None:
        ax = plt.gca()
    # Create theta values (0 to 2pi) in radians.
    theta = np.linspace(0, 2*np.pi, 360)
    a_val = 1 / (1 + r)
    m = r / (1 + r)
    n = 0
    Re = a_val * np.cos(theta) + m
    Im = a_val * np.sin(theta) + n
    ax.plot(Re, Im, 'k')  # Plot in black
    # Return the complex points (if needed later)
    return Re + 1j * Im

def imcirc(x, ax=None):
    """
    Draw a circle of constant imaginary part (a reactance circle) on the Smith Chart.
    For a given reactance x, the circle is defined by:
         a = |1/x|
         center = (1, 1/x)
    Only points within the unit circle (|gamma| <= 1) are plotted.
    Parameters:
      x  : reactance value (real, normalized)
      ax : matplotlib axes (optional). If None, uses current axes.
    """
    if ax is None:
        ax = plt.gca()
    a_val = abs(1/x)
    m = 1
    n = 1/x
    theta = np.linspace(0, 2*np.pi, 360)
    Re = a_val * np.cos(theta) + m
    Im = a_val * np.sin(theta) + n
    z = Re + 1j * Im
    # Only keep points that lie inside the unit circle.
    mask = np.abs(z) <= 1
    ax.plot(Re[mask], Im[mask], 'k')
    return z[mask]

def main():
    # Create a new figure and axes.
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # --- Plot the outer (unit) circle of the Smith Chart ---
    theta = np.linspace(-np.pi, np.pi, 180)
    a_val = 1
    m = 0
    n = 0
    Re = a_val * np.cos(theta) + m
    Im = a_val * np.sin(theta) + n
    ax.plot(Re, Im, 'k')  # Outer circle in black
    ax.axis('equal')
    ax.axis('off')
    
    # --- Add the horizontal line (x = 0 line) ---
    ax.plot([-1, 1], [0, 0], 'k')
    
    # --- Draw the real circles (constant resistance lines) ---
    rvalues = [0.5, 1, 2, 4]
    for r in rvalues:
        # Call realcirc to plot the circle.
        realcirc(r, ax=ax)
        # Compute text position using z2gamma (for a real impedance, z2gamma returns a real value).
        gamma_val = z2gamma(r)
        xpos = gamma_val.real  # Should be real
        # Place the text label at (xpos, 0) with vertical alignment 'top' and horizontal alignment 'right'.
        ax.text(xpos, 0, str(r), verticalalignment='top', horizontalalignment='right')
    
    # --- Draw the imaginary circles (constant reactance lines) ---
    xvalues = [0.2, 0.5, 1, 2]
    for x in xvalues:
        # Plot the circle for positive and negative reactance.
        imcirc(x, ax=ax)
        imcirc(-x, ax=ax)
        # Compute text positions using z2gamma for a pure imaginary impedance.
        gamma_val = z2gamma(1j * x)
        xpos = gamma_val.real
        ypos = gamma_val.imag
        # Place two text labels: one for +j{x} and one for -j{x}.
        text1 = ax.text(xpos, ypos, ' j' + str(x), verticalalignment='bottom')
        text2 = ax.text(xpos, -ypos, '-j' + str(x), verticalalignment='top')
        # Adjust horizontal alignment based on the x position.
        if xpos == 0:
            text1.set_horizontalalignment('center')
            text2.set_horizontalalignment('center')
        elif xpos < 0:
            text1.set_horizontalalignment('right')
            text2.set_horizontalalignment('right')
    
    # --- Add the '0' label at the leftmost point of the Smith Chart ---
    ax.text(-1, 0, '0', verticalalignment='center', horizontalalignment='right')
    
    # Display the Smith Chart.
    plt.show()

if __name__ == "__main__":
    main()
