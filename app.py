"""
Laboratorio Virtual de Transistores BJT NPN de Silicio (2N3904)
Desarrollado en Streamlit - Basado en material académico:
  - Semana 7: TRANSISTORES (Polarización de Base Fija)
  - Semana 8: Fundamentos de los transistores (Polarización de Emisor)
  - Semana 10 Adicional: Polarización por Divisor de Tensión
"""

import streamlit as st
import plotly.graph_objects as go

BETA = 100          # Ganancia de corriente fija para todos los cálculos del laboratorio
VBE = 0.7           # Segunda aproximación del transistor de silicio (barrera de unión)
VCE_SAT = 0.2        # Voltaje de saturación típico (transistor como interruptor cerrado)

st.set_page_config(
    page_title="Laboratorio Virtual BJT - 2N3904",
    page_icon="🔌",
    layout="wide",
)

# ----------------------------------------------------------------------------
# ESTILOS
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    html, body, .stApp {
        background-color: #9ddb1a;
    }
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        z-index: -1;
        background-image:
            radial-gradient(circle at 8% 15%, rgba(255,255,255,0.55) 0 22px, transparent 23px),
            radial-gradient(circle at 32% 55%, rgba(255,255,255,0.55) 0 14px, transparent 15px),
            radial-gradient(circle at 60% 20%, rgba(255,255,255,0.55) 0 28px, transparent 29px),
            radial-gradient(circle at 85% 60%, rgba(255,255,255,0.55) 0 18px, transparent 19px),
            radial-gradient(circle at 15% 85%, rgba(255,255,255,0.55) 0 24px, transparent 25px),
            radial-gradient(circle at 48% 90%, rgba(255,255,255,0.55) 0 12px, transparent 13px),
            radial-gradient(circle at 75% 90%, rgba(255,255,255,0.55) 0 20px, transparent 21px),
            radial-gradient(circle at 92% 10%, rgba(255,255,255,0.55) 0 14px, transparent 15px);
        background-repeat: no-repeat;
        background-size: 100% 100%;
    }
    .block-container {
        padding: 2rem 5rem !important;
        margin-top: 1rem;
        max-width: 1400px;
    }
    .stApp, .stApp p, .stApp span, .stApp label, .stMarkdown, h1, h2, h3, h4 {
        color: #0d1117 !important;
    }
    /* Sliders (Vcc, Vee) y number_input (Rb, Rc, Re...) al 80% del ancho, centrados */
    div[data-testid="stSlider"] {
        max-width: 80%;
        margin-left: auto;
        margin-right: auto;
    }
    div[data-testid="stNumberInput"] {
        max-width: 80%;
        margin-left: auto;
        margin-right: auto;
    }
    div[data-testid="stNumberInput"] input {
        color: #0d1117 !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
    }
    div[data-testid="stSlider"] label, div[data-testid="stNumberInput"] label {
        font-size: 1rem !important;
        font-weight: 700 !important;
    }
    /* Espaciado entre columnas para evitar sensación de apretado */
    div[data-testid="stHorizontalBlock"] {
        gap: 1rem;
    }
    /* Reducir ligeramente el tamaño de las métricas (Ib, Ic, Vce, Ic(sat)) */
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        font-size: 1.55rem !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
    }
    .circuit-frame {
        background: #ffffff;
        border: 6px solid #000000;
        border-radius: 14px;
        padding: 1rem;
        margin-bottom: 0.75rem;
    }
    .chart-frame {
        background: #ffffff;
        border: 6px solid #000000;
        border-radius: 14px;
        padding: 0.5rem;
        margin-top: 0.5rem;
        margin-bottom: 0.75rem;
    }
    div[data-testid="stPlotlyChart"] {
        background: #ffffff;
        border: 6px solid #000000;
        border-radius: 14px;
        padding: 0.75rem;
        max-width: 95%;
        margin-left: auto;
        margin-right: auto;
    }
    /* Centrar el bloque de métricas (Ib, Ic, Vce, Ic(sat)) igual que la gráfica de abajo */
    div[data-testid="column"] > div > div[data-testid="stHorizontalBlock"]:has(div[data-testid="stMetric"]) {
        max-width: 95%;
        margin-left: auto;
        margin-right: auto;
    }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 8px;
        padding: 0.4rem;
    }
    .alert-ok {
        background-color: #0f3320; border: 1px solid #2ea043;
        border-radius: 10px; padding: 1rem; color: #7ee2a8; font-weight: 600;
    }
    .alert-sat {
        background-color: #3a2a0f; border: 1px solid #d29922;
        border-radius: 10px; padding: 1rem; color: #f5c451; font-weight: 600;
    }
    .alert-cutoff {
        background-color: #3a0f14; border: 1px solid #da3633;
        border-radius: 10px; padding: 1rem; color: #ff9a96; font-weight: 600;
    }
    .beta-note {
        background-color: #ffffff; border-left: 5px solid #1f6feb;
        border-radius: 8px; padding: .8rem 1rem; font-size: 0.85rem; color: #0d1117 !important;
        margin-top: .5rem; margin-bottom: 1rem;
    }
    .beta-note * { color: #0d1117 !important; }

    /* Título principal centrado con tipografía Rockwell Extra Bold */
    h1 {
        text-align: center !important;
        font-family: 'Rockwell Extra Bold', 'Rockwell', 'Georgia', serif !important;
        font-weight: 800 !important;
        width: 100%;
    }

    /* Pestañas de selección de circuito: más separadas, en negrita, negro y con fondo sombreado en la activa */
    div[data-testid="stTabs"] [data-baseweb="tab-list"] {
        gap: 3.5rem;
    }
    div[data-testid="stTabs"] [data-baseweb="tab"] {
        font-weight: 800 !important;
        color: #0d1117 !important;
        font-size: 1.05rem;
        border-radius: 10px 10px 0 0;
        padding: 0.5rem 1rem;
    }
    div[data-testid="stTabs"] [data-baseweb="tab"] p {
        font-weight: 800 !important;
        color: #0d1117 !important;
    }
    div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
        background-color: rgba(0, 0, 0, 0.12);
    }

    /* ---- Estilos exclusivos de la pestaña "Presentación" ---- */
    .pres-board {
        background: #0b3d2e;
        border: 14px solid #c9b896;
        border-radius: 6px;
        padding: 2.2rem 2.6rem;
        box-shadow: 0 10px 0 rgba(0,0,0,0.08);
    }
    .pres-board h3 {
        color: #e8e042 !important;
        font-weight: 800 !important;
        margin-top: 0.6rem;
        margin-bottom: 0.2rem;
        font-size: 1.25rem;
    }
    .pres-board ul {
        margin-top: 0.1rem;
        margin-bottom: 0.4rem;
        padding-left: 1.4rem;
    }
    .pres-board li {
        color: #f5f5f0 !important;
        font-size: 1.05rem;
        margin-bottom: 0.15rem;
    }
    .pres-shield-wrap {
        text-align: center;
        padding-top: 1.5rem;
    }
    .pres-shield-caption {
        text-align: center;
        font-weight: 800 !important;
        color: #0d1117 !important;
        margin-top: 0.4rem;
        font-size: 1.05rem;
    }
    .pres-shield-caption small {
        display: block;
        font-weight: 600 !important;
        color: #3a3a3a !important;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Proyecto final de Física Electrónica")
st.caption("Modelo de referencia: Transistor 2N3904 · Segunda aproximación (Vbe = 0.7 V)")

BETA_NOTE = (
    "**Nota Teórica (Transistor 2N3904):** La ganancia de corriente (β) no es estática; "
    "varía dinámicamente entre 100 (caso peor) y 300 (caso mejor) según la temperatura y la "
    "corriente de colector (Ic). Para los cálculos base de este laboratorio virtual, "
    "utilizaremos el valor estándar teórico de **β = 100**."
)

# ----------------------------------------------------------------------------
# DIAGRAMAS SVG (estructura inspirada en las figuras del material académico)
# ----------------------------------------------------------------------------

def svg_base_fija(vcc=None, rb=None, rc=None):
    vcc_txt = f"{vcc:.1f} V" if vcc is not None else "Vcc"
    rb_txt = f"{rb/1000:.0f} kΩ" if rb is not None else "Rb"
    rc_txt = f"{rc/1000:.2f} kΩ" if rc is not None else "Rc"
    return f"""
    <svg viewBox="0 0 340 230" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
      <style>
        .wire{{stroke:#000000;stroke-width:3;fill:none;}}
        .lbl{{fill:#000000;font-size:12px;font-family:Arial, sans-serif;font-weight:700;}}
        .val{{fill:#1a7f37;font-size:12px;font-family:Arial, sans-serif;font-weight:700;}}
      </style>
      <!-- Vcc fuente izquierda -->
      <line x1="40" y1="40" x2="40" y2="170" class="wire"/>
      <line x1="28" y1="55" x2="52" y2="55" class="wire"/>
      <line x1="33" y1="63" x2="47" y2="63" class="wire"/>
      <text x="4" y="35" class="lbl">Vcc</text>
      <text x="4" y="100" class="val">{vcc_txt}</text>
      <!-- Rb resistencia base -->
      <line x1="40" y1="40" x2="120" y2="40" class="wire"/>
      <rect x="60" y="32" width="40" height="16" fill="none" stroke="#000000" stroke-width="3"/>
      <text x="58" y="25" class="lbl">Rb</text>
      <text x="55" y="64" class="val">{rb_txt}</text>
      <!-- linea base hacia transistor -->
      <line x1="120" y1="40" x2="160" y2="40" class="wire"/>
      <line x1="160" y1="40" x2="160" y2="90" class="wire"/>
      <!-- transistor circulo -->
      <circle cx="190" cy="100" r="32" fill="none" stroke="#000000" stroke-width="3"/>
      <line x1="160" y1="100" x2="180" y2="100" class="wire"/>
      <line x1="180" y1="85" x2="180" y2="115" class="wire" stroke-width="4"/>
      <line x1="180" y1="90" x2="205" y2="70" class="wire"/>
      <line x1="180" y1="110" x2="205" y2="130" class="wire"/>
      <text x="222" y="104" class="lbl">β = 100</text>
      <!-- Colector arriba hacia Rc y Vcc derecha -->
      <line x1="205" y1="70" x2="205" y2="40" class="wire"/>
      <line x1="205" y1="40" x2="270" y2="40" class="wire"/>
      <rect x="225" y="32" width="40" height="16" fill="none" stroke="#000000" stroke-width="3"/>
      <text x="225" y="25" class="lbl">Rc</text>
      <line x1="270" y1="40" x2="270" y2="170" class="wire"/>
      <line x1="258" y1="55" x2="282" y2="55" class="wire"/>
      <line x1="263" y1="63" x2="277" y2="63" class="wire"/>
      <text x="285" y="35" class="lbl">Vcc</text>
      <text x="220" y="64" class="val">{rc_txt}</text>
      <!-- Emisor a tierra comun -->
      <line x1="205" y1="130" x2="205" y2="170" class="wire"/>
      <line x1="40" y1="170" x2="270" y2="170" class="wire"/>
      <line x1="150" y1="170" x2="150" y2="185" class="wire"/>
      <line x1="133" y1="185" x2="167" y2="185" class="wire"/>
      <line x1="140" y1="192" x2="160" y2="192" class="wire"/>
      <line x1="147" y1="199" x2="153" y2="199" class="wire"/>
    </svg>
    """


def svg_emisor(vcc=None, vee=None, rb=None, rc=None, re=None):
    vcc_txt = f"{vcc:.1f} V" if vcc is not None else "+Vcc"
    vee_txt = f"{vee:.1f} V" if vee is not None else "-Vee"
    rb_txt = f"{rb/1000:.1f} kΩ" if rb is not None else "Rb"
    rc_txt = f"{rc/1000:.1f} kΩ" if rc is not None else "Rc"
    re_txt = f"{re/1000:.1f} kΩ" if re is not None else "Re"
    return f"""
    <svg viewBox="0 0 360 250" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
      <style>
        .wire{{stroke:#000000;stroke-width:3;fill:none;}}
        .lbl{{fill:#000000;font-size:12px;font-family:Arial, sans-serif;font-weight:700;}}
        .val{{fill:#1a7f37;font-size:12px;font-family:Arial, sans-serif;font-weight:700;}}
      </style>
      <!-- Rb desde nodo base a tierra/referencia -->
      <line x1="60" y1="40" x2="60" y2="80" class="wire"/>
      <rect x="52" y="80" width="16" height="35" fill="none" stroke="#000000" stroke-width="3"/>
      <text x="74" y="92" class="lbl">Rb</text>
      <text x="74" y="106" class="val">{rb_txt}</text>
      <line x1="60" y1="115" x2="60" y2="200" class="wire"/>
      <!-- linea base hacia transistor -->
      <line x1="60" y1="40" x2="160" y2="40" class="wire"/>
      <line x1="160" y1="40" x2="160" y2="90" class="wire"/>
      <!-- transistor -->
      <circle cx="190" cy="100" r="32" fill="none" stroke="#000000" stroke-width="3"/>
      <line x1="160" y1="100" x2="180" y2="100" class="wire"/>
      <line x1="180" y1="85" x2="180" y2="115" class="wire" stroke-width="4"/>
      <line x1="180" y1="90" x2="205" y2="70" class="wire"/>
      <line x1="180" y1="110" x2="205" y2="130" class="wire"/>
      <text x="222" y="104" class="lbl">β = 100</text>
      <!-- Colector arriba hacia Rc y Vcc -->
      <line x1="205" y1="70" x2="205" y2="40" class="wire"/>
      <line x1="205" y1="40" x2="280" y2="40" class="wire"/>
      <rect x="235" y="32" width="40" height="16" fill="none" stroke="#000000" stroke-width="3"/>
      <text x="235" y="25" class="lbl">Rc</text>
      <text x="230" y="64" class="val">{rc_txt}</text>
      <line x1="280" y1="40" x2="280" y2="100" class="wire"/>
      <line x1="268" y1="55" x2="292" y2="55" class="wire"/>
      <line x1="273" y1="63" x2="287" y2="63" class="wire"/>
      <text x="296" y="35" class="lbl">+Vcc</text>
      <text x="296" y="64" class="val">{vcc_txt}</text>
      <!-- Emisor abajo hacia Re y Vee -->
      <line x1="205" y1="130" x2="205" y2="200" class="wire"/>
      <line x1="205" y1="200" x2="280" y2="200" class="wire"/>
      <rect x="235" y="192" width="40" height="16" fill="none" stroke="#000000" stroke-width="3"/>
      <text x="235" y="186" class="lbl">Re</text>
      <text x="230" y="224" class="val">{re_txt}</text>
      <line x1="280" y1="200" x2="280" y2="140" class="wire"/>
      <line x1="268" y1="155" x2="292" y2="155" class="wire"/>
      <line x1="273" y1="163" x2="287" y2="163" class="wire"/>
      <text x="296" y="160" class="lbl">-Vee</text>
      <text x="296" y="178" class="val">{vee_txt}</text>
      <!-- Rb a Vee tambien -->
      <line x1="60" y1="200" x2="205" y2="200" class="wire"/>
    </svg>
    """


def svg_divisor(vcc=None, r1=None, r2=None, rc=None, re=None):
    vcc_txt = f"{vcc:.1f} V" if vcc is not None else "Vcc"
    r1_txt = f"{r1/1000:.1f} kΩ" if r1 is not None else "R1"
    r2_txt = f"{r2/1000:.1f} kΩ" if r2 is not None else "R2"
    rc_txt = f"{rc/1000:.2f} kΩ" if rc is not None else "Rc"
    re_txt = f"{re:.0f} Ω" if re is not None else "Re"
    return f"""
    <svg viewBox="0 0 360 270" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
      <style>
        .wire{{stroke:#000000;stroke-width:3;fill:none;}}
        .lbl{{fill:#000000;font-size:12px;font-family:Arial, sans-serif;font-weight:700;}}
        .val{{fill:#1a7f37;font-size:12px;font-family:Arial, sans-serif;font-weight:700;}}
      </style>
      <!-- riel Vcc superior -->
      <line x1="60" y1="30" x2="260" y2="30" class="wire"/>
      <circle cx="60" cy="30" r="3" fill="#000000"/>
      <text x="100" y="20" class="lbl">Vcc</text>
      <text x="155" y="20" class="val">{vcc_txt}</text>
      <!-- R1 -->
      <line x1="60" y1="30" x2="60" y2="60" class="wire"/>
      <rect x="52" y="60" width="16" height="35" fill="none" stroke="#000000" stroke-width="3"/>
      <text x="74" y="72" class="lbl">R1</text>
      <text x="74" y="86" class="val">{r1_txt}</text>
      <line x1="60" y1="95" x2="60" y2="130" class="wire"/>
      <!-- base hacia transistor -->
      <line x1="60" y1="130" x2="160" y2="130" class="wire"/>
      <line x1="160" y1="130" x2="160" y2="135" class="wire"/>
      <!-- transistor -->
      <circle cx="190" cy="140" r="32" fill="none" stroke="#000000" stroke-width="3"/>
      <line x1="160" y1="140" x2="180" y2="140" class="wire"/>
      <line x1="180" y1="125" x2="180" y2="155" class="wire" stroke-width="4"/>
      <line x1="180" y1="130" x2="205" y2="110" class="wire"/>
      <line x1="180" y1="150" x2="205" y2="170" class="wire"/>
      <text x="222" y="144" class="lbl">β = 100</text>
      <!-- R2 desde nodo base a tierra -->
      <line x1="60" y1="130" x2="60" y2="160" class="wire"/>
      <rect x="52" y="160" width="16" height="35" fill="none" stroke="#000000" stroke-width="3"/>
      <text x="74" y="172" class="lbl">R2</text>
      <text x="74" y="186" class="val">{r2_txt}</text>
      <line x1="60" y1="195" x2="60" y2="230" class="wire"/>
      <!-- Rc -->
      <line x1="205" y1="110" x2="205" y2="30" class="wire"/>
      <line x1="205" y1="30" x2="260" y2="30" class="wire"/>
      <rect x="222" y="60" width="16" height="35" fill="none" stroke="#000000" stroke-width="3"/>
      <text x="244" y="72" class="lbl">Rc</text>
      <text x="244" y="86" class="val">{rc_txt}</text>
      <line x1="230" y1="30" x2="230" y2="60" class="wire"/>
      <line x1="230" y1="95" x2="230" y2="110" class="wire"/>
      <line x1="205" y1="110" x2="230" y2="110" class="wire"/>
      <!-- Re hacia tierra -->
      <line x1="205" y1="170" x2="205" y2="195" class="wire"/>
      <rect x="197" y="195" width="16" height="35" fill="none" stroke="#000000" stroke-width="3"/>
      <text x="219" y="207" class="lbl">Re</text>
      <text x="219" y="221" class="val">{re_txt}</text>
      <line x1="205" y1="230" x2="205" y2="230" class="wire"/>
      <!-- tierra comun -->
      <line x1="60" y1="230" x2="205" y2="230" class="wire"/>
      <line x1="120" y1="230" x2="120" y2="240" class="wire"/>
      <line x1="106" y1="240" x2="134" y2="240" class="wire"/>
      <line x1="111" y1="247" x2="129" y2="247" class="wire"/>
      <line x1="116" y1="254" x2="124" y2="254" class="wire"/>
    </svg>
    """


def svg_unmsm_shield():
    """Escudo simplificado tipo San Marcos: óvalo dorado, banda azul, columnas y león."""
    return """
    <svg viewBox="0 0 220 260" xmlns="http://www.w3.org/2000/svg" style="width:170px;height:auto;">
      <defs>
        <radialGradient id="goldGrad" cx="50%" cy="35%" r="75%">
          <stop offset="0%" stop-color="#ffe27a"/>
          <stop offset="55%" stop-color="#e8b923"/>
          <stop offset="100%" stop-color="#b8860b"/>
        </radialGradient>
      </defs>
      <!-- corona / angel simplificado -->
      <circle cx="110" cy="34" r="20" fill="#f3d27a" stroke="#7a5a10" stroke-width="2"/>
      <path d="M70 40 Q110 10 150 40" fill="none" stroke="#b8860b" stroke-width="4"/>
      <!-- óvalo dorado principal -->
      <ellipse cx="110" cy="148" rx="92" ry="104" fill="url(#goldGrad)" stroke="#5c4209" stroke-width="5"/>
      <ellipse cx="110" cy="148" rx="78" ry="90" fill="#ffffff" stroke="#b8860b" stroke-width="3"/>
      <!-- banda celeste superior con estrellas -->
      <path d="M40 95 Q110 70 180 95 L180 120 Q110 98 40 120 Z" fill="#7fb7e8" stroke="#1f6feb" stroke-width="2"/>
      <circle cx="80" cy="100" r="3" fill="#ffffff"/>
      <circle cx="110" cy="92" r="3" fill="#ffffff"/>
      <circle cx="140" cy="100" r="3" fill="#ffffff"/>
      <!-- columnas plateadas -->
      <rect x="78" y="118" width="10" height="80" fill="#c9d3dc" stroke="#5c6b78" stroke-width="2"/>
      <rect x="132" y="118" width="10" height="80" fill="#c9d3dc" stroke="#5c6b78" stroke-width="2"/>
      <!-- mar azul -->
      <path d="M55 195 Q110 215 165 195 L165 215 Q110 232 55 215 Z" fill="#1f6feb" stroke="#123a86" stroke-width="2"/>
      <!-- leon dorado central -->
      <ellipse cx="110" cy="165" rx="20" ry="14" fill="#caa43d" stroke="#5c4209" stroke-width="2"/>
      <circle cx="110" cy="150" r="9" fill="#caa43d" stroke="#5c4209" stroke-width="2"/>
      <!-- lima (fruta) abajo -->
      <circle cx="110" cy="218" r="9" fill="#2ea043" stroke="#0f3320" stroke-width="2"/>
      <!-- texto SM -->
      <text x="110" y="78" text-anchor="middle" font-family="Georgia, serif" font-weight="700" font-size="13" fill="#5c4209">S.M.</text>
    </svg>
    """


# ----------------------------------------------------------------------------
# FUNCIONES DE CÁLCULO
# ----------------------------------------------------------------------------

def calc_base_fija(vcc, rb, rc):
    ib = (vcc - VBE) / rb
    ib = max(ib, 0)
    ic_ideal = BETA * ib
    ic_sat = vcc / rc
    if ib <= 0:
        return dict(ib=0, ic=0, vce=vcc, ic_sat=ic_sat, estado="corte")
    if ic_ideal >= ic_sat:
        return dict(ib=ib, ic=ic_sat, vce=VCE_SAT, ic_sat=ic_sat, estado="saturacion")
    vce = vcc - ic_ideal * rc
    return dict(ib=ib, ic=ic_ideal, vce=vce, ic_sat=ic_sat, estado="activa")


def calc_emisor(vcc, vee, rb, rc, re):
    ie = (vee - VBE) / (re + rb / BETA)
    ie = max(ie, 0)
    ic_ideal = ie  # Ic ≈ Ie
    ic_sat = (vcc + vee) / (rc + re)
    if ie <= 0:
        return dict(ib=ie / BETA, ic=0, vce=vcc + vee, ic_sat=ic_sat, estado="corte")
    if ic_ideal >= ic_sat:
        return dict(ib=ic_sat / BETA, ic=ic_sat, vce=VCE_SAT, ic_sat=ic_sat, estado="saturacion")
    vce = vcc + vee - ic_ideal * (rc + re)
    return dict(ib=ic_ideal / BETA, ic=ic_ideal, vce=vce, ic_sat=ic_sat, estado="activa")


def calc_divisor(vcc, r1, r2, rc, re):
    vth = vcc * (r2 / (r1 + r2))
    rth = (r1 * r2) / (r1 + r2)
    ib = (vth - VBE) / (rth + (BETA + 1) * re)
    ib = max(ib, 0)
    ic_ideal = BETA * ib
    ic_sat = vcc / (rc + re)
    if ib <= 0:
        return dict(ib=0, ic=0, vce=vcc, ic_sat=ic_sat, estado="corte", vth=vth, rth=rth)
    if ic_ideal >= ic_sat:
        return dict(ib=ib, ic=ic_sat, vce=VCE_SAT, ic_sat=ic_sat, estado="saturacion", vth=vth, rth=rth)
    vce = vcc - ic_ideal * (rc + re)
    return dict(ib=ib, ic=ic_ideal, vce=vce, ic_sat=ic_sat, estado="activa", vth=vth, rth=rth)


# ----------------------------------------------------------------------------
# COMPONENTES DE INTERFAZ COMPARTIDOS
# ----------------------------------------------------------------------------

def render_alert(estado, vcc_total):
    if estado == "corte":
        st.markdown(
            f"""<div class="alert-cutoff">⛔ <b>Falla: Transistor en CORTE</b><br>
            Ic = 0 A, Vce = Vcc ({vcc_total:.2f} V). El voltaje de la base es insuficiente
            para superar la barrera de 0.7 V del Silicio, o una resistencia seleccionada
            se encuentra abierta.</div>""",
            unsafe_allow_html=True,
        )
    elif estado == "saturacion":
        st.markdown(
            """<div class="alert-sat">🟠 <b>Falla: Transistor en SATURACIÓN</b><br>
            Vce ≈ 0.2 V. El circuito opera como un interruptor cerrado (cortocircuito
            aparente). Modifique las resistencias para retornar a la región activa.</div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """<div class="alert-ok">✅ <b>Circuito Operando Correctamente</b><br>
            Región Activa (Zona de Amplificación Lineal).</div>""",
            unsafe_allow_html=True,
        )


def render_load_line(vce, ic, ib, vce_max, ic_sat):
    """
    Dibuja la familia de Curvas Características del Colector (Ic vs Vce para
    distintos valores de Ib), la Recta de Carga DC y el Punto Q de operación.
    """
    fig = go.Figure()

    # --- Familia de curvas características (para varios múltiplos de Ib) ---
    # Cada curva: en la zona de saturación sube abruptamente hasta Ic = beta*Ib,
    # luego se mantiene "plana" (modelo ideal) en la región activa.
    ib_actual = max(ib, vce_max / 1e9)  # evita división por cero si ib=0
    ib_multipliers = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
    tau = vce_max * 0.06  # controla qué tan "abierto" es el codo de la curva

    n_points = 60
    for m in ib_multipliers:
        ib_curve = ib_actual * m
        ic_flat = min(BETA * ib_curve, ic_sat)
        is_active_curve = abs(m - 1.0) < 1e-6
        x_vals = [vce_max * i / (n_points - 1) for i in range(n_points)]
        y_vals = [ic_flat * 1000 * (1 - 2.718281828 ** (-x / tau)) for x in x_vals]
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode="lines",
            name=f"Ib = {ib_curve*1e6:.1f} µA" if is_active_curve else None,
            line=dict(
                color="#2ea043" if is_active_curve else "#b7c4d6",
                width=3 if is_active_curve else 1.5,
                dash="solid" if is_active_curve else "dot",
                shape="spline",
            ),
            showlegend=is_active_curve,
            hoverinfo="skip" if not is_active_curve else "all",
        ))

    # --- Recta de Carga DC ---
    fig.add_trace(go.Scatter(
        x=[0, vce_max], y=[ic_sat * 1000, 0],
        mode="lines", name="Recta de Carga (DC)",
        line=dict(color="#1f6feb", width=3),
    ))

    # --- Punto Q ---
    fig.add_trace(go.Scatter(
        x=[vce], y=[ic * 1000],
        mode="markers+text", name="Punto Q",
        marker=dict(color="#d62828", size=14, line=dict(width=2, color="#000000")),
        text=[f"Q ({vce:.2f} V, {ic*1000:.3f} mA)"],
        textposition="top center",
        textfont=dict(color="#000000"),
    ))

    fig.update_layout(
        template="plotly_white",
        title=dict(text="Curvas Características del Colector", font=dict(size=14, color="#0d1117")),
        xaxis_title="Vce (V)",
        yaxis_title="Ic (mA)",
        xaxis=dict(range=[0, vce_max * 1.05], gridcolor="#d0d7de", color="#0d1117"),
        yaxis=dict(range=[0, ic_sat * 1000 * 1.15], gridcolor="#d0d7de", color="#0d1117"),
        plot_bgcolor="#ffffff",
        paper_bgcolor="#ffffff",
        font=dict(color="#0d1117"),
        margin=dict(l=10, r=10, t=40, b=10),
        height=420,
        legend=dict(orientation="h", y=-0.2, font=dict(color="#0d1117")),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_results(res, vce_max):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ib", f"{res['ib']*1e6:.2f} µA")
    c2.metric("Ic", f"{res['ic']*1000:.3f} mA")
    c3.metric("Vce", f"{res['vce']:.2f} V")
    c4.metric("Ic(sat)", f"{res['ic_sat']*1000:.3f} mA")


# ----------------------------------------------------------------------------
# LAYOUT PRINCIPAL: 4 PESTAÑAS (3 de polarización + Presentación)
# ----------------------------------------------------------------------------

tab_a, tab_b, tab_c, tab_pres = st.tabs([
    "Polarización de Base (Fija)",
    "Polarización de Emisor",
    "Divisor de Tensión",
    "Presentación",
])

# ============================ OPCIÓN A ======================================
with tab_a:
    st.subheader("Polarización de Base (Fija)")
    st.write(
        "Requiere los valores de la fuente de alimentación principal (Vcc), la resistencia "
        "conectada a la base (Rb) y la resistencia del colector (Rc)."
    )
    st.caption("📘 Referencia: *Semana 7 - TRANSISTORES*, Página 24 (Figura 13).")

    col_form, col_gap, col_diag = st.columns([1, 0.18, 1])
    with col_form:
        vcc_a = st.slider("Vcc (V)", 0.0, 30.0, 10.0, 0.1, key="vcc_a")
        rb_a = st.number_input("Rb (Ω)", min_value=1.0, value=1_000_000.0, step=1000.0, key="rb_a")
        rc_a = st.number_input("Rc (Ω)", min_value=1.0, value=1000.0, step=10.0, key="rc_a")

        st.markdown(
            f'<div class="circuit-frame">{svg_base_fija(vcc_a, rb_a, rc_a)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="beta-note">{BETA_NOTE}</div>', unsafe_allow_html=True)

    res_a = calc_base_fija(vcc_a, rb_a, rc_a)

    with col_diag:
        render_results(res_a, vcc_a)
        render_load_line(res_a["vce"], res_a["ic"], res_a["ib"], vcc_a, res_a["ic_sat"])
        render_alert(res_a["estado"], vcc_a)

# ============================ OPCIÓN B ======================================
with tab_b:
    st.subheader("Polarización de Emisor")
    st.write(
        "Requiere los valores de dos fuentes de alimentación (Vcc positivo y Vee negativo), "
        "la resistencia de base (Rb), la resistencia de colector (Rc) y la resistencia de "
        "emisor (Re)."
    )
    st.caption("📘 Referencia: *Semana 8 - Fundamentos de los transistores*, Página 27 (Figura 10).")

    col_form, col_gap, col_diag = st.columns([1, 0.18, 1])
    with col_form:
        vcc_b = st.slider("Vcc (V)", 0.0, 30.0, 20.0, 0.1, key="vcc_b")
        vee_b = st.slider("Vee (V)", 0.0, 30.0, 20.0, 0.1, key="vee_b")
        rb_b = st.number_input("Rb (Ω)", min_value=1.0, value=10_000.0, step=100.0, key="rb_b")
        rc_b = st.number_input("Rc (Ω)", min_value=1.0, value=5_000.0, step=100.0, key="rc_b")
        re_b = st.number_input("Re (Ω)", min_value=1.0, value=10_000.0, step=100.0, key="re_b")

        st.markdown(
            f'<div class="circuit-frame">{svg_emisor(vcc_b, vee_b, rb_b, rc_b, re_b)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="beta-note">{BETA_NOTE}</div>', unsafe_allow_html=True)

    res_b = calc_emisor(vcc_b, vee_b, rb_b, rc_b, re_b)

    with col_diag:
        render_results(res_b, vcc_b + vee_b)
        render_load_line(res_b["vce"], res_b["ic"], res_b["ib"], vcc_b + vee_b, res_b["ic_sat"])
        render_alert(res_b["estado"], vcc_b + vee_b)

# ============================ OPCIÓN C ======================================
with tab_c:
    st.subheader("Polarización por Divisor de Tensión")
    st.write(
        "Requiere el voltaje de la fuente común (Vcc), las dos resistencias del divisor en "
        "la base (R1 y R2), la resistencia de colector (Rc) y la resistencia de emisor (Re)."
    )
    st.caption("📘 Referencia: *Semana 10 Adicional*, Páginas 1 y 2 (Figuras 1 y 2a).")

    col_form, col_gap, col_diag = st.columns([1, 0.18, 1])
    with col_form:
        vcc_c = st.slider("Vcc (V)", 0.0, 30.0, 10.0, 0.1, key="vcc_c")
        r1_c = st.number_input("R1 (Ω)", min_value=1.0, value=10_000.0, step=100.0, key="r1_c")
        r2_c = st.number_input("R2 (Ω)", min_value=1.0, value=5_000.0, step=100.0, key="r2_c")
        rc_c = st.number_input("Rc (Ω)", min_value=1.0, value=1_000.0, step=10.0, key="rc_c")
        re_c = st.number_input("Re (Ω)", min_value=1.0, value=500.0, step=10.0, key="re_c")

        st.markdown(
            f'<div class="circuit-frame">{svg_divisor(vcc_c, r1_c, r2_c, rc_c, re_c)}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f'<div class="beta-note">{BETA_NOTE}</div>', unsafe_allow_html=True)

    res_c = calc_divisor(vcc_c, r1_c, r2_c, rc_c, re_c)

    with col_diag:
        render_results(res_c, vcc_c)
        st.caption(f"Vth = {res_c['vth']:.3f} V  |  Rth = {res_c['rth']:.1f} Ω (método de Thévenin)")
        render_load_line(res_c["vce"], res_c["ic"], res_c["ib"], vcc_c, res_c["ic_sat"])
        render_alert(res_c["estado"], vcc_c)

# ============================ PRESENTACIÓN ==================================
with tab_pres:
    col_board, col_shield = st.columns([1.6, 1])

    with col_board:
        st.markdown(
            """
            <div class="pres-board">
                <h3>Facultad:</h3>
                <ul><li>Ingeniería de Sistemas e Informática</li></ul>
                <h3>Profesor:</h3>
                <ul><li>Galarreta Díaz, Jose Hermenegildo</li></ul>
                <h3>Asignatura:</h3>
                <ul><li>Física Electrónica</li></ul>
                <h3>Integrantes:</h3>
                <ul>
                    <li>Machaca Ponce, Sebastián Emanuel</li>
                    <li>Huallpacuna Gutierrez, Jean Piero</li>
                    <li>Tafur Coveñas, Angel Daniel</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_shield:
        st.markdown(
            f"""
            <div class="pres-shield-wrap">{svg_unmsm_shield()}</div>
            <div class="pres-shield-caption">
                UNIVERSIDAD NACIONAL MAYOR DE<br>SAN MARCOS
                <small>Universidad del Perú, Decana de América</small>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()
st.caption(
    "Laboratorio Virtual BJT 2N3904 · β = 100 fijo · Vbe = 0.7 V (segunda aproximación) · "
    "Desarrollado en Streamlit + Plotly"
)
