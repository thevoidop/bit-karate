import streamlit as st
import numpy as np
from PIL import Image
import io
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- Page Config ---
st.set_page_config(page_title="Bit-Karate", layout="wide", page_icon="🥋")

# --- Custom CSS (Modern, Gradient, Vibrant) ---
st.markdown(
    """
<style>
    /* Gradient Main Title */
    .main-title {
        text-align: center;
        background: linear-gradient(90deg, #00f2fe 0%, #4facfe 50%, #00f2fe 100%);
        background-size: 200% auto;
        color: transparent;
        -webkit-background-clip: text;
        background-clip: text;
        font-weight: 900;
        font-size: 4rem;
        margin-bottom: 0px;
        animation: shine 3s linear infinite;
    }
    
    @keyframes shine { to { background-position: 200% center; } }

    .sub-title {
        text-align: center;
        color: #94a3b8;
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 2.5rem;
    }
    
    .quality-pill {
        background: linear-gradient(145deg, #1e293b, #0f172a);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.2rem;
        margin-top: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
</style>
""",
    unsafe_allow_html=True,
)


# --- Helpers ---
def format_size(size_in_bytes):
    if size_in_bytes < 1024 * 1024:
        return f"{size_in_bytes / 1024:.2f} KB"
    return f"{size_in_bytes / (1024 * 1024):.2f} MB"


def reduce_bit_plane_simple(image_array, n_bits):
    mask = (0xFF << (8 - n_bits)) & 0xFF
    return image_array & mask


def compute_psnr(original, processed):
    mse = np.mean((original.astype(np.float64) - processed.astype(np.float64)) ** 2)
    if mse == 0:
        return float("inf")
    return 10 * np.log10(255.0**2 / mse)


def count_unique_colors(img_array):
    if img_array.ndim == 3:
        return len(np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0))
    return len(np.unique(img_array))


def create_modern_histogram(orig_array, reduced_array, n_bits):
    counts_orig, bins_orig = np.histogram(orig_array.ravel(), bins=64, range=(0, 256))
    counts_red, bins_red = np.histogram(reduced_array.ravel(), bins=64, range=(0, 256))
    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Original Distribution",
            f"Reduced Distribution ({n_bits} bits)",
        ),
    )
    fig.add_trace(
        go.Bar(
            x=bins_orig[:-1],
            y=counts_orig,
            marker_color="#c084fc",
            opacity=0.8,
            name="Original",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Bar(
            x=bins_red[:-1],
            y=counts_red,
            marker_color="#38bdf8",
            opacity=0.8,
            name="Reduced",
        ),
        row=1,
        col=2,
    )
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        height=350,
    )
    fig.update_xaxes(showgrid=False, title_text="Pixel Intensity")
    fig.update_yaxes(showgrid=True, gridcolor="#334155")
    return fig


# --- Sidebar ---
with st.sidebar:
    st.markdown("## ⚙️ App Settings")
    uploaded_file = st.file_uploader("📤 Upload Image", type=["jpg", "jpeg", "png"])
    st.markdown("---")
    n_bits = st.slider("Bits per channel", 1, 8, 3)

    desc = {
        1: ("1 bit", "Silhouette", "Severe", "#f87171"),
        2: ("2 bits", "Posterized", "Very Heavy", "#f87171"),
        3: ("3 bits", "Strong Banding", "Heavy", "#f87171"),
        4: ("4 bits", "Artistic", "Moderate", "#fbbf24"),
        5: ("5 bits", "Subtle Banding", "Light", "#fbbf24"),
        6: ("6 bits", "Near Original", "Minimal", "#34d399"),
        7: ("7 bits", "Lossless Look", "Negligible", "#34d399"),
        8: ("8 bits", "Original", "None", "#34d399"),
    }[n_bits]

    st.markdown(
        f"""
    <div class="quality-pill" style="border-left: 4px solid {desc[3]};">
        <div style="font-size:1.1rem; font-weight:800; color:{desc[3]};">{desc[0]}</div>
        <div style="font-size:0.9rem; color:#f8fafc;">{desc[1]}</div>
        <div style="font-size:0.75rem; color:#94a3b8; margin-top:8px; text-transform:uppercase;">Loss: <b>{desc[2]}</b></div>
    </div>
    """,
        unsafe_allow_html=True,
    )

# --- Main UI ---
st.markdown('<h1 class="main-title">Bit-Karate 🥋</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-title">Chop away the noise. Reduce image size. Keep the essence.</p>',
    unsafe_allow_html=True,
)

if uploaded_file:
    input_image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(input_image)

    # PNG baseline size
    orig_io = io.BytesIO()
    input_image.save(orig_io, format="PNG")
    orig_size = len(orig_io.getvalue())

    with st.spinner("Executing Karate Chop... 🥷"):
        reduced_array = reduce_bit_plane_simple(img_array, n_bits)
        reduced_image = Image.fromarray(reduced_array)
        reduced_io = io.BytesIO()
        reduced_image.save(reduced_io, format="PNG")
        reduced_size = len(reduced_io.getvalue())

    # Metrics Calculations
    savings = ((orig_size - reduced_size) / orig_size) * 100
    size_diff = orig_size - reduced_size
    psnr_val = compute_psnr(img_array, reduced_array)
    orig_colors = count_unique_colors(img_array)
    redu_colors = count_unique_colors(reduced_array)
    color_diff = orig_colors - redu_colors

    # --- 5-Column Dashboard ---
    st.markdown("### 📊 Karate Results")
    m1, m2, m3, m4, m5 = st.columns(5)

    m1.metric("Original Size", format_size(orig_size))
    m2.metric("Chopped Size", format_size(reduced_size))
    m3.metric(
        "💾 Space Saved",
        f"{savings:.1f}%",
        f"-{format_size(size_diff)}",
        delta_color="normal",
    )
    m4.metric(
        "🎨 Color Palette",
        f"{redu_colors:,}",
        f"-{color_diff:,} colors",
        delta_color="inverse",
    )
    m5.metric("✨ Quality (PSNR)", f"{psnr_val:.1f} dB")

    st.divider()

    # --- Visual Comparison ---
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📁 Original")
        st.image(input_image, width="stretch")
    with col2:
        st.markdown(f"#### ✂️ Chopped ({n_bits} Bits)")
        st.image(reduced_image, width="stretch")

    # --- Actions ---
    st.write("")
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        st.download_button(
            "⬇️ Download Result",
            data=reduced_io.getvalue(),
            file_name=f"chopped_{n_bits}bits.png",
            mime="image/png",
            width="stretch",
            type="primary",
        )

    # --- Histograms (Default Visible) ---
    st.divider()
    st.markdown("### 📈 Pixel Density Distributions")
    st.plotly_chart(
        create_modern_histogram(img_array, reduced_array, n_bits), width="stretch"
    )

else:
    st.info("👈 Upload an image in the sidebar to start!")
