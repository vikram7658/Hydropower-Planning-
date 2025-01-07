# -- coding: utf-8 --
"""
Optimal Rebar Design for Invert Slab
"""

import pandas as pd
import numpy as np

class Invert:
    def __init__(self, h=1, L = 3.8):
        self.h = h
        self.L = L  # Width of the invert (m)
        self.fy = 500  # Steel yield strength (MPa or N/mm²)
        self.tau = 0.28  # Shear strength (MPa)

    def down_force(self, thick):
        """Calculate the downward force due to self-weight."""
        w = thick * 25 * self.L  # kN
        return w

    def up_force(self):
        """Calculate the upward force due to water pressure."""
        p = 9.81 * self.L * self.h  # kN
        return p

    def moment_SS(self):
        """Calculate bending moments, shear forces, and rebar requirements."""
        data = []
        for t in [0.12, 0.15, 0.2]:  # Various thicknesses of the invert
            AF = self.up_force() - self.down_force(t)  #0 Axial force (kN)
            BM = round(AF * self.L ** 2 / 8, 2)  # Bending moment (kNm) when single dowel is intnroduced
            SF = round(AF / (self.L * t), 2)  # Shear force (kN/m²)
            d_eff = t - 0.05  # Effective depth (subtract0ing cover) 50 mm for structure in concrete
            As = round((BM )*1000 / (0.87*self.fy * d_eff), 2)  # Steel area required (mm²)
            # space = 3*t*1000
            
            optimal_spacing, optimal_dia, opt_area = self.rebar(As)
    
            A_available = opt_area if optimal_spacing else None
            D_opt = optimal_dia if optimal_spacing else None
            
            data.append((t, AF,  SF, BM,  As, optimal_spacing, D_opt, A_available))
        
        df = pd.DataFrame(data, columns=["Thickness (m)", "SF, KN", "AF","BM(kNm)", 
                                         "As_rqd (mm²)", "opt_Space(mm)","opt_dia, mm", 
                                          "As_avai(mm²)"])
        return df

    def area(self, d):
        """Calculate cross-sectional area of a rebar given its diameter."""
        return np.pi * (d ** 2) / 4

    def rebar(self, As):
        """Find the optimal spacing and diameter for rebars."""
        # for d in [10, 12, 16]:  # Available diameters
        dia = [10,12,16,20,25]
        optimal_spacing = None
        opt_area = None
        optimal_dia = None
        for d in dia:
            for s in range(300,100,-50):  # Spacing from 100 mm to 300 mm
                A_bar = self.area(d)
                T_area = round((1000 / s) * A_bar,2)   # Total area for 1 layers
                if As< T_area <= As*1.5:
                    optimal_spacing = s #if s<=200 else 200
                    optimal_dia = d
                    opt_area = T_area
                    break
            if optimal_spacing is not None:
                break
        return  optimal_spacing or "No valid spacing",optimal_dia or "No valid dia",  opt_area or "No valid T_area"  # If no suitable configuration is found
                
# Instantiate and calculate for cahnging invert width
file_path = "Results_with_dowels.txt"
# Open the file in write mode and write the results to it
with open(file_path, "w") as file:
    # file.write(results)
    for i in [3.8,1.9,0.95]: #dividing the invert width into different segments after dowel placement
        invert = Invert(h=1,L=i)
        results = (invert.moment_SS()).to_string(index=False)
        title = f"Results for Total Width = {i:.2f} m with pore pressure of 1 m\n"
        file.write(title + "-" * len(title) + "\n")  # Add a separator line
        file.write(results + "\n\n")
        
#instantiate for changing water head
file_path = "Pore_water_with_dowels.txt"
# Open the file in write mode and write the results to it
with open(file_path, "w") as file:
    # file.write(results)
    for i in np.arange(1,5,1): #for varying pore pressure head
        invert = Invert(h=i, L= 1.9)
        results = (invert.moment_SS()).to_string(index=False)
        title = f"Results for Total pore pressure head = {i:.2f} m and single dowel at center\n"
        file.write(title + "-" * len(title) + "\n")  # Add a separator line
        file.write(results + "\n\n")

