import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd  # Added for the summary data table
from physics_models import (
    calculate_concentration,
    calculate_permeability,
    calculate_velocity,
    calculate_oil_recovery
)

# ==========================================
# 1. APP HEADER
# ==========================================
st.title("NanoFlow-Sim: Advanced Particle Transport Model")
st.write("An interactive simulation modeling nanoparticle concentration decay, pore clogging, and oil recovery inside a reservoir.")

# ==========================================
# 2. SIDEBAR CONTROLS (INPUTS)
# ==========================================
st.sidebar.header("Simulation Inputs")
C0 = st.sidebar.slider("Initial Injection Concentration (ppm)", 100, 2000, 1000, step=100)
k = st.sidebar.slider("Rock Filtration Rate (k)", 0.01, 0.50, 0.15, step=0.01)
max_distance = st.sidebar.slider("Reservoir Distance (meters)", 5, 50, 20)

st.sidebar.markdown("---")
st.sidebar.header("Rock & Fluid Properties")
K0 = st.sidebar.slider("Initial Rock Permeability (mD)", 50, 500, 200, step=10)
clogging_factor = st.sidebar.slider("Pore Clogging Severity", 0.1, 0.9, 0.4, step=0.1)
mu = st.sidebar.slider("Fluid Viscosity (cP)", 1.0, 10.0, 2.0)
P_inj = st.sidebar.slider("Injection Pressure (psi)", 1000, 5000, 3000)
P_res = st.sidebar.slider("Reservoir Pressure (psi)", 500, 3000, 1500)
A = st.sidebar.slider("Cross-sectional Area (m²)", 1.0, 10.0, 5.0)

st.sidebar.markdown("---")
st.sidebar.header("Time Settings")
days = st.sidebar.slider("Injection Duration (Days)", 1, 60, 30)

# ==========================================
# 3. RUNNING SIMULATION (USING IMPORTS)
# ==========================================
distance_points = np.linspace(0, max_distance, 100)

concentration_points = calculate_concentration(C0, k, distance_points)
permeability_points = calculate_permeability(K0, clogging_factor, C0, k, distance_points)
velocity_points = calculate_velocity(permeability_points, A, mu, P_inj, P_res, max_distance)

average_velocity = np.mean(velocity_points)
time_steps, recovery_points = calculate_oil_recovery(days, C0, clogging_factor, average_velocity)

# Base Case Scenario for comparison charts
_, recovery_low_clog = calculate_oil_recovery(days, C0, 0.1, average_velocity)
_, recovery_high_clog = calculate_oil_recovery(days, C0, 0.9, average_velocity)

# ==========================================
# 4. MULTI-TAB INTERFACE
# ==========================================
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Particle Concentration",
    "Permeability Damage",
    "Flow Velocity",
    "🎯 Ultimate Oil Recovery",
    "📊 Project Analytics Dashboard"
])

with tab1:
    st.subheader("Nanoparticle Propagation Profile")
    fig1, ax1 = plt.subplots()
    ax1.plot(distance_points, concentration_points, label="Fluid Concentration", color="teal", linewidth=2)
    ax1.set_xlabel("Distance into Reservoir (m)")
    ax1.set_ylabel("Concentration (ppm)")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend()
    st.pyplot(fig1)
    st.info("Shows how nanoparticle concentration drops as it moves deeper into the formation.")

with tab2:
    st.subheader("Reservoir Permeability Reduction")
    fig2, ax2 = plt.subplots()
    ax2.plot(distance_points, permeability_points, label="Damaged Permeability (K)", color="crimson", linewidth=2)
    ax2.axhline(K0, color="gray", linestyle=":", label="Original Permeability (K0)")
    ax2.set_xlabel("Distance into Reservoir (m)")
    ax2.set_ylabel("Permeability (mD)")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend()
    st.pyplot(fig2)
    st.warning("Pore clogging is highest near the injection wellbore (0m), dropping original permeability down.")

with tab3:
    st.subheader("Fluid Flow Velocity")
    fig3, ax3 = plt.subplots()
    ax3.plot(distance_points, velocity_points, color="green", linewidth=2, label="Velocity")
    ax3.set_xlabel("Distance into Reservoir (m)")
    ax3.set_ylabel("Relative Velocity")
    ax3.grid(True, linestyle="--", alpha=0.6)
    ax3.legend()
    st.pyplot(fig3)
    st.success("Fluid velocity calculation based on the dynamic permeability changes across the reservoir.")

with tab4:
    st.subheader("Oil Recovery Factor over Time")
    fig4, ax4 = plt.subplots()
    ax4.plot(time_steps, recovery_points, color="purple", linewidth=3, label="Recovery %")
    ax4.set_xlabel("Time (Days)")
    ax4.set_ylabel("Oil Recovery Factor (%)")
    ax4.set_ylim(0, 100)
    ax4.grid(True, linestyle="--", alpha=0.6)
    ax4.legend()
    st.pyplot(fig4)
    
    final_recovery = recovery_points[-1]
    st.metric(label="Final Estimated Oil Recovery", value=f"{final_recovery:.2f} %")
    st.info("Main Objective Met: This curve models total sweep efficiency.")

with tab5:
    st.subheader("Project Presentation Analytics")
    st.write("Use this dashboard to show your professors how changing reservoir constraints alters the final project economics.")
    
    # Chart: Comparative Analysis
    st.markdown("### 📈 Scenario Comparison Chart")
    fig5, ax5 = plt.subplots()
    ax5.plot(time_steps, recovery_low_clog, label="Optimized Scenario (Low Clogging)", color="green", linestyle="--")
    ax5.plot(time_steps, recovery_points, label="Your Current Setup", color="purple", linewidth=3)
    ax5.plot(time_steps, recovery_high_clog, label="Critical Damage Scenario (High Clogging)", color="red", linestyle=":")
    ax5.set_xlabel("Time (Days)")
    ax5.set_ylabel("Oil Recovery Factor (%)")
    ax5.set_ylim(0, 100)
    ax5.grid(True, linestyle="--", alpha=0.6)
    ax5.legend()
    st.pyplot(fig5)
    
    # Table: Data Summary Matrix
    st.markdown("### 📋 Generated Reservoir Summary Data Table")
    summary_data = {
        "Metric Parameter": [
            "Initial Injection Concentration",
            "Minimum Permeability Recorded",
            "Average Fluid Flow Velocity",
            "Final Oil Recovery Factor"
        ],
        "Value": [
            f"{C0} ppm",
            f"{np.min(permeability_points):.2f} mD",
            f"{average_velocity:.2f} relative units",
            f"{final_recovery:.2f} %"
        ]
    }
    df = pd.DataFrame(summary_data)
    st.table(df)