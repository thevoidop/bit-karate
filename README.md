# 🥋 Bit‑Karate: Bit‑Plane Reduction & Image Compression Dashboard

**Chop away the noise. Reduce image size without losing the essence.**

A modern [Streamlit](https://streamlit.io) web application that demonstrates _bit‑plane slicing_, a technique to reduce the colour depth of an image by discarding the least significant bits.  
The result is a visibly coarser image that occupies **less disk space** when stored in a lossless format (PNG).
This updated version features a highly interactive UI with real-time quality metrics and pixel density distributions.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive-purple)](https://plotly.com/python/)

---

## 🧠 Overview

**Bit‑Karate** chops away the _least meaningful_ binary information from an image.  
You control the aggressive “bit‑karate chop” with a slider (1–8 bits). At **8 bits** the image remains untouched; at **1 bit** only the most significant bit plane is kept, resulting in a stark, posterised look.

The app features a modern 5-column dashboard showing you:

- **File size reduction** (Space Saved).
- **Unique Colour Palette** reduction.
- **PSNR (Peak Signal-to-Noise Ratio)** to objectively measure visual quality loss.
- A live **before/after visual comparison**.
- **Interactive Plotly histograms** showing exactly how the pixel intensities shift.

Everything is wrapped in a custom dark UI with cyber-gradients, neon accents, and responsive metrics.

---

## ⚙️ How It Works

For each pixel’s R, G and B channel, the binary representation is **masked** to keep only the highest `n` bits.  
For example, if you keep **3 bits** (n=3), the mask is `11100000` (decimal `224`).  
All lower bits become zero, effectively removing subtle colour differences and throwing away entropy that lossless compression can exploit.

Mathematically:

```python
new_pixel_value = original_pixel_value & (0xFF << (8 - n))
```

Because the image contains fewer distinct values, a **PNG (lossless) compression** can pack the data much more tightly.

---

## 🤔 Why Bit‑Plane Reduction Matters

- **Educational** – Understand how digital images store colour, how distributions shift, and how compression works at the bit level.

---

## ✨ Features

- **Interactive Dashboard** – 5-column responsive layout detailing Sizes, Space Saved, Color Counts, and PSNR.
- **Interactive Distributions** – Beautiful, hoverable Plotly histograms comparing original vs. reduced pixel densities.
- **Real‑time processing** – Instant preview after upload and slider adjustments.
- **Fair size comparison** – Always compares **PNG to PNG** to avoid misleading results.
- **Vibrant Cyber UI** – Custom CSS with gradient titles, dynamic quality badges, and a sleek dark theme.

---

## 💻 Installation & Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/thevoidop/bit-karate.git
cd bit-karate
```

### 2. Set up a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt** should contain:

```text
streamlit>=1.29.0
numpy>=1.24.0
Pillow>=9.5.0
plotly>=5.10.0
```

### 4. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🕹️ Usage Guide

1. **Upload an image** – Use the sidebar to upload a JPG, JPEG, or PNG file.
2. **Adjust the slider** – Move the “Bits per channel” slider in the sidebar.  
   _1 = most aggressive chop (tiny file, extreme posterisation)_  
   _8 = original quality (file size unchanged)_
3. **Analyze the Data** – Check the top metric row for storage saved and PSNR quality. Scroll down to hover over the Plotly histograms to see exactly which pixel intensities were grouped together.
4. **Download** – Click the primary download button to get the reduced image.

---

## 🔧 Technical Deep‑Dive: Lossless vs Lossy

**Why PNG instead of JPEG for the output?**  
Bit-plane reduction destroys smooth gradients by creating sharp steps (banding) between colours. JPEG compression relies on the Discrete Cosine Transform (DCT) which handles smooth gradients beautifully but struggles heavily with sharp, high-frequency steps.

If you save a bit-chopped image as a JPEG, the file size will often _increase_. Therefore, the app strictly calculates baseline sizes by converting the input to PNG in memory, and outputs the chopped file as a PNG. This ensures the lossless algorithm (DEFLATE) can take full advantage of the reduced entropy.

---

## 📁 Project Structure

```text
bit-karate/
├── app.py              # Main Streamlit application (UI, Logic, Plotly charts)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

---

## 🎨 Customisation

The app uses **custom CSS injected into Streamlit** to create its vibrant dark look. You can modify:

- **Gradients**: Adjust the `linear-gradient` hex codes in the `.main-title` and `.quality-pill` CSS classes in `app.py`.
- **Plotly Colors**: Change the `marker_color` properties in the `create_modern_histogram` function to match your preferred aesthetic.

---

## 📃 License

This project is open‑source and available under the [MIT License](LICENSE).
