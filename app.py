
import random
import time
from datetime import datetime
from urllib.parse import quote

import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import cv2
import plotly.graph_objects as go
import plotly.express as px


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SweetVision 3D",
    page_icon="🧁",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# SWEET DATABASE
# Values are indicative class-level estimates.
# =========================================================

FOOD_DATA = {
    "Rasmalai": {
        "density": 0.95, "sugar100": 28, "portion": 80, "emoji": "🥛"
    },
    "Rasgulla": {
        "density": 1.00, "sugar100": 32, "portion": 50, "emoji": "⚪"
    },
    "Gulab jamun": {
        "density": 1.05, "sugar100": 38, "portion": 45, "emoji": "🍯"
    },
    "Cham cham": {
        "density": 0.95, "sugar100": 35, "portion": 60, "emoji": "🍬"
    },
    "Sandesh": {
        "density": 0.90, "sugar100": 30, "portion": 50, "emoji": "🍥"
    },
    "Peda": {
        "density": 1.05, "sugar100": 35, "portion": 35, "emoji": "🟡"
    },
    "Kalakand": {
        "density": 0.95, "sugar100": 32, "portion": 50, "emoji": "🍮"
    },
    "Kaju katli": {
        "density": 1.10, "sugar100": 30, "portion": 30, "emoji": "💎"
    },
    "Barfi": {
        "density": 1.10, "sugar100": 35, "portion": 40, "emoji": "🍥"
    },
    "Laddu": {
        "density": 0.85, "sugar100": 30, "portion": 50, "emoji": "🟠"
    },
    "Motichoor laddu": {
        "density": 0.85, "sugar100": 35, "portion": 45, "emoji": "🟠"
    },
    "Besan laddu": {
        "density": 0.90, "sugar100": 30, "portion": 45, "emoji": "🟡"
    },
    "Jalebi": {
        "density": 0.75, "sugar100": 42, "portion": 60, "emoji": "🥨"
    },
    "Soan papdi": {
        "density": 0.55, "sugar100": 38, "portion": 35, "emoji": "🍰"
    },
    "Chocolate cake": {
        "density": 0.68, "sugar100": 24, "portion": 90, "emoji": "🍰"
    },
    "Cupcake": {
        "density": 0.68, "sugar100": 25, "portion": 85, "emoji": "🧁"
    },
    "Donut": {
        "density": 0.55, "sugar100": 24, "portion": 75, "emoji": "🍩"
    },
    "Brownie": {
        "density": 0.72, "sugar100": 32, "portion": 80, "emoji": "🍫"
    },
    "Cheesecake": {
        "density": 0.75, "sugar100": 28, "portion": 110, "emoji": "🍰"
    },
    "Ice cream": {
        "density": 0.60, "sugar100": 21, "portion": 100, "emoji": "🍨"
    },
    "Cookie": {
        "density": 0.75, "sugar100": 30, "portion": 35, "emoji": "🍪"
    },
    "Macaron": {
        "density": 0.65, "sugar100": 38, "portion": 25, "emoji": "🍬"
    },
    "Pastry": {
        "density": 0.70, "sugar100": 26, "portion": 100, "emoji": "🍮"
    },
    "Pancake": {
        "density": 0.65, "sugar100": 18, "portion": 100, "emoji": "🥞"
    },
    "Other sweet": {
        "density": 0.80, "sugar100": 25, "portion": 80, "emoji": "🍡"
    },
}


# Descriptive prompts help distinguish visually similar sweets.
LABEL_PROMPTS = {
    "Rasmalai": "Indian rasmalai dessert, soft flattened white paneer discs soaked in thick saffron milk, garnished with pistachios",
    "Rasgulla": "Indian rasgulla, round white spongy cottage cheese balls soaked in sugar syrup",
    "Gulab jamun": "Indian gulab jamun, round dark golden brown milk-solid balls soaked in sugar syrup",
    "Cham cham": "Bengali cham cham sweet, oval shaped milk-based dessert often coated with coconut",
    "Sandesh": "Bengali sandesh, small smooth shaped sweet made from fresh chenna or cottage cheese",
    "Peda": "Indian peda, small round dense milk fudge sweet",
    "Kalakand": "Indian kalakand, grainy white milk cake cut into square pieces",
    "Kaju katli": "Indian kaju katli, thin diamond shaped cashew nut fudge",
    "Barfi": "Indian barfi, square or diamond shaped milk fudge sweet",
    "Laddu": "Indian laddu, round sweet ball made from flour, ghee and sugar",
    "Motichoor laddu": "Indian motichoor laddu, orange round sweet made of tiny gram flour pearls",
    "Besan laddu": "Indian besan laddu, round yellow gram flour sweet balls",
    "Jalebi": "Indian jalebi, bright orange spiral shaped deep fried sweet soaked in syrup",
    "Soan papdi": "Indian soan papdi, flaky layered cube shaped sweet",
    "Chocolate cake": "a slice of chocolate cake with chocolate frosting",
    "Cupcake": "a small individual cupcake with frosting on top",
    "Donut": "a ring shaped fried doughnut with glaze",
    "Brownie": "a dense square chocolate brownie",
    "Cheesecake": "a slice of creamy cheesecake",
    "Ice cream": "a scoop of ice cream",
    "Cookie": "a baked cookie or biscuit",
    "Macaron": "a French macaron sandwich cookie",
    "Pastry": "a decorated bakery pastry",
    "Pancake": "a stack of pancakes",
    "Other sweet": "an Indian or international sweet dessert not matching the other categories",
}

LABELS = list(FOOD_DATA.keys())
SWEET_EMOJIS = ["🍩", "🍬", "🧁", "🍰", "🍯", "🍡", "🥞", "🍮", "🍪", "🍨", "🟠"]


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "page": "Home",
    "nav_radio": "Home",
    "history": [],
    "analysis": None,
    "splash_seen": False,
    "cursor_sweet": random.choice(SWEET_EMOJIS),
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def go_to(page):
    st.session_state.page = page
    st.session_state.nav_radio = page


def sync_navigation():
    st.session_state.page = st.session_state.nav_radio


def start_new_scan():
    st.session_state.analysis = None
    go_to("Analyze Food")


# =========================================================
# CUSTOM CSS AND SWEET CURSOR
# =========================================================

cursor_svg = (
    '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40">'
    '<text x="3" y="31" font-size="29">'
    + st.session_state.cursor_sweet +
    '</text></svg>'
)

cursor_url = "data:image/svg+xml," + quote(cursor_svg)

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap');

    :root {{
        --berry:#a51f43;
        --berry2:#d94367;
        --pink:#ffe7ed;
        --ink:#49202d;
    }}

    html, body, [class*="css"] {{
        font-family:'DM Sans',sans-serif;
    }}

    body, button, a, input, textarea, select,
    [data-testid="stAppViewContainer"] {{
        cursor:url("{cursor_url}") 5 5, auto;
    }}

    .stApp {{
        background:
        radial-gradient(circle at 8% 5%,#fff0f3 0,transparent 27%),
        radial-gradient(circle at 92% 20%,#ffe2e9 0,transparent 25%),
        linear-gradient(135deg,#fff9fa 0%,#fff 55%,#fff1f4 100%);
        color:var(--ink);
    }}

    [data-testid="stHeader"] {{
        background:rgba(255,249,250,.82);
    }}

    section[data-testid="stSidebar"] {{
        background:linear-gradient(180deg,#ffe8ee 0%,#ffd9e2 100%);
        border-right:1px solid #f0b8c5;
    }}

    section[data-testid="stSidebar"] * {{
        color:#76223a;
    }}

    .block-container {{
        padding-top:1.5rem;
        padding-bottom:3rem;
        max-width:1450px;
    }}

    .hero {{
        position:relative;
        overflow:hidden;
        background:linear-gradient(115deg,#fff 0%,#ffeaf0 58%,#ffd0dc 100%);
        border:1px solid #f2bdc9;
        border-radius:28px;
        padding:30px 34px;
        box-shadow:0 18px 48px #9e244012;
        animation:rise .65s ease both;
    }}

    .hero:after {{
        content:'🍩   🧁   🍡';
        position:absolute;
        right:22px;
        bottom:8px;
        font-size:42px;
        opacity:.22;
        transform:rotate(-10deg);
        pointer-events:none;
    }}

    .hero h1 {{
        font-family:'Playfair Display',serif;
        font-size:clamp(2rem,4vw,3.3rem);
        color:var(--berry);
        margin:7px 0 2px;
        line-height:1.08;
    }}

    .hero p {{
        color:#754653;
        margin:8px 0 0;
        font-size:1rem;
        max-width:760px;
    }}

    .eyebrow {{
        display:inline-block;
        background:#ffe0e8;
        color:var(--berry);
        padding:7px 13px;
        border-radius:30px;
        font-size:11px;
        font-weight:800;
        letter-spacing:1px;
    }}

    .feature-card {{
        background:rgba(255,255,255,.88);
        border:1px solid #f1c4ce;
        border-radius:20px;
        padding:20px;
        min-height:145px;
        box-shadow:0 8px 26px #9e24400a;
        transition:transform .22s ease,box-shadow .22s ease;
    }}

    .feature-card:hover {{
        transform:translateY(-6px);
        box-shadow:0 16px 32px #9e24401b;
    }}

    .feature-icon {{
        font-size:30px;
    }}

    .feature-card h3 {{
        color:var(--berry);
        font-size:17px;
        margin:8px 0 5px;
    }}

    .feature-card p {{
        color:#805562;
        font-size:13px;
        margin:0;
    }}

    .metric-card {{
        background:white;
        border:1px solid #f0c1cb;
        border-radius:18px;
        padding:16px 18px;
        box-shadow:0 7px 22px #9e24400b;
        min-height:112px;
        transition:transform .2s ease;
    }}

    .metric-card:hover {{
        transform:translateY(-4px);
    }}

    .metric-label {{
        font-size:11px;
        color:#93606c;
        font-weight:800;
        letter-spacing:.7px;
    }}

    .metric-value {{
        font-size:clamp(22px,3vw,29px);
        color:var(--berry);
        font-weight:800;
        margin-top:5px;
    }}

    .metric-note {{
        color:#98727c;
        font-size:11px;
        margin-top:2px;
    }}

    .soft-panel {{
        background:rgba(255,255,255,.9);
        border:1px solid #f1c4cd;
        border-radius:20px;
        padding:19px;
    }}

    .loading-card {{
        position:relative;
        overflow:hidden;
        text-align:center;
        padding:34px 18px;
        margin:12px 0;
        border-radius:24px;
        border:1px solid #f0bdca;
        background:linear-gradient(120deg,#fff,#ffe8ee);
    }}

    .loading-sweets span {{
        display:inline-block;
        font-size:32px;
        margin:0 9px;
        animation:bob 1s ease-in-out infinite;
    }}

    .loading-sweets span:nth-child(2) {{ animation-delay:.12s; }}
    .loading-sweets span:nth-child(3) {{ animation-delay:.24s; }}
    .loading-sweets span:nth-child(4) {{ animation-delay:.36s; }}
    .loading-sweets span:nth-child(5) {{ animation-delay:.48s; }}

    .loading-title {{
        color:var(--berry);
        font-family:'Playfair Display',serif;
        font-size:25px;
        font-weight:700;
    }}

    .loading-track {{
        height:8px;
        max-width:380px;
        margin:18px auto 0;
        background:#f8cbd5;
        border-radius:20px;
        overflow:hidden;
    }}

    .loading-track:after {{
        content:'';
        display:block;
        height:100%;
        width:40%;
        border-radius:20px;
        background:linear-gradient(90deg,#a51f43,#ff8ba5);
        animation:loadbar 1.25s ease-in-out infinite;
    }}

    div.stButton>button, div.stDownloadButton>button {{
        border-radius:13px;
        font-weight:800;
        min-height:44px;
        transition:all .2s ease;
    }}

    div.stButton>button {{
        background:linear-gradient(95deg,#a51f43,#e34c6b);
        color:white;
        border:0;
    }}

    div.stButton>button:hover {{
        background:linear-gradient(95deg,#861936,#c92f55);
        color:white;
        transform:translateY(-2px);
        box-shadow:0 8px 20px #a51f4330;
    }}

    div.stDownloadButton>button {{
        background:#fff0f3;
        color:var(--berry);
        border:1px solid #e9aab8;
    }}

    h1,h2,h3 {{
        color:#92213d;
    }}

    [data-testid="stMetric"] {{
        background:white;
        border:1px solid #f0c1cb;
        padding:14px;
        border-radius:15px;
    }}

    [data-testid="stFileUploader"] section {{
        background:#fffafd;
        border:1px dashed #df8fa2;
        border-radius:18px;
    }}

    [data-testid="stCameraInput"] {{
        border:1px solid #f1c4cd;
        border-radius:18px;
        padding:10px;
        background:#fffafd;
    }}

    .tiny-note {{
        color:#8e6873;
        font-size:12px;
    }}

    @keyframes bob {{
        0%,100% {{ transform:translateY(0) rotate(-5deg); }}
        50% {{ transform:translateY(-12px) rotate(7deg); }}
    }}

    @keyframes loadbar {{
        0% {{ transform:translateX(-110%); }}
        100% {{ transform:translateX(280%); }}
    }}

    @keyframes rise {{
        from {{ opacity:0; transform:translateY(12px); }}
        to {{ opacity:1; transform:translateY(0); }}
    }}

    @media(max-width:700px) {{
        .block-container {{
            padding:1rem .8rem 2rem;
        }}

        .hero {{
            padding:23px 20px;
            border-radius:20px;
        }}

        .hero:after {{
            font-size:25px;
            right:10px;
        }}

        .feature-card {{
            min-height:unset;
            margin-bottom:8px;
        }}
    }}

    @media(prefers-reduced-motion:reduce) {{
        *,*::before,*::after {{
            animation-duration:.01ms!important;
            transition-duration:.01ms!important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# REUSABLE UI FUNCTIONS
# =========================================================

def hero(eyebrow, title, description):
    st.markdown(
        f'<div class="hero"><span class="eyebrow">{eyebrow}</span>'
        f'<h1>{title}</h1><p>{description}</p></div>',
        unsafe_allow_html=True,
    )


def metric_card(label, value, note=""):
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def render_loading(message):
    slot = st.empty()

    slot.markdown(
        f'<div class="loading-card">'
        f'<div class="loading-sweets">'
        f'<span>🍩</span><span>🧁</span><span>🍡</span><span>🍰</span><span>🍯</span>'
        f'</div>'
        f'<div class="loading-title">A little sweetness is on its way…</div>'
        f'<p style="color:#805562">{message}</p>'
        f'<div class="loading-track"></div>'
        f'<p class="tiny-note">Preparing the vision model · Reading your dessert · Building your insights</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    return slot


# =========================================================
# AI MODEL
# =========================================================

@st.cache_resource(show_spinner=False)
def load_classifier():
    import torch
    from transformers import pipeline

    device = 0 if torch.cuda.is_available() else -1

    return pipeline(
        "zero-shot-image-classification",
        model="openai/clip-vit-base-patch32",
        device=device,
    )


def classify_sweet(img):
    classifier = load_classifier()

    # Use descriptive prompts instead of only short category names.
    prompt_to_label = {
        prompt: label
        for label, prompt in LABEL_PROMPTS.items()
    }

    prompts = list(prompt_to_label.keys())

    raw_predictions = classifier(
        img,
        candidate_labels=prompts,
        hypothesis_template="A photograph of {}.",
    )

    predictions = []

    for item in raw_predictions:
        prompt = item["label"]
        canonical_label = prompt_to_label.get(prompt, "Other sweet")

        predictions.append({
            "label": canonical_label,
            "score": float(item["score"]),
        })

    # Keep the best score for each canonical category.
    unique_predictions = {}

    for item in predictions:
        label = item["label"]

        if (
            label not in unique_predictions
            or item["score"] > unique_predictions[label]["score"]
        ):
            unique_predictions[label] = item

    predictions = sorted(
        unique_predictions.values(),
        key=lambda x: x["score"],
        reverse=True,
    )

    return predictions[:5]


# =========================================================
# IMAGE SEGMENTATION
# =========================================================

def get_mask(img):
    rgb = np.array(img.convert("RGB"))
    h, w = rgb.shape[:2]

    scale = min(1, 850 / max(h, w))

    if scale < 1:
        small = cv2.resize(
            rgb,
            (max(1, int(w * scale)), max(1, int(h * scale))),
        )
    else:
        small = rgb.copy()

    sh, sw = small.shape[:2]

    mask = np.zeros((sh, sw), np.uint8)
    bg = np.zeros((1, 65), np.float64)
    fg = np.zeros((1, 65), np.float64)

    rect = (
        max(2, int(sw * .07)),
        max(2, int(sh * .07)),
        max(1, int(sw * .86)),
        max(1, int(sh * .86)),
    )

    try:
        cv2.grabCut(
            cv2.cvtColor(small, cv2.COLOR_RGB2BGR),
            mask,
            rect,
            bg,
            fg,
            5,
            cv2.GC_INIT_WITH_RECT,
        )

        mask = np.where(
            (mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD),
            255,
            0,
        ).astype(np.uint8)

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            np.ones((5, 5), np.uint8),
        )

        if scale < 1:
            mask = cv2.resize(
                mask,
                (w, h),
                interpolation=cv2.INTER_NEAREST,
            )

        if np.count_nonzero(mask) < max(100, int(mask.size * .01)):
            raise ValueError("Foreground mask too small")

        return mask

    except Exception:
        fallback = np.zeros((h, w), np.uint8)

        cv2.ellipse(
            fallback,
            (w // 2, h // 2),
            (
                max(1, int(w * .39)),
                max(1, int(h * .39)),
            ),
            0,
            0,
            360,
            255,
            -1,
        )

        return fallback


# =========================================================
# SHAPE-BASED DEPTH VISUALIZATION
# =========================================================

def depth_shape(mask):
    distance = cv2.distanceTransform(
        (mask > 0).astype(np.uint8),
        cv2.DIST_L2,
        5,
    )

    if distance.max() > 0:
        return (distance / distance.max()).astype(np.float32)

    return distance.astype(np.float32)


def surface_figure(depth, mask):
    step = max(1, int(max(depth.shape) / 55))

    z = depth[::step, ::step].copy()
    z = np.where(mask[::step, ::step] > 0, z, np.nan)

    yy, xx = np.mgrid[0:z.shape[0], 0:z.shape[1]]

    fig = go.Figure(
        go.Surface(
            x=xx,
            y=yy,
            z=z,
            colorscale=[
                [0, "#ffd7e0"],
                [.5, "#ed8299"],
                [1, "#a52242"],
            ],
            showscale=False,
            hovertemplate=(
                "X: %{x}<br>Y: %{y}<br>"
                "Relative shape: %{z:.2f}<extra></extra>"
            ),
        )
    )

    fig.update_layout(
        height=430,
        margin=dict(l=0, r=0, t=8, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        scene=dict(
            xaxis_title="X",
            yaxis_title="Y",
            zaxis_title="Relative shape",
            bgcolor="rgba(0,0,0,0)",
            aspectmode="data",
            xaxis=dict(showbackground=False, gridcolor="#f5d8df"),
            yaxis=dict(showbackground=False, gridcolor="#f5d8df"),
            zaxis=dict(showbackground=False, gridcolor="#f5d8df"),
        ),
    )

    return fig


# =========================================================
# CREATE SWEET ANALYSIS
# =========================================================

def make_analysis(img, predictions):
    best = predictions[0]
    sweet = best["label"]

    refs = FOOD_DATA[sweet]

    mask = get_mask(img)
    depth = depth_shape(mask)

    array = np.array(img.convert("RGB"))

    tint = np.zeros_like(array)
    tint[:, :, 0] = 225
    tint[:, :, 1] = 55
    tint[:, :, 2] = 95

    alpha = (mask > 0)[:, :, None] * .28

    overlay = np.where(
        alpha,
        (array * (1 - alpha) + tint * alpha).astype(np.uint8),
        array,
    )

    mass = float(refs["portion"])
    volume = mass / refs["density"]
    sugar = mass * refs["sugar100"] / 100

    return {
        "image": img,
        "sweet": sweet,
        "confidence": float(best["score"]),
        "predictions": predictions,
        "mask": mask,
        "depth": depth,
        "overlay": overlay,
        "mass": mass,
        "density": refs["density"],
        "sugar100": refs["sugar100"],
        "volume": volume,
        "sugar": sugar,
        "time": datetime.now().strftime("%d %b %Y, %I:%M %p"),
    }


# =========================================================
# FIRST VISIT LOADING SCREEN
# =========================================================

if not st.session_state.splash_seen:
    splash = st.empty()

    splash.markdown(
        '<div class="loading-card" style="padding:60px 15px">'
        '<div class="loading-sweets">'
        '<span>🍩</span><span>🧁</span><span>🍡</span><span>🍰</span><span>🍯</span>'
        '</div>'
        '<div class="loading-title" style="font-size:34px">SweetVision 3D</div>'
        '<p style="color:#805562">A sweeter way to explore your desserts</p>'
        '<div class="loading-track"></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    time.sleep(1.0)
    splash.empty()

    st.session_state.splash_seen = True


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

with st.sidebar:
    st.markdown("## 🧁 SweetVision 3D")
    st.caption("SMART DESSERT INSIGHTS")

    st.radio(
        "EXPLORE",
        ["Home", "Analyze Food", "History", "About"],
        key="nav_radio",
        on_change=sync_navigation,
    )

    st.markdown("---")
    st.markdown("### 🍓 Your sweet studio")
    st.caption("Capture · Recognize · Explore")

    st.markdown(
        '<div class="soft-panel">'
        '<b>Quick tip</b><br>'
        '<span class="tiny-note">'
        'Use a clear photo with one dessert, good lighting and as little background clutter as possible.'
        '</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.button(
        "＋ Start a new scan",
        use_container_width=True,
        on_click=start_new_scan,
    )


page = st.session_state.page


# =========================================================
# HOME PAGE
# =========================================================

if page == "Home":

    hero(
        "AI-ASSISTED DESSERT RECOGNITION",
        "Every sweet has a story.",
        "Meet your dessert companion. Capture or upload a sweet, discover its likely type, and explore an interactive visual and nutrition summary.",
    )

    st.write("")

    st.markdown("### Your dessert journey")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            '<div class="feature-card">'
            '<div class="feature-icon">📸</div>'
            '<h3>Capture or upload</h3>'
            '<p>Use your camera or choose a photo from your device in seconds.</p>'
            '</div>',
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            '<div class="feature-card">'
            '<div class="feature-icon">🧠</div>'
            '<h3>Smart sweet recognition</h3>'
            '<p>AI compares your image with Indian and international sweet categories.</p>'
            '</div>',
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            '<div class="feature-card">'
            '<div class="feature-icon">📊</div>'
            '<h3>Explore your insights</h3>'
            '<p>View visual analysis, an interactive 3D-style surface and indicative nutrition estimates.</p>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.write("")

    left, right = st.columns([1.25, .75])

    with left:
        st.markdown("#### Ready for a little sweetness?")

        st.write(
            "Start with a photo. The app will suggest a sweet category automatically—no manual category selection needed."
        )

        st.button(
            "✨ Get Started",
            key="home_get_started",
            use_container_width=True,
            on_click=go_to,
            args=("Analyze Food",),
        )

    with right:
        st.markdown(
            '<div class="soft-panel" style="text-align:center">'
            '<div style="font-size:46px;letter-spacing:8px">🍩 🧁 🍯</div>'
            '<h3 style="margin:5px 0;color:#a51f43">Made for sweet moments</h3>'
            '<span class="tiny-note">Rasmalai · Laddu · Gulab jamun · Jalebi · Cakes</span>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.caption(
        "Recognition scores are image-text similarity scores, not guaranteed accuracy. Nutrition and volume values are indicative estimates."
    )


# =========================================================
# ANALYZE FOOD PAGE
# =========================================================

elif page == "Analyze Food":

    hero(
        "YOUR SWEET SCANNER",
        "Capture. Recognize. Enjoy.",
        "Take a live photo or upload an image. SweetVision will suggest the closest sweet category and prepare your visual insights.",
    )

    st.write("")

    st.markdown("### Choose your image source")

    source_type = st.radio(
        "Select one option",
        ["📷 Use camera", "🖼️ Upload image"],
        horizontal=True,
        label_visibility="collapsed",
        key="source_type",
    )

    source = None

    # ---------------- CAMERA ----------------

    if source_type == "📷 Use camera":

        st.markdown("#### Take a photo of your sweet")

        st.info(
            "Camera permission is controlled by your browser. "
            "If Brave previously blocked camera access, change the site permission to Allow and reload this page."
        )

        with st.expander("📷 Camera not working in Brave? Follow these steps"):

            st.markdown(
                """
                **Step 1:** Open this page in Brave.

                **Step 2:** Click the site settings icon beside the address bar.

                **Step 3:** Open Site settings and find Camera.

                **Step 4:** Change Camera permission to Allow.

                **Step 5:** Select your webcam if Brave asks which camera to use.

                **Step 6:** Reload SweetVision 3D.

                You can also open this Brave settings page:

                `brave://settings/content/camera`

                Make sure your camera is not listed under Blocked sites.

                **Windows camera permission:**

                Open Windows Settings → Privacy & security → Camera.

                Enable Camera access and Let desktop apps access your camera.
                """
            )

        try:
            source = st.camera_input(
                "Allow camera access and take a photo",
                key="sweet_camera",
            )

        except Exception as camera_error:
            st.error(
                "Camera input could not be opened. Check browser permissions or use image upload."
            )
            st.caption(str(camera_error))

        st.caption(
            "Camera access normally requires localhost or an HTTPS website. "
            "A browser permission prompt may not appear if permission was already decided earlier."
        )

    # ---------------- UPLOAD ----------------

    else:

        st.markdown("#### Choose a dessert photo")

        source = st.file_uploader(
            "Drag and drop or browse your image",
            type=["jpg", "jpeg", "png", "webp"],
            help="Supported formats: JPG, JPEG, PNG and WEBP.",
            key="sweet_upload",
        )

    # ---------------- IMAGE ANALYSIS ----------------

    if source is not None:

        try:
            img = Image.open(source).convert("RGB")

            st.markdown("#### Your selected image")

            st.image(
                img,
                use_container_width=True,
            )

            recognize_clicked = st.button(
                "✨ Recognize sweet & analyze",
                key="recognize_button",
                use_container_width=True,
                type="primary",
            )

            if recognize_clicked:

                loading_slot = render_loading(
                    "The AI model is checking the visual features of your sweet. First-time model setup may take a few minutes."
                )

                try:
                    predictions = classify_sweet(img)

                    if not predictions:
                        raise ValueError("The model did not return any predictions.")

                    result = make_analysis(img, predictions)

                    st.session_state.analysis = result

                    loading_slot.empty()

                    st.success("Sweet analysis is ready!")

                except Exception as exc:

                    loading_slot.empty()

                    st.error(
                        "The recognition model could not be loaded or run. "
                        "Check your internet connection, PyTorch installation and package versions."
                    )

                    st.exception(exc)

        except Exception as exc:
            st.error(f"Could not read this image: {exc}")

    # ---------------- REPORT ----------------

    result = st.session_state.analysis

    if result:

        st.markdown("---")
        st.markdown("## ✨ Your sweet report")

        sweet = result["sweet"]
        emoji = FOOD_DATA[sweet]["emoji"]

        st.markdown(
            f'<div class="soft-panel">'
            f'<span class="eyebrow">TOP AI MATCH</span>'
            f'<h2 style="margin:8px 0 3px;color:#a51f43">{emoji} {sweet}</h2>'
            f'<p style="margin:0;color:#805562">'
            f'Image-text similarity score: '
            f'<b>{result["confidence"]*100:.1f}%</b>'
            f' · This is not a calibrated probability.'
            f'</p></div>',
            unsafe_allow_html=True,
        )

        # Heuristic warning, not a validated confidence threshold.
        sorted_predictions = result["predictions"]

        if len(sorted_predictions) > 1:
            score_gap = (
                sorted_predictions[0]["score"]
                - sorted_predictions[1]["score"]
            )
        else:
            score_gap = 1.0

        if result["confidence"] < 0.25 or score_gap < 0.04:
            st.warning(
                "The model is not strongly distinguishing this sweet from other categories. "
                "Try a clearer photo showing the complete dessert."
            )

        st.write("")

        m1, m2, m3 = st.columns(3)

        with m1:
            metric_card(
                "ESTIMATED VOLUME",
                f'{result["volume"]:.1f} cm³',
                "Based on reference density",
            )

        with m2:
            metric_card(
                "PORTION MASS",
                f'{result["mass"]:.0f} g',
                "Typical starting serving",
            )

        with m3:
            metric_card(
                "ESTIMATED SUGAR",
                f'{result["sugar"]:.1f} g',
                "Class-level reference estimate",
            )

        overview_tab, visual_tab, nutrition_tab = st.tabs(
            ["✨ Overview", "🧊 Visual studio", "🍓 Nutrition explorer"]
        )

        # ---------------- OVERVIEW ----------------

        with overview_tab:

            a, b = st.columns([.85, 1.15])

            with a:
                st.image(
                    result["image"],
                    caption="Original dessert image",
                    use_container_width=True,
                )

            with b:

                st.markdown("### What the model noticed")

                pred_df = pd.DataFrame([
                    {
                        "Sweet": p["label"],
                        "Similarity": round(float(p["score"]) * 100, 1),
                    }
                    for p in result["predictions"]
                ])

                fig = px.bar(
                    pred_df.sort_values("Similarity"),
                    x="Similarity",
                    y="Sweet",
                    orientation="h",
                    text="Similarity",
                    color="Similarity",
                    color_continuous_scale=[
                        "#ffd5df",
                        "#d94367",
                        "#8f1d39",
                    ],
                )

                fig.update_traces(
                    texttemplate="%{text:.1f}%",
                    textposition="outside",
                    cliponaxis=False,
                )

                fig.update_layout(
                    height=380,
                    margin=dict(l=0, r=35, t=8, b=8),
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    coloraxis_showscale=False,
                    xaxis_title="Image-text similarity (%)",
                    yaxis_title="",
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                )

                st.caption(
                    "The other matches are alternatives considered by the vision-language model."
                )

        # ---------------- VISUAL STUDIO ----------------

        with visual_tab:

            v1, v2 = st.columns(2)

            with v1:

                st.image(
                    result["overlay"],
                    caption="Approximate foreground highlight",
                    use_container_width=True,
                )

                st.image(
                    result["mask"],
                    caption="Foreground mask",
                    use_container_width=True,
                )

            with v2:

                st.image(
                    result["depth"],
                    caption="Shape-based depth visualization",
                    use_container_width=True,
                    clamp=True,
                )

                st.plotly_chart(
                    surface_figure(
                        result["depth"],
                        result["mask"],
                    ),
                    use_container_width=True,
                )

            st.caption(
                "The depth-style image and 3D surface are shape visualizations, not calibrated physical reconstruction."
            )

        # ---------------- NUTRITION EXPLORER ----------------

        with nutrition_tab:

            st.markdown("### Adjust the portion size")

            adjusted_mass = st.slider(
                "Estimated portion mass (grams)",
                10,
                400,
                int(result["mass"]),
                5,
                key="adjusted_mass",
            )

            ref = FOOD_DATA[sweet]

            adjusted_volume = adjusted_mass / ref["density"]
            adjusted_sugar = adjusted_mass * ref["sugar100"] / 100

            n1, n2, n3 = st.columns(3)

            with n1:
                metric_card(
                    "PORTION MASS",
                    f"{adjusted_mass} g",
                )

            with n2:
                metric_card(
                    "ESTIMATED VOLUME",
                    f"{adjusted_volume:.1f} cm³",
                )

            with n3:
                metric_card(
                    "ESTIMATED SUGAR",
                    f"{adjusted_sugar:.1f} g",
                )

            donut = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            "Estimated sugar",
                            "Other portion mass",
                        ],
                        values=[
                            adjusted_sugar,
                            max(0, adjusted_mass - adjusted_sugar),
                        ],
                        hole=.68,
                        marker=dict(
                            colors=["#bd3157", "#ffe0e8"]
                        ),
                        textinfo="label+percent",
                    )
                ]
            )

            donut.update_layout(
                height=300,
                margin=dict(l=0, r=0, t=15, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
            )

            st.plotly_chart(
                donut,
                use_container_width=True,
            )

            st.caption(
                "Sugar is estimated from a typical class-level sugar fraction. Actual recipes and portion composition vary."
            )

        # ---------------- SAVE AND DOWNLOAD ----------------

        save_col, download_col = st.columns(2)

        with save_col:

            if st.button(
                "💾 Save this analysis to history",
                use_container_width=True,
            ):

                row = {
                    "Date": result["time"],
                    "Sweet": sweet,
                    "Match score": f'{result["confidence"]*100:.1f}%',
                    "Mass (g)": adjusted_mass,
                    "Volume (cm³)": round(adjusted_volume, 1),
                    "Sugar (g)": round(adjusted_sugar, 1),
                }

                st.session_state.history.insert(0, row)

                st.success("Saved to your session history.")

        with download_col:

            report = pd.DataFrame([
                {
                    "Sweet": sweet,
                    "Model similarity": result["confidence"],
                    "Mass (g)": adjusted_mass,
                    "Volume (cm³)": adjusted_volume,
                    "Sugar (g)": adjusted_sugar,
                    "Date": result["time"],
                }
            ]).to_csv(index=False).encode("utf-8")

            st.download_button(
                "⬇️ Download report (CSV)",
                report,
                "sweetvision_analysis.csv",
                "text/csv",
                use_container_width=True,
            )

        st.caption(
            "Estimation method: volume = portion mass ÷ reference density; "
            "sugar = portion mass × reference sugar fraction. "
            "Values are illustrative class-level estimates, not laboratory-verified dietary measurements."
        )


# =========================================================
# HISTORY PAGE
# =========================================================

elif page == "History":

    hero(
        "YOUR DESSERT JOURNAL",
        "A history of sweet discoveries.",
        "Your saved analyses from this browser session.",
    )

    st.write("")

    if st.session_state.history:

        df = pd.DataFrame(st.session_state.history)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

        col1, col2 = st.columns(2)

        with col1:

            st.download_button(
                "⬇️ Export history",
                df.to_csv(index=False).encode("utf-8"),
                "sweetvision_history.csv",
                "text/csv",
                use_container_width=True,
            )

        with col2:

            if st.button(
                "🗑️ Clear history",
                use_container_width=True,
            ):

                st.session_state.history = []
                st.rerun()

    else:

        st.markdown(
            '<div class="soft-panel" style="text-align:center;padding:42px 15px">'
            '<div style="font-size:48px">🍡</div>'
            '<h3>No saved scans yet</h3>'
            '<p class="tiny-note">Your sweet discoveries will appear here after you save an analysis.</p>'
            '</div>',
            unsafe_allow_html=True,
        )

        st.button(
            "Start your first scan",
            on_click=go_to,
            args=("Analyze Food",),
        )


# =========================================================
# ABOUT PAGE
# =========================================================

else:

    hero(
        "BEHIND THE SWEETNESS",
        "How SweetVision 3D works.",
        "A visual dessert-recognition experience built with Python and computer-vision tools.",
    )

    st.write("")

    st.markdown("### The analysis journey")

    steps = st.columns(4)

    items = [
        (
            "📷",
            "Capture",
            "Upload a dessert photo or take one using your device camera.",
        ),
        (
            "🧠",
            "Recognize",
            "CLIP ranks the available sweet labels using image-text similarity.",
        ),
        (
            "✂️",
            "Extract",
            "OpenCV GrabCut creates an approximate foreground mask.",
        ),
        (
            "📊",
            "Explore",
            "See shape-based visuals and indicative class-level nutrition estimates.",
        ),
    ]

    for col, (icon, title, desc) in zip(steps, items):

        with col:

            st.markdown(
                f'<div class="feature-card">'
                f'<div class="feature-icon">{icon}</div>'
                f'<h3>{title}</h3>'
                f'<p>{desc}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

    st.markdown("### Technologies")

    st.write(
        "Python · Streamlit · Hugging Face Transformers · CLIP · "
        "PyTorch · OpenCV · Plotly · NumPy · Pandas"
    )

    st.markdown("### Important notes")

    st.info(
        "Sweet recognition uses a general zero-shot vision-language model. "
        "Its scores are similarity scores, not calibrated probabilities, "
        "and visually similar sweets may be confused. The foreground mask "
        "is an approximate GrabCut result. The depth-style display is derived "
        "from mask shape rather than measured depth. Portion mass, density "
        "and sugar values are class-level references and should not be treated "
        "as medical or laboratory nutrition measurements."
    )

    st.markdown("### Camera permission")

    st.write(
        "The camera control is provided by Streamlit. The browser asks for "
        "permission when you use the camera. Camera access normally works on "
        "localhost or an HTTPS deployment. If access was denied, open the "
        "browser site-permission settings, set Camera to Allow, then reload "
        "the page."
    )

    st.markdown("### Supported sweet categories")

    st.write(
        ", ".join(FOOD_DATA.keys())
    )
