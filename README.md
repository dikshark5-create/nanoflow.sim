# NanoFlow-Sim: Advanced Particle Transport & Reservoir Recovery Model

An interactive reservoir engineering simulation built with Python and Streamlit. This project models the dynamic relationship between nanoparticle injection, pore clogging (permeability damage), fluid flow velocity, and the ultimate **Oil Recovery Factor (%)**.

---

## 📐 Mathematical & Physics Framework

The project separates its user interface from the core analytical reservoir models to maintain a clean, professional architecture:

### 1. Nanoparticle Concentration Profile
As fluid moves away from the injection wellbore, particles are captured by the rock matrix due to adsorption and mechanical filtration. This concentration decay over distance ($x$) is modeled using a standard exponential filtration equation:
$$C(x) = C_0 \cdot e^{-k \cdot x}$$

### 2. Permeability Alteration (Pore Clogging)
Trapped nanoparticles reduce the available pore throat area, causing a localized drop in rock permeability ($K$). The damaged permeability profile is calculated by tracking the rate of trapped particles:
$$K(x) = K_0 \cdot \left(1 - \beta \cdot \frac{\sigma(x)}{C_0}\right)$$
*Where $\beta$ is the Pore Clogging Severity Factor and $\sigma(x)$ represents the trapped concentration.*

### 3. Fluid Velocity Profile (Darcy's Law)
Using the dynamic, distance-dependent permeability calculated above, the linear fluid flow velocity is modeled using a 1D form of Darcy's Law:
$$v(x) = \frac{K(x) \cdot A}{\mu} \cdot \left(\frac{P_{\text{inj}} - P_{\text{res}}}{L}\right)$$

### 4. Ultimate Oil Recovery (The Main Objective)
The ultimate sweep efficiency and oil recovery over time ($t$) balances the benefit of interfacial tension reduction against the negative impacts of localized pore plugging:
$$RF(t) = RF_{\text{max}} \cdot \left(1 - e^{-\alpha \cdot t}\right)$$
*Where $RF_{\text{max}}$ is mathematically constrained by the clogging severity, and the recovery rate $\alpha$ is a function of the injection concentration and average fluid flow velocity.*

---

## 📂 Project Architecture

The repository is structured as a modular software package:
* `app.py`: Handles the Streamlit user interface, sidebar inputs, data visualization layout, and tab renders.
* `physics_models.py`: Contains the standalone, reusable Python functions representing the reservoir physics equations.
* `README.md`: Project documentation and technical reference report.

---

## 🚀 How to Run the Project

1. Ensure you have the required dependencies installed:
   ```bash
   pip install streamlit numpy matplotlib