
import numpy as np
import matplotlib.pyplot as plt

# Define the Manning's equation for open channel flow
class OpenChannelFlow:
    def __init__(self, slope, width, mannings_n):
        self.slope = slope        # Channel slope
        self.width = width        # Channel bottom width (m)
        self.n = mannings_n       # Manning's roughness coefficient

    def flow_area(self, depth):
        return self.width * depth  # Area for rectangular channel

    def wetted_perimeter(self, depth):
        return self.width + 2 * depth  # Wetted perimeter for rectangular channel

    def hydraulic_radius(self, depth):
        return self.flow_area(depth) / self.wetted_perimeter(depth)

    def velocity(self, depth):
        R = self.hydraulic_radius(depth)
        return (1 / self.n) * R**(2/3) * self.slope**0.5

    def discharge(self, depth):
        A = self.flow_area(depth)
        V = self.velocity(depth)
        return A * V

    def depth_for_discharge(self, target_discharge, depth_guess=1.0):
        """Use Newton-Raphson method to find the depth for a given discharge."""
        depth = depth_guess
        for _ in range(100):
            Q = self.discharge(depth)
            dQ_dd = (self.discharge(depth + 0.001) - Q) / 0.001
            depth -= (Q - target_discharge) / dQ_dd
            if abs(Q - target_discharge) < 1e-6:
                break
        return depth

# Parameters
slope = 1 / 600           #update as per the project requirement and availability
width = 5.2                # meters as per project
"""
For flow distribution, distribute based on the number of turbines, COL allowable, minimum flow and limiting flow value
0.5 = fifty percent flow
0.55 = one turbine with 5 % col
1.00 = two turbine 0 % col
1.05 = two turbine 5 % col
"""

discharges = [47.6 * factor for factor in [0.50, 0.55, 1.00, 1.05]]
mannings_values = [0.012, 0.018, 0.025, 0.040]  # Concrete, shotcrete, rough shotcrete, unlined

# Prepare plot
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
colors = ['b', 'g', 'r', 'k']
depths_data = {n: [] for n in mannings_values}
velocities_data = {n: [] for n in mannings_values}

# Calculate and store depths and velocities
for n in mannings_values:
    channel = OpenChannelFlow(slope, width, n)
    for Q in discharges:
        depth = channel.depth_for_discharge(Q, depth_guess=1.0)
        velocity = channel.velocity(depth)
        depths_data[n].append(depth)
        velocities_data[n].append(velocity)

# Plot velocity vs discharge
for i, n in enumerate(mannings_values):
    axes[0].plot(discharges, velocities_data[n], marker='o', color=colors[i], label=f'n={n}')
    
for Q in discharges:
    axes[0].axvline(Q, linestyle='--', color='gray', alpha=0.5)
    axes[0].text(Q, axes[0].get_ylim()[1]*0.95, f'{Q:.1f} m3/s', rotation=90,
                 verticalalignment='top', horizontalalignment='right', fontsize=10)
axes[0].set_title('Velocity vs Discharge')
axes[0].set_xlabel('Discharge (m³/s)')
axes[0].set_ylabel('Velocity (m/s)')
axes[0].legend()
axes[0].grid(True)

# Plot depth vs discharge
for i, n in enumerate(mannings_values):
    axes[1].plot(discharges, depths_data[n], marker='o', color=colors[i], label=f'n={n}')
    
for Q in discharges:
    axes[1].axvline(Q, linestyle='--', color='gray', alpha=0.5)
    axes[1].text(Q, axes[1].get_ylim()[1]*0.95, f'{Q:.1f} m3/s', rotation=90,
                 verticalalignment='top', horizontalalignment='right', fontsize=10)
axes[1].set_title('Water Depth vs Discharge')
axes[1].set_xlabel('Discharge (m³/s)')
axes[1].set_ylabel('Water Depth (m)')
axes[1].legend()
axes[1].grid(True)

plt.suptitle(f'Tailrace Flow for B={width} m')
plt.tight_layout()
plt.savefig('Tailrace Optimisation.png', dpi=300, bbox_inches='tight')

plt.show()

