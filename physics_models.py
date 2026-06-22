import numpy as np

def calculate_concentration(C0, k, distance_points):
    """Calculates nanoparticle concentration decay over distance."""
    return C0 * np.exp(-k * distance_points)

def calculate_permeability(K0, clogging_factor, C0, k, distance_points):
    """Calculates rock permeability reduction due to trapped particles."""
    trapped_particles = C0 * k * np.exp(-k * distance_points)
    # Avoid division by zero if C0 is somehow 0
    with np.errstate(divide='ignore', invalid='ignore'):
        perm_points = K0 * (1 - (clogging_factor * (trapped_particles / C0)))
    return perm_points

def calculate_velocity(permeability_points, A, mu, P_inj, P_res, max_distance):
    """Calculates fluid flow velocity using Darcy's Law."""
    pressure_gradient = (P_inj - P_res) / max_distance
    return (permeability_points * A / mu) * pressure_gradient

def calculate_oil_recovery(days, C0, clogging_factor, average_velocity):
    """Models the Ultimate Oil Recovery Factor over time (The Main Objective)."""
    time_steps = np.linspace(0, days, 100)
    max_possible_recovery = 75 * (1 - (clogging_factor * 0.3))
    recovery_rate = 0.05 * (C0 / 1000) * (average_velocity / 10)
    recovery_points = max_possible_recovery * (1 - np.exp(-recovery_rate * time_steps))
    return time_steps, recovery_points