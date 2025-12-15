# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import ttk
import numpy as np

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ============================================================
# 1. CONTINUOUS SIGNALS
# ============================================================

def generate_continuous_signal(sig_id):
    duration = 0.005      # 5 ms
    dt = 1e-6             # 1 MHz resolution
    t = np.arange(0, duration, dt)

    if sig_id == 1:
        x = 5*np.cos(2*np.pi*1000*t)

    elif sig_id == 2:
        x = 5*np.cos(2*np.pi*2000*t) + 3*np.cos(2*np.pi*3000*t)

    elif sig_id == 3:
        x = 5*np.cos(2*np.pi*2000*t) + 1*np.cos(2*np.pi*5000*t)

    else:
        x = 1 + np.cos(2*np.pi*2000*t) + 2*np.cos(2*np.pi*4000*t) + 3*np.cos(2*np.pi*6000*t)

    return t, x


# ============================================================
# 2. SAMPLE THE SIGNAL
# ============================================================

def sample_signal(t, x, fs=8000):
    Ts = 1.0 / fs
    n = np.arange(0, t[-1], Ts)
    xs = np.interp(n, t, x)
    return n, xs


# ============================================================
# 3. ANALYTICAL SPECTRA (ARROWS)
# ============================================================

def get_frequencies(sig_id):
    if sig_id == 1:
        return [(1000, 5/2.0)]

    elif sig_id == 2:
        return [(2000, 5/2.0), (3000, 3/2.0)]

    elif sig_id == 3:
        return [(2000, 5/2.0), (5000, 1/2.0)]

    else:
        return [(0, 1.0), (2000, 1/2.0), (4000, 2/2.0), (6000, 3/2.0)]


def spectrum_sampled(sig_id, fs, fmax):
    """Replicate spectrum every fs with proper amplitude summation."""
    base = get_frequencies(sig_id)
    # Use dictionary to accumulate amplitudes
    freq_dict = {}
    
    kmax = int(fmax / fs) + 2
    
    for k in range(-kmax, kmax+1):
        for (f, a) in base:
            f_rep = f + k * fs
            
            # Handle negative frequencies (mirror to positive)
            if f_rep < 0:
                f_rep = abs(f_rep)
            
            if 0 <= f_rep <= fmax:
                # Accumulate amplitude if frequency already exists
                if f_rep in freq_dict:
                    freq_dict[f_rep] += a
                else:
                    freq_dict[f_rep] = a
    
    # Convert to lists
    freqs = list(freq_dict.keys())
    amps = list(freq_dict.values())
    
    return freqs, amps

def ideal_lowpass(freqs, amps, fc):
	"""Ideal LPF applied to spectral lines."""
	f_out = []
	a_out = []

	for f, a in zip(freqs, amps):
		if abs(f) <= fc:
			f_out.append(f)
			a_out.append(a)

	return f_out, a_out

def get_max_frequency(sig_id):
	base = get_frequencies(sig_id)
	return max(abs(f) for f, _ in base)

# ============================================================
# 4. PLOT INTO A TAB
# ============================================================

def build_tab(tab_frame, sig_id):
	# --- Prepare figure ---
	fig = Figure(figsize=(8, 6))

	ax1 = fig.add_subplot(2, 2, 1)
	ax2 = fig.add_subplot(2, 2, 2)
	ax3 = fig.add_subplot(2, 2, 3)
	ax4 = fig.add_subplot(2, 2, 4)

    # ---------------------------------------------------------
    # ORIGINAL SIGNAL
    # ---------------------------------------------------------
	t, x = generate_continuous_signal(sig_id)
	ax1.plot(t*1000, x)  # ms
	ax1.set_title("Original signal x(t)")
	ax1.set_ylabel("Amplitude")
	ax1.set_ylim(1.2 * x.min(), 1.2 * x.max())

    # ---------------------------------------------------------
    # CONTINUOUS SPECTRUM (ARROWS)
    # ---------------------------------------------------------
	base = get_frequencies(sig_id)
	f0 = [f for (f, a) in base]
	a0 = [a for (f, a) in base]

	ax2.stem(f0, a0, use_line_collection=True)
	ax2.set_title("Spectrum of x(t)")
	ax2.set_ylabel("Amplitude")
	ax2.set_ylim(0, 1.2 * 4)
	ax2.set_xlim(0, 8000)

    # ---------------------------------------------------------
    # SAMPLED SPECTRUM (REPLICATED)
    # ---------------------------------------------------------
	if sig_id == 4:
		fmax = 40000
	else:
		fmax = 20000

	frep, arep = spectrum_sampled(sig_id, 8000, fmax)

	ax3.stem(frep, arep, use_line_collection=True)
	ax3.set_xlim(0, fmax)
	ax3.set_title("Spectrum of sampled signal")
	ax3.set_ylabel("Amplitude")
	ax3.set_ylim(0, 1.2 * 4)

    # ---------------------------------------------------------
    # FILTER
    # ---------------------------------------------------------
	fc = get_max_frequency(sig_id) * 1.1

	f_filt, a_filt = ideal_lowpass(frep, arep, fc)

	ax4.stem(f_filt, a_filt, use_line_collection=True)
	ax4.set_xlim(0, fmax)
	ax4.set_ylim(0, 1.2 * 4)
	ax4.set_title("After ideal LPF (reconstruction)")
	ax4.set_ylabel("Amplitude")
    # ---------------------------------------------------------
	canvas = FigureCanvasTkAgg(fig, master=tab_frame)
	canvas.draw()
	canvas.get_tk_widget().pack(fill="both", expand=True)



# ============================================================
# 5. TKINTER GUI
# ============================================================

root = tk.Tk()
root.title("Signal Spectrum Viewer")
root.geometry("1000x700")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# ------------------------------------------------------------
# Footer (Made by)
# ------------------------------------------------------------
footer = ttk.Label(
	root,
	text="Made by: Tagma Saif / Nadi Nuria / Lhissou Laila",
	anchor="center",
	font=("Arial", 9)
)
footer.pack(side="bottom", pady=5)


tabs = []
for i in range(4):
    frame = ttk.Frame(notebook)
    notebook.add(frame, text="Signal %d" % (i+1))
    tabs.append(frame)

# Build tabs
for i in range(4):
    build_tab(tabs[i], i+1)


root.mainloop()