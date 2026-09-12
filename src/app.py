import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================
# PAGE CONFIGURATION & CYBERPUNK SCADA STYLING
# ==========================================
st.set_page_config(
    page_title="NEXUS v5.0 | Industrial PID Digital Twin",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Inter:wght@400;600;700;800&display=swap');

    /* Global OLED */
    .stApp { background: #0A0A0A; }
    [data-testid="stAppViewContainer"] { background: #0A0A0A; }
    [data-testid="stSidebar"] { background: #0F0F12; border-right: 1px solid rgba(0,229,255,0.08); }
    [data-testid="stHeader"] { background: rgba(10,10,10,0.0); }

    /* Typography */
    h1, h2, h3 { font-family: 'Inter', sans-serif !important; letter-spacing: -0.03em; }
    p, label, span { font-family: 'Inter', sans-serif; }

    /* SCADA Card Wrapper — targets Streamlit bordered containers */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(20,20,22,0.85) !important;
        border: 1px solid rgba(0,229,255,0.14) !important;
        border-radius: 14px !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.45), 0 0 0 1px rgba(0,229,255,0.04) inset;
        padding: 2px 0 8px 0;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    [data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(0,229,255,0.26) !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.55), 0 0 18px rgba(0,229,255,0.08);
    }

    /* SCADA labels inside cards */
    .scada-label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 10px !important;
        letter-spacing: 0.14em !important;
        color: #00E5FF !important;
        font-weight: 600;
        margin: 6px 0 8px 0;
        display: flex;
        align-items: center;
        gap: 6px;
        opacity: 0.95;
    }
    .scada-label::before {
        content: "";
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background: #00E5FF;
        box-shadow: 0 0 8px rgba(0,229,255,0.9);
        display: inline-block;
    }
    .scada-hint {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #80868E;
        letter-spacing: 0.06em;
        margin: -6px 0 10px 0;
    }
    .scada-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        color: #00E5FF;
        text-align: right;
        margin-top: -4px;
        letter-spacing: 0.08em;
        opacity: 0.9;
    }
    .scada-value span {
        background: rgba(0,229,255,0.10);
        border: 1px solid rgba(0,229,255,0.18);
        padding: 2px 7px;
        border-radius: 999px;
        font-weight: 700;
    }

    /* Sidebar selectbox / inputs — sleek */
    [data-testid="stSidebar"] [data-baseweb="select"] > div,
    [data-testid="stSidebar"] [data-testid="stNumberInput"] input,
    [data-testid="stSidebar"] [data-testid="stTextInput"] input {
        background: #0A0A0A !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        border-radius: 10px !important;
        color: #E6E8EB !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div:focus-within,
    [data-testid="stSidebar"] [data-testid="stNumberInput"] input:focus {
        border-color: rgba(0,229,255,0.35) !important;
        box-shadow: 0 0 0 3px rgba(0,229,255,0.10) !important;
    }

    /* Sliders — neon track & thumb */
    [data-testid="stSlider"] { padding: 6px 2px 4px 2px; }
    [data-testid="stSlider"] label { 
        font-family: 'Inter', sans-serif !important;
        font-size: 12px !important;
        color: #C7CAD1 !important;
        font-weight: 500;
        letter-spacing: -0.01em;
    }
    [data-testid="stSlider"] div[data-baseweb="slider"] > div:first-child {
        background: rgba(255,255,255,0.08) !important;
        height: 4px !important;
        border-radius: 999px !important;
    }
    [data-testid="stSlider"] div[data-baseweb="slider"] div[style*="background"] {
        background: linear-gradient(90deg, #00E5FF 0%, #7C4DFF 100%) !important;
        height: 4px !important;
    }
    [data-testid="stSlider"] div[role="slider"] {
        background: #00E5FF !important;
        border: 2px solid #0A0A0A !important;
        box-shadow: 0 0 12px rgba(0,229,255,0.8), 0 2px 8px rgba(0,0,0,0.6) !important;
        width: 18px !important;
        height: 18px !important;
    }

    /* Segmented control row — pill buttons */
    [data-testid="stSidebar"] .stButton > button {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        font-weight: 600 !important;
        letter-spacing: 0.06em !important;
        border-radius: 999px !important;
        padding: 7px 10px !important;
        transition: all 0.15s ease !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
        background: rgba(255,255,255,0.04) !important;
        color: #9AA0A6 !important;
        backdrop-filter: blur(6px);
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        border-color: rgba(0,229,255,0.28) !important;
        color: #E6E8EB !important;
        background: rgba(0,229,255,0.08) !important;
        box-shadow: 0 0 14px rgba(0,229,255,0.12);
        transform: translateY(-1px);
    }
    [data-testid="stSidebar"] .stButton > button:active {
        transform: translateY(0px) scale(0.98);
    }
    /* Primary Apply Gains — cyan solid */
    [data-testid="stSidebar"] div[data-testid="stVerticalBlockBorderWrapper"] + div .stButton > button,
    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: #00E5FF !important;
        color: #001114 !important;
        border-color: transparent !important;
        box-shadow: 0 6px 20px rgba(0,229,255,0.30) !important;
        font-weight: 700 !important;
    }
    [data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
        background: #00D4EA !important;
        box-shadow: 0 8px 24px rgba(0,229,255,0.40) !important;
    }

    /* Main CTA Execute button — neon */
    [data-testid="stMain"] .stButton > button {
        background: #00E5FF !important;
        color: #001114 !important;
        border: none !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 12px 18px !important;
        box-shadow: 0 8px 30px rgba(0,229,255,0.35), inset 0 1px 0 rgba(255,255,255,0.6) !important;
    }
    [data-testid="stMain"] .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 12px 36px rgba(0,229,255,0.45) !important;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(20,20,20,0.9) !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 14px !important;
        padding: 14px 16px !important;
        backdrop-filter: blur(8px);
    }
    [data-testid="stMetricLabel"] { font-family: 'JetBrains Mono', monospace !important; font-size: 10px !important; letter-spacing: 0.10em !important; color: #80868E !important; }
    [data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace !important; color: #00E5FF !important; }

    /* Divider */
    hr { border-color: rgba(255,255,255,0.06) !important; margin: 14px 0 !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# CORE PID ENGINE (INDUSTRIAL-GRADE)
# ==========================================
class IndustrialPID:
    def __init__(self, Kp, Ki, Kd, output_limits=(-100, 100), anti_windup=True, alpha=0.1):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.min_out, self.max_out = output_limits
        self.anti_windup = anti_windup
        self.alpha = alpha  # Derivative filter coefficient
        self.reset()

    def reset(self):
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_derivative = 0.0
        self.prev_measurement = 0.0

    def compute(self, setpoint, measurement, dt):
        if dt <= 0:
            return 0.0

        error = setpoint - measurement

        # Proportional term
        P = self.Kp * error

        # Integral term with anti-windup
        self.integral += error * dt
        I = self.Ki * self.integral

        # Derivative term on measurement (prevents Derivative Kick)
        d_measurement = (measurement - self.prev_measurement) / dt
        derivative = (self.alpha * d_measurement) + (1 - self.alpha) * self.prev_derivative
        D = -self.Kd * derivative

        # Unclamped Output
        output_unclamped = P + I + D

        # Clamp Output (Actuator saturation)
        output = np.clip(output_unclamped, self.min_out, self.max_out)

        # Anti-windup clamping logic
        if self.anti_windup and (output != output_unclamped):
            if np.sign(error) == np.sign(output_unclamped):
                self.integral -= error * dt  # Prevent further accumulation
                I = self.Ki * self.integral
                output = np.clip(P + I + D, self.min_out, self.max_out)

        # Save states
        self.prev_error = error
        self.prev_derivative = derivative
        self.prev_measurement = measurement

        return float(output)


# ==========================================
# PHYSICAL PLANT MODELS (DIGITAL TWIN)
# ==========================================
class PhysicalPlant:
    def __init__(self, plant_type="Thermal"):
        self.plant_type = plant_type
        self.state = 0.0
        self.velocity = 0.0

    def reset(self, initial_value=0.0):
        self.state = initial_value
        self.velocity = 0.0

    def update(self, u, dt, disturbance=0.0):
        if self.plant_type == "Thermal System":
            # First-order process with thermal loss
            tau = 3.0  # Time constant
            K = 1.5  # Gain
            ambient_temp = 25.0
            dstate = (-(self.state - ambient_temp) + K * u + disturbance) / tau
            self.state += dstate * dt

        elif self.plant_type == "DC Motor Speed":
            # Second-order electromechanical system
            J = 0.01  # Inertia
            b = 0.1  # Friction
            K = 0.01  # Torque constant

            d2_state = (K * u - b * self.velocity + disturbance) / J
            self.velocity += d2_state * dt
            self.state += self.velocity * dt

        elif self.plant_type == "Liquid Tank Level":
            # Hydraulic gravity system
            area = 2.0
            valve_coeff = 0.5
            inflow = max(0, u * 0.1)
            outflow = valve_coeff * np.sqrt(max(0, self.state))
            dstate = (inflow - outflow + disturbance) / area
            self.state = max(0.0, self.state + dstate * dt)

        return self.state


# ==========================================
# SIDEBAR — CYBERPUNK SCADA CALIBRATION
# ==========================================
st.sidebar.title("🎛️ Control Panel")

# ── Industrial Target ──
with st.sidebar.container(border=True):
    st.markdown('<div class="scada-label">⬢ INDUSTRIAL TARGET</div>', unsafe_allow_html=True)
    plant_choice = st.selectbox(
        "Select Industrial Target",
        ["Thermal System", "DC Motor Speed", "Liquid Tank Level"],
        label_visibility="collapsed",
        key="plant_choice",
    )
    st.caption("Select plant dynamics for Digital Twin")

# ── Session State Initialization (BEFORE widgets) ──
if "Kp" not in st.session_state:
    st.session_state["Kp"] = 2.5
if "Ki" not in st.session_state:
    st.session_state["Ki"] = 0.5
if "Kd" not in st.session_state:
    st.session_state["Kd"] = 0.1
if "Setpoint" not in st.session_state:
    st.session_state["Setpoint"] = 80.0

# ── Callbacks — executed BEFORE slider instantiation ──
def apply_gains_controller():
    """Primary Apply — Ziegler-Nichols aggressive preset."""
    st.session_state["Kp"] = 6.0
    st.session_state["Ki"] = 1.5
    st.session_state["Kd"] = 0.8

def set_preset(kp, ki, kd):
    st.session_state["Kp"] = kp
    st.session_state["Ki"] = ki
    st.session_state["Kd"] = kd

def set_setpoint(v):
    st.session_state["Setpoint"] = float(v)

# ── Rapid Gain Presets — Segmented Control ──
with st.sidebar.container(border=True):
    st.markdown(
        '<div class="scada-label">⚡ RAPID GAIN PRESETS</div><div class="scada-hint">One-tap SCADA tuning — Z-N &amp; factory presets</div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.button("CONS", help="Conservative: low overshoot", on_click=set_preset, args=(1.2, 0.25, 0.05), use_container_width=True)
    c2.button("BAL", help="Balanced: factory default", on_click=set_preset, args=(2.5, 0.5, 0.1), use_container_width=True)
    c3.button("AGGR", help="Aggressive: fast response", on_click=set_preset, args=(6.0, 1.5, 0.8), use_container_width=True)
    c4.button("ZN", help="Ziegler-Nichols tuned", on_click=set_preset, args=(8.5, 2.2, 1.0), use_container_width=True)

    st.button("Apply Gains Controller", on_click=apply_gains_controller, use_container_width=True, type="primary")

# ── Kp — SCADA Card ──
with st.sidebar.container(border=True):
    st.markdown('<div class="scada-label">▸ KP — PROPORTIONAL GAIN</div>', unsafe_allow_html=True)
    Kp = st.slider("Kp (Proportional)", 0.0, 20.0, key="Kp", label_visibility="collapsed", step=0.1)
    st.markdown(f'<div class="scada-value"><span>{Kp:.2f} gain</span></div>', unsafe_allow_html=True)

# ── Ki — SCADA Card ──
with st.sidebar.container(border=True):
    st.markdown('<div class="scada-label">▸ KI — INTEGRAL GAIN</div>', unsafe_allow_html=True)
    Ki = st.slider("Ki (Integral)", 0.0, 10.0, key="Ki", label_visibility="collapsed", step=0.05)
    st.markdown(f'<div class="scada-value"><span>{Ki:.2f} gain</span></div>', unsafe_allow_html=True)

# ── Kd — SCADA Card ──
with st.sidebar.container(border=True):
    st.markdown('<div class="scada-label">▸ KD — DERIVATIVE GAIN</div>', unsafe_allow_html=True)
    Kd = st.slider("Kd (Derivative)", 0.0, 5.0, key="Kd", label_visibility="collapsed", step=0.01)
    st.markdown(f'<div class="scada-value"><span>{Kd:.2f} gain</span></div>', unsafe_allow_html=True)

# ── Setpoint — SCADA Card with Segmented Presets ──
with st.sidebar.container(border=True):
    st.markdown('<div class="scada-label">🎯 SETPOINT — TARGET VALUE</div>', unsafe_allow_html=True)
    # Segmented setpoint presets
    s1, s2, s3, s4 = st.columns(4)
    s1.button("40", on_click=set_setpoint, args=(40.0,), use_container_width=True, key="sp40")
    s2.button("60", on_click=set_setpoint, args=(60.0,), use_container_width=True, key="sp60")
    s3.button("80", on_click=set_setpoint, args=(80.0,), use_container_width=True, key="sp80")
    s4.button("100", on_click=set_setpoint, args=(100.0,), use_container_width=True, key="sp100")

    setpoint = st.number_input(
        "Target Setpoint",
        key="Setpoint",
        label_visibility="collapsed",
        step=1.0,
        format="%.1f",
    )
    st.markdown(f'<div class="scada-value"><span>{setpoint:.1f} units</span></div>', unsafe_allow_html=True)

# ── Environment — compact ──
with st.sidebar.container(border=True):
    st.markdown('<div class="scada-label">🌡️ ENVIRONMENT & TIME</div>', unsafe_allow_html=True)
    disturbance = st.slider("External Disturbance", -10.0, 10.0, 0.0, 0.5, label_visibility="visible")
    sim_time = st.slider("Simulation Duration (s)", 10, 100, 30, label_visibility="visible")

# ==========================================
# MAIN DASHBOARD INTERFACE
# ==========================================
st.title("⚡ NEXUS v5.0 — Embedded PID Digital Twin")
st.caption(f"Real-time Industrial Control Simulation | Target Model: **{plant_choice}**")

# Run Simulation Engine
if st.button("▶ Execute Real-Time Simulation"):
    dt = 0.05
    steps = int(sim_time / dt)

    # Initialize Engine
    pid = IndustrialPID(Kp=Kp, Ki=Ki, Kd=Kd)
    plant = PhysicalPlant(plant_type=plant_choice)
    if plant_choice == "Thermal System":
        plant.reset(initial_value=25.0)
    else:
        plant.reset(initial_value=0.0)

    # Logging structures
    time_vec = []
    pv_vec = []
    sp_vec = []
    op_vec = []
    error_vec = []

    # Simulation Loop
    for i in range(steps):
        t = i * dt
        current_pv = plant.state
        u = pid.compute(setpoint, current_pv, dt)
        new_pv = plant.update(u, dt, disturbance=disturbance)

        time_vec.append(t)
        pv_vec.append(current_pv)
        sp_vec.append(setpoint)
        op_vec.append(u)
        error_vec.append(setpoint - current_pv)

    # Metrics Calculations
    iae = np.sum(np.abs(error_vec)) * dt
    ise = np.sum(np.square(error_vec)) * dt
    settling_err = np.abs(error_vec[-100:])
    is_stable = np.mean(settling_err) < (0.02 * setpoint) if setpoint != 0 else True

    # Display Top Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Final Process Value", f"{pv_vec[-1]:.2f}")
    col2.metric("IAE (Absolute Error)", f"{iae:.2f}")
    col3.metric("ISE (Square Error)", f"{ise:.2f}")
    col4.metric("System Stability Status", "STABLE ✅" if is_stable else "UNSTABLE ⚠️")

    # Interactive Plots
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=("Process Response (PV vs SP)", "Controller Output (PWM / % Power)"),
    )

    fig.add_trace(
        go.Scatter(x=time_vec, y=sp_vec, name="Setpoint", line=dict(color="#FFD700", dash="dash")),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(x=time_vec, y=pv_vec, name="Process Value", line=dict(color="#00E676", width=2)),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(x=time_vec, y=op_vec, name="Control Signal (U)", line=dict(color="#00B0FF", width=1.5)),
        row=2,
        col=1,
    )

    fig.update_layout(
        height=550,
        template="plotly_dark",
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="#0A0A0C",
        plot_bgcolor="#12131C",
    )

    st.plotly_chart(fig, use_container_width=True)

    # Export Telemetry Data
    df_log = pd.DataFrame(
        {
            "Timestamp_s": time_vec,
            "Setpoint": sp_vec,
            "ProcessValue": pv_vec,
            "ControlOutput": op_vec,
            "Error": error_vec,
        }
    )

    st.download_button(
        label="📥 Export Industrial Telemetry (CSV)",
        data=df_log.to_csv(index=False).encode("utf-8"),
        file_name="pid_telemetry_data.csv",
        mime="text/csv",
    )
