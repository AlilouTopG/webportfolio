import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==========================================
# PAGE CONFIGURATION & CYBERPUNK STYLING
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
    .main { background-color: #0A0A0C; color: #E0E0E0; }
    .stMetric { background-color: #12131C; border: 1px solid #1E202D; border-radius: 8px; padding: 10px; }
    .stButton>button { width: 100%; background-color: #00E676; color: #000; font-weight: bold; border-radius: 6px; }
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
# UI SIDEBAR CONTROLS
# ==========================================
st.sidebar.title("🎛️ Control Panel")

plant_choice = st.sidebar.selectbox(
    "Select Industrial Target",
    ["Thermal System", "DC Motor Speed", "Liquid Tank Level"],
)

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ PID Parameters")

# --- FIX: StreamlitWidgetAlreadyInstantiatedError ---
# Initialize session_state for sliders BEFORE widget instantiation
if "Kp" not in st.session_state:
    st.session_state["Kp"] = 2.5
if "Ki" not in st.session_state:
    st.session_state["Ki"] = 0.5
if "Kd" not in st.session_state:
    st.session_state["Kd"] = 0.1

def apply_gains_controller():
    """on_click callback — updates session_state BEFORE sliders are instantiated."""
    # Example: Ziegler-Nichols tuned aggressive preset
    st.session_state["Kp"] = 6.0
    st.session_state["Ki"] = 1.5
    st.session_state["Kd"] = 0.8

# Button uses on_click so state changes happen before slider instantiation on next run
st.sidebar.button(
    "Apply Gains Controller",
    on_click=apply_gains_controller,
    use_container_width=True,
)

# Sliders bound to session_state via key — no value arg to avoid duplicate instantiation
Kp = st.sidebar.slider("Kp (Proportional)", 0.0, 20.0, key="Kp", step=0.1)
Ki = st.sidebar.slider("Ki (Integral)", 0.0, 10.0, key="Ki", step=0.05)
Kd = st.sidebar.slider("Kd (Derivative)", 0.0, 5.0, key="Kd", step=0.01)

st.sidebar.markdown("---")
st.sidebar.subheader("🎯 Setpoint & Environment")
setpoint = st.sidebar.number_input(
    "Target Setpoint", value=50.0 if plant_choice != "Thermal System" else 80.0
)
disturbance = st.sidebar.slider("External Disturbance", -10.0, 10.0, 0.0, 0.5)
sim_time = st.sidebar.slider("Simulation Duration (s)", 10, 100, 30)

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
