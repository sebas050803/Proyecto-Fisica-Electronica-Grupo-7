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
    .stApp { background-color: #0e1117; }
    .circuit-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1rem;
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
        background-color: #1c2333; border-left: 4px solid #58a6ff;
        border-radius: 8px; padding: .8rem 1rem; font-size: 0.85rem; color: #c9d1d9;
        margin-top: .5rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔌 Laboratorio Virtual de Transistores BJT NPN de Silicio")
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

def svg_base_fija():
    return """
    <svg viewBox="0 0 320 220" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
      <style>
        .wire{stroke:#c9d1d9;stroke-width:2;fill:none;}
        .lbl{fill:#8b949e;font-size:11px;font-family:monospace;}
        .val{fill:#58a6ff;font-size:11px;font-family:monospace;font-weight:bold;}
      </style>
      <!-- Vcc fuente izquierda -->
      <line x1="40" y1="40" x2="40" y2="170" class="wire"/>
      <line x1="30" y1="55" x2="50" y2="55" class="wire"/>
      <line x1="34" y1="62" x2="46" y2="62" class="wire"/>
      <text x="10" y="100" class="lbl">Vcc</text>
      <!-- Rb resistencia base -->
      <line x1="40" y1="40" x2="120" y2="40" class="wire"/>
      <rect x="60" y="32" width="40" height="16" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <text x="55" y="25" class="lbl">Rb</text>
      <!-- linea base hacia transistor -->
      <line x1="120" y1="40" x2="160" y2="40" class="wire"/>
      <line x1="160" y1="40" x2="160" y2="90" class="wire"/>
      <!-- transistor circulo -->
      <circle cx="190" cy="100" r="32" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <line x1="160" y1="100" x2="180" y2="100" class="wire"/>
      <line x1="180" y1="85" x2="180" y2="115" class="wire" stroke-width="3"/>
      <line x1="180" y1="90" x2="205" y2="70" class="wire"/>
      <line x1="180" y1="110" x2="205" y2="130" class="wire"/>
      <text x="200" y="100" class="lbl">β=100</text>
      <!-- Colector arriba hacia Rc y Vcc derecha -->
      <line x1="205" y1="70" x2="205" y2="40" class="wire"/>
      <line x1="205" y1="40" x2="270" y2="40" class="wire"/>
      <rect x="225" y="32" width="40" height="16" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <text x="225" y="25" class="lbl">Rc</text>
      <line x1="270" y1="40" x2="270" y2="170" class="wire"/>
      <line x1="260" y1="55" x2="280" y2="55" class="wire"/>
      <line x1="264" y1="62" x2="276" y2="62" class="wire"/>
      <!-- Emisor a tierra comun -->
      <line x1="205" y1="130" x2="205" y2="170" class="wire"/>
      <line x1="40" y1="170" x2="270" y2="170" class="wire"/>
      <line x1="150" y1="170" x2="150" y2="185" class="wire"/>
      <line x1="135" y1="185" x2="165" y2="185" class="wire"/>
      <line x1="141" y1="192" x2="159" y2="192" class="wire"/>
      <line x1="147" y1="199" x2="153" y2="199" class="wire"/>
    </svg>
    """


def svg_emisor():
    return """
    <svg viewBox="0 0 340 240" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
      <style>
        .wire{stroke:#c9d1d9;stroke-width:2;fill:none;}
        .lbl{fill:#8b949e;font-size:11px;font-family:monospace;}
      </style>
      <!-- Rb desde nodo base a tierra/referencia -->
      <line x1="60" y1="40" x2="60" y2="80" class="wire"/>
      <rect x="52" y="80" width="16" height="35" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <text x="72" y="100" class="lbl">Rb</text>
      <line x1="60" y1="115" x2="60" y2="200" class="wire"/>
      <!-- linea base hacia transistor -->
      <line x1="60" y1="40" x2="160" y2="40" class="wire"/>
      <line x1="160" y1="40" x2="160" y2="90" class="wire"/>
      <!-- transistor -->
      <circle cx="190" cy="100" r="32" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <line x1="160" y1="100" x2="180" y2="100" class="wire"/>
      <line x1="180" y1="85" x2="180" y2="115" class="wire" stroke-width="3"/>
      <line x1="180" y1="90" x2="205" y2="70" class="wire"/>
      <line x1="180" y1="110" x2="205" y2="130" class="wire"/>
      <!-- Colector arriba hacia Rc y Vcc -->
      <line x1="205" y1="70" x2="205" y2="40" class="wire"/>
      <line x1="205" y1="40" x2="280" y2="40" class="wire"/>
      <rect x="235" y="32" width="40" height="16" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <text x="235" y="25" class="lbl">Rc</text>
      <line x1="280" y1="40" x2="280" y2="100" class="wire"/>
      <line x1="270" y1="55" x2="290" y2="55" class="wire"/>
      <line x1="274" y1="62" x2="286" y2="62" class="wire"/>
      <text x="295" y="60" class="lbl">+Vcc</text>
      <!-- Emisor abajo hacia Re y Vee -->
      <line x1="205" y1="130" x2="205" y2="200" class="wire"/>
      <line x1="205" y1="200" x2="280" y2="200" class="wire"/>
      <rect x="235" y="192" width="40" height="16" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <text x="235" y="186" class="lbl">Re</text>
      <line x1="280" y1="200" x2="280" y2="140" class="wire"/>
      <line x1="270" y1="155" x2="290" y2="155" class="wire"/>
      <line x1="274" y1="162" x2="286" y2="162" class="wire"/>
      <text x="295" y="160" class="lbl">-Vee</text>
      <!-- Rb a Vee tambien -->
      <line x1="60" y1="200" x2="205" y2="200" class="wire"/>
    </svg>
    """


def svg_divisor():
    return """
    <svg viewBox="0 0 340 260" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;">
      <style>
        .wire{stroke:#c9d1d9;stroke-width:2;fill:none;}
        .lbl{fill:#8b949e;font-size:11px;font-family:monospace;}
      </style>
      <!-- riel Vcc superior -->
      <line x1="60" y1="30" x2="260" y2="30" class="wire"/>
      <circle cx="60" cy="30" r="3" fill="#58a6ff"/>
      <text x="100" y="20" class="lbl">Vcc</text>
      <!-- R1 -->
      <line x1="60" y1="30" x2="60" y2="60" class="wire"/>
      <rect x="52" y="60" width="16" height="35" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <text x="72" y="80" class="lbl">R1</text>
      <line x1="60" y1="95" x2="60" y2="130" class="wire"/>
      <!-- base hacia transistor -->
      <line x1="60" y1="130" x2="160" y2="130" class="wire"/>
      <line x1="160" y1="130" x2="160" y2="135" class="wire"/>
      <!-- transistor -->
      <circle cx="190" cy="140" r="32" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <line x1="160" y1="140" x2="180" y2="140" class="wire"/>
      <line x1="180" y1="125" x2="180" y2="155" class="wire" stroke-width="3"/>
      <line x1="180" y1="130" x2="205" y2="110" class="wire"/>
      <line x1="180" y1="150" x2="205" y2="170" class="wire"/>
      <!-- R2 desde nodo base a tierra -->
      <line x1="60" y1="130" x2="60" y2="160" class="wire"/>
      <rect x="52" y="160" width="16" height="35" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <text x="72" y="180" class="lbl">R2</text>
      <line x1="60" y1="195" x2="60" y2="230" class="wire"/>
      <!-- Rc -->
      <line x1="205" y1="110" x2="205" y2="30" class="wire"/>
      <line x1="205" y1="30" x2="260" y2="30" class="wire"/>
      <rect x="222" y="60" width="16" height="35" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <text x="240" y="80" class="lbl">Rc</text>
      <line x1="230" y1="30" x2="230" y2="60" class="wire"/>
      <line x1="230" y1="95" x2="230" y2="110" class="wire"/>
      <line x1="205" y1="110" x2="230" y2="110" class="wire"/>
      <!-- Re hacia tierra -->
      <line x1="205" y1="170" x2="205" y2="195" class="wire"/>
      <rect x="197" y="195" width="16" height="35" fill="none" stroke="#c9d1d9" stroke-width="2"/>
      <text x="217" y="215" class="lbl">Re</text>
      <line x1="205" y1="230" x2="205" y2="230" class="wire"/>
      <!-- tierra comun -->
      <line x1="60" y1="230" x2="205" y2="230" class="wire"/>
      <line x1="120" y1="230" x2="120" y2="240" class="wire"/>
      <line x1="108" y1="240" x2="132" y2="240" class="wire"/>
      <line x1="113" y1="246" x2="127" y2="246" class="wire"/>
      <line x1="118" y1="252" x2="122" y2="252" class="wire"/>
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
    vce_knee = vce_max * 0.04  # rodilla de saturación aproximada

    for m in ib_multipliers:
        ib_curve = ib_actual * m
        ic_flat = min(BETA * ib_curve, ic_sat)
        is_active_curve = abs(m - 1.0) < 1e-6
        x_vals = [0, vce_knee, vce_max]
        y_vals = [0, ic_flat * 1000, ic_flat * 1000]
        fig.add_trace(go.Scatter(
            x=x_vals, y=y_vals,
            mode="lines",
            name=f"Ib = {ib_curve*1e6:.1f} µA" if is_active_curve else None,
            line=dict(
                color="#3fb950" if is_active_curve else "#2c3a4a",
                width=3 if is_active_curve else 1.5,
                dash="solid" if is_active_curve else "dot",
            ),
            showlegend=is_active_curve,
            hoverinfo="skip" if not is_active_curve else "all",
        ))

    # --- Recta de Carga DC ---
    fig.add_trace(go.Scatter(
        x=[0, vce_max], y=[ic_sat * 1000, 0],
        mode="lines", name="Recta de Carga (DC)",
        line=dict(color="#58a6ff", width=3),
    ))

    # --- Punto Q ---
    fig.add_trace(go.Scatter(
        x=[vce], y=[ic * 1000],
        mode="markers+text", name="Punto Q",
        marker=dict(color="#ff4d4d", size=14, line=dict(width=2, color="white")),
        text=[f"Q ({vce:.2f} V, {ic*1000:.3f} mA)"],
        textposition="top center",
        textfont=dict(color="#ff9a96"),
    ))

    fig.update_layout(
        template="plotly_dark",
        title=dict(text="Curvas Características del Colector", font=dict(size=14, color="#c9d1d9")),
        xaxis_title="Vce (V)",
        yaxis_title="Ic (mA)",
        xaxis=dict(range=[0, vce_max * 1.05], gridcolor="#30363d"),
        yaxis=dict(range=[0, ic_sat * 1000 * 1.15], gridcolor="#30363d"),
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        margin=dict(l=10, r=10, t=40, b=10),
        height=420,
        legend=dict(orientation="h", y=-0.2),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_results(res, vce_max):
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Ib", f"{res['ib']*1e6:.2f} µA")
    c2.metric("Ic", f"{res['ic']*1000:.3f} mA")
    c3.metric("Vce", f"{res['vce']:.2f} V")
    c4.metric("Ic(sat)", f"{res['ic_sat']*1000:.3f} mA")


# ----------------------------------------------------------------------------
# LAYOUT PRINCIPAL: 3 PESTAÑAS
# ----------------------------------------------------------------------------

tab_a, tab_b, tab_c = st.tabs([
    "🅰️ Polarización de Base (Fija)",
    "🅱️ Polarización de Emisor",
    "🅲️ Divisor de Tensión",
])

# ============================ OPCIÓN A ======================================
with tab_a:
    st.subheader("Polarización de Base (Fija)")
    st.write(
        "Requiere los valores de la fuente de alimentación principal (Vcc), la resistencia "
        "conectada a la base (Rb) y la resistencia del colector (Rc)."
    )
    st.caption("📘 Referencia: *Semana 7 - TRANSISTORES*, Página 24 (Figura 13).")

    col_form, col_diag = st.columns([1, 1])
    with col_form:
        st.markdown('<div class="circuit-card">', unsafe_allow_html=True)
        st.markdown(svg_base_fija(), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="beta-note">{BETA_NOTE}</div>', unsafe_allow_html=True)

        vcc_a = st.slider("Vcc (V)", 0.0, 30.0, 10.0, 0.1, key="vcc_a")
        rb_a = st.number_input("Rb (Ω)", min_value=1.0, value=1_000_000.0, step=1000.0, key="rb_a")
        rc_a = st.number_input("Rc (Ω)", min_value=1.0, value=1000.0, step=10.0, key="rc_a")

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

    col_form, col_diag = st.columns([1, 1])
    with col_form:
        st.markdown('<div class="circuit-card">', unsafe_allow_html=True)
        st.markdown(svg_emisor(), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="beta-note">{BETA_NOTE}</div>', unsafe_allow_html=True)

        vcc_b = st.slider("Vcc (V)", 0.0, 30.0, 20.0, 0.1, key="vcc_b")
        vee_b = st.slider("Vee (V)", 0.0, 30.0, 20.0, 0.1, key="vee_b")
        rb_b = st.number_input("Rb (Ω)", min_value=1.0, value=10_000.0, step=100.0, key="rb_b")
        rc_b = st.number_input("Rc (Ω)", min_value=1.0, value=5_000.0, step=100.0, key="rc_b")
        re_b = st.number_input("Re (Ω)", min_value=1.0, value=10_000.0, step=100.0, key="re_b")

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

    col_form, col_diag = st.columns([1, 1])
    with col_form:
        st.markdown('<div class="circuit-card">', unsafe_allow_html=True)
        st.markdown(svg_divisor(), unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="beta-note">{BETA_NOTE}</div>', unsafe_allow_html=True)

        vcc_c = st.slider("Vcc (V)", 0.0, 30.0, 10.0, 0.1, key="vcc_c")
        r1_c = st.number_input("R1 (Ω)", min_value=1.0, value=10_000.0, step=100.0, key="r1_c")
        r2_c = st.number_input("R2 (Ω)", min_value=1.0, value=5_000.0, step=100.0, key="r2_c")
        rc_c = st.number_input("Rc (Ω)", min_value=1.0, value=1_000.0, step=10.0, key="rc_c")
        re_c = st.number_input("Re (Ω)", min_value=1.0, value=500.0, step=10.0, key="re_c")

    res_c = calc_divisor(vcc_c, r1_c, r2_c, rc_c, re_c)

    with col_diag:
        render_results(res_c, vcc_c)
        st.caption(f"Vth = {res_c['vth']:.3f} V  |  Rth = {res_c['rth']:.1f} Ω (método de Thévenin)")
        render_load_line(res_c["vce"], res_c["ic"], res_c["ib"], vcc_c, res_c["ic_sat"])
        render_alert(res_c["estado"], vcc_c)

st.divider()
st.caption(
    "Laboratorio Virtual BJT 2N3904 · β = 100 fijo · Vbe = 0.7 V (segunda aproximación) · "
    "Desarrollado en Streamlit + Plotly"
)
