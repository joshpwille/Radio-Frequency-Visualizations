# Place these import statements at the very beginning of your file.
import math       # for mathematical operations
import cmath      # for complex math (to compute the square root of complex numbers)
import numpy as np  # for handling arrays and frequency sweep
import matplotlib.pyplot as plt  # for plotting the curve

# Define the main function.
def main():
    # --- Step 1: Display header and get user inputs ---
    print("Calc Dist. Parameters for Coax")
    print("")  # Blank line for spacing

    # Prompt the user to enter the coaxial cable parameters.
    a = float(input("inner radius, in mm, = "))      # inner radius (mm)
    b = float(input("outer radius, in mm, = "))      # outer radius (mm)
    er = float(input("relative permittivity, er= "))  # relative permittivity (dimensionless)
    sigd = float(input("diel. conductivity,S/m, = "))  # dielectric conductivity (S/m)
    sigc = float(input("cond. conductivity,S/m, = "))  # conductor conductivity (S/m)
    f_input = float(input("frequency, in Hz, = "))     # operating frequency (Hz)

    print("")  # Blank line for spacing

    # --- Step 2: Define constants ---
    eo = 8.854e-12  # free space permittivity (F/m)
    muo = math.pi * 4e-7  # free space permeability (H/m)

    # --- Step 3: Calculate distributed parameters (which are independent of frequency except R) ---
    # Note: log(b/a) is dimensionless since both are in mm.
    L = muo * math.log(b / a) / (2 * math.pi)           # Distributed inductance (H/m)
    G = 2 * math.pi * sigd / math.log(b / a)              # Distributed conductance (S/m)
    C = 2 * math.pi * er * eo / math.log(b / a)           # Distributed capacitance (F/m)

    # Calculate the frequency-dependent distributed resistance at the input frequency.
    # Rs is calculated using the skin effect formula.
    Rs_input = math.sqrt(math.pi * f_input * muo / sigc)
    R_input = (1000 * ((1 / a) + (1 / b)) * Rs_input) / (2 * math.pi)  # Distributed resistance (ohm/m)

    # --- Step 4: Display the calculated results for the provided frequency ---
    print("Calculated Distributed Parameters at f = {:.2e} Hz:".format(f_input))
    print("C = {:.4e} F/m".format(C))
    print("L = {:.4e} H/m".format(L))
    print("R = {:.4e} ohm/m".format(R_input))
    print("G = {:.4e} S/m".format(G))

    # --- Step 5: Compute a frequency sweep to show the loss curve ---
    # We will sweep frequency from 1e6 Hz to 1e10 Hz.
    f_min = 1e6    # lower bound frequency in Hz
    f_max = 1e10   # upper bound frequency in Hz
    num_points = 500  # number of frequency points in the sweep
    freqs = np.linspace(f_min, f_max, num_points)

    # Initialize an array to store the attenuation (loss) values.
    attenuation_dB = np.zeros_like(freqs)

    # For each frequency in the sweep, calculate the frequency-dependent distributed resistance and propagation constant.
    # The propagation constant gamma is given by: gamma = sqrt((R + jωL)*(G + jωC))
    # The attenuation constant (alpha) is the real part of gamma (in nepers/m), and we convert it to dB/m.
    for i, f in enumerate(freqs):
        omega = 2 * math.pi * f
        # Calculate the frequency-dependent resistance for this frequency.
        Rs = math.sqrt(math.pi * f * muo / sigc)
        R_val = (1000 * ((1 / a) + (1 / b)) * Rs) / (2 * math.pi)
        # Calculate the propagation constant gamma.
        gamma = cmath.sqrt((R_val + 1j * omega * L) * (G + 1j * omega * C))
        alpha = gamma.real  # attenuation constant in nepers/m
        attenuation_dB[i] = 8.686 * alpha  # convert from nepers/m to dB/m

    # --- Step 6: Plot the attenuation loss curve ---
    plt.figure(figsize=(10, 6))
    plt.plot(freqs, attenuation_dB, label='Attenuation (dB/m)')
    plt.xscale('log')  # Use logarithmic scale for frequency
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Attenuation (dB/m)")
    plt.title("Frequency Response of Coaxial Cable Loss")
    plt.grid(True, which="both", ls="--", lw=0.5)
    plt.legend()
    plt.show()

# This block ensures that the main function is executed when the script is run.
if __name__ == "__main__":
    main()
