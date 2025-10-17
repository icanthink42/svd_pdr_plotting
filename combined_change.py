import numpy as np
from numpy.linalg import norm
import plotly.graph_objects as go

def calculate_hohmann_dv(r1, r2, mu):
    v1 = np.sqrt(mu/r1)
    v2 = np.sqrt(mu/r2)

    a_transfer = (r1 + r2) / 2
    v_trans_1 = np.sqrt(mu * (2/r1 - 1/a_transfer))
    v_trans_2 = np.sqrt(mu * (2/r2 - 1/a_transfer))

    dv1 = abs(v_trans_1 - v1)
    dv2 = abs(v2 - v_trans_2)

    return dv1 + dv2

def calculate_plane_change_dv(v_orbit, inclination):
    return 2 * v_orbit * np.sin(inclination/2)

def setup_initial_orbit():
    mu_earth = 3.986004418e14
    r_earth = 6.378137e6
    r_orbit = r_earth + 500000
    return r_orbit, mu_earth

def plot_combined_deltav():
    r1, mu = setup_initial_orbit()

    altitudes = np.linspace(500, 3000, 50)
    inclinations = np.linspace(0, 30, 50)
    alt_mesh, inc_mesh = np.meshgrid(altitudes, inclinations)

    dv_combined = np.zeros_like(alt_mesh)

    for i in range(len(inclinations)):
        for j in range(len(altitudes)):
            r2 = r1 + (altitudes[j] - 500) * 1000
            dv_hohmann = calculate_hohmann_dv(r1, r2, mu)

            v_orbit = np.sqrt(mu/r2)
            dv_plane = calculate_plane_change_dv(v_orbit, np.radians(inclinations[i]))

            dv_combined[i,j] = (dv_hohmann + dv_plane) / 1000

    fig = go.Figure(data=[
        go.Surface(
            x=alt_mesh,
            y=inc_mesh,
            z=dv_combined,
            colorscale='Viridis',
            colorbar=dict(
                title=dict(
                    text='ΔV (km/s)',
                    font=dict(size=16)
                ),
                x=1.1
            )
        )
    ])

    fig.update_layout(
        title=dict(
            text='Delta-V Required for Combined Orbital Changes<br>(From 500km Circular Orbit)',
            font=dict(size=24),
            y=0.95
        ),
        scene=dict(
            xaxis_title=dict(text='Target Altitude (km)', font=dict(size=16)),
            yaxis_title=dict(text='Inclination Change (deg)', font=dict(size=16)),
            zaxis_title=dict(text='Required ΔV (km/s)', font=dict(size=16)),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)
            )
        ),
        width=1200,
        height=800,
        margin=dict(t=100)
    )

    fig.write_html("orbital_maneuvers_3d.html")

def main():
    plot_combined_deltav()

if __name__ == "__main__":
    main()
