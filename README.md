# Signal Spectrum Viewer

A **Tkinter + Matplotlib educational tool** to visualize **continuous-time signals**, their **analytical spectra**, the effect of **sampling**, and **ideal low‑pass reconstruction**.

This project is designed for **beginners in Signals & Systems / Telecommunications** to build intuition about:

* Frequency-domain representation of cosine signals
* Spectral replication due to sampling
* Aliasing
* Ideal low-pass filtering for signal reconstruction

---

## 📌 Features

For each signal, the GUI displays **four plots**:

1. **Original signal x(t)**
   Continuous-time waveform plotted with high time resolution.

2. **Spectrum of x(t)**
   Analytical (line) spectrum using stem plots (positive frequencies).

3. **Spectrum of sampled signal**
   Replicated spectra every sampling frequency (f_s), showing aliasing when it occurs.

4. **After ideal LPF (reconstruction)**
   Ideal low‑pass filter applied to the sampled spectrum.

Each signal is displayed in its own **tab**.

---

## 🧠 Signals Included

| Signal   | Expression                                                         |
| -------- | ------------------------------------------------------------------ |
| Signal 1 | $$(5\cos(2\pi·1000t))$$                                            |
| Signal 2 | $$(5\cos(2\pi·2000t) + 3\cos(2\pi·3000t))$$                        |
| Signal 3 | $$(5\cos(2\pi·2000t) + \cos(2\pi·5000t))$$                         |
| Signal 4 | $$(1 + \cos(2\pi·2000t) + 2\cos(2\pi·4000t) + 3\cos(2\pi·6000t))$$ |

---

## ⚙️ How It Works

### 1. Continuous-Time Signal Generation

Signals are generated using a **very small time step** (1 µs) to approximate continuous time.

```python
t, x = generate_continuous_signal(sig_id)
```

---

### 2. Analytical Spectrum

Each cosine produces **two impulses** in the frequency domain.
Only **positive frequencies** are plotted for clarity.

Amplitudes are scaled by $(A/2)$, consistent with Fourier theory.

---

### 3. Sampling & Spectral Replication

Sampling at:

```
fs = 8000 Hz
```

The spectrum is **replicated every $(f_s)$**:

$$[
X_s(f) = \sum_k X(f - kf_s)
]$$

Overlapping spectral lines are **summed**, correctly showing aliasing effects.

---

### 4. Ideal Low‑Pass Filter

An **ideal LPF** keeps frequencies below:

$$[
f_c = 1.1 × f_{max}
]$$

This simulates perfect reconstruction when the **Nyquist condition** is satisfied.

---

## 🖥️ GUI Layout

* Built using **Tkinter Notebook tabs**
* Embedded **Matplotlib figures**
* Each tab corresponds to one signal

---

## 📦 Requirements

Make sure you have Python 3 installed, then install dependencies:

```bash
pip install numpy matplotlib
```

Tkinter is included by default with most Python installations.

---

## ▶️ How to Run

Save the script as `main.py` and run:

```bash
python main.py
```

A window titled **"Signal Spectrum Viewer"** will open.

---

## 🎓 Learning Objectives

By using this project, you should be able to:

* Understand why sampling creates spectral replicas
* Visually identify aliasing
* Relate time-domain cosines to frequency-domain impulses
* Understand the role of low‑pass filtering in reconstruction

---

## 🚀 Possible Extensions

* Add adjustable sampling frequency (slider)
* Show **negative frequencies** explicitly
* Add time‑domain reconstruction
* Replace ideal LPF with practical filters
* Export plots as images

---

## 📚 Target Audience

* Signals & Systems students
* Telecommunications / Networks students
* Beginners learning DSP concepts

---

## 📝 License

This project is for **educational use**.
Feel free to modify and extend it for learning purposes.

---

**Happy learning & exploring spectra! 📡📈**
