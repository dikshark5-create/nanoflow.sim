import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. App Header Layout
st.title("NanoFlow-Sim: Advanced Particle Transport Model")
st.write("An interactive simulation modeling nanoparticle concentration decay and subsequent pore clogging inside a reservoir.")

# 2. Creating Control Sliders in the Sidebar
st.sidebar.header("Simulation Inputs")
C0 = st.sidebar.slider("Initial Injection Concentration (ppm)", 100, 2000, 1000, step=100)
k = st.sidebar.slider("Rock Filtration/Adsorption Rate (k)", 0.01, 0.50, 0.15, step=0.01)
max_distance = st.sidebar.slider("Reservoir Distance (meters)", 5, 50, 20)

# NEW SLIDERS FOR PORE CLOGGING
st.sidebar.markdown("---")
st.sidebar.header("Rock Properties")
K0 = st.sidebar.slider("Initial Rock Permeability (mD)", 50, 500, 200, step=10)
clogging_factor = st.sidebar.slider("Pore Clogging Severity Factor", 0.1, 0.9, 0.4, step=0.1)

# 3. Physics Math Simulation
distance_points = np.linspace(0, max_distance, 100)
# Graph 1 Math: Concentration Profile
concentration_points = C0 * np.exp(-k * distance_points)

# Graph 2 Math: Permeability Drop due to trapped particles
trapped_particles = C0 * k * np.exp(-k * distance_points) 
permeability_points = K0 * (1 - (clogging_factor * (trapped_particles / C0)))

# 4. Displaying the Layout in Tabs
tab1, tab2 = st.tabs(["Particle Concentration", "Permeability Damage (Clogging)"])

with tab1:
    st.subheader("Nanoparticle Propagation Profile")
    fig1, ax1 = plt.subplots()
    ax1.plot(distance_points, concentration_points, label="Fluid Concentration", color="teal", linewidth=2)
    ax1.set_xlabel("Distance into Reservoir (m)")
    ax1.set_ylabel("Concentration (ppm)")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend()
    st.pyplot(fig1)
    st.info("This graph shows how the concentration of nanoparticles floating in the fluid decreases as it travels deeper into the rock.")

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
    st.warning("This graph shows pore clogging. Near the injection point (0m), a lot of particles get trapped, causing the rock's permeability to drop significantly. Deeper in the reservoir, the damage decreases.")