# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 09:40:05 2025

@author: vikra
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Tower_foundation:
    
    def __init__(self, t_ht,  c_pull ,fl, fh,  w_l = 47 ):  
        "Cable pull force = 1.4 t (13 Kn) per phase and we have 3 phase in this condition"
        self.t_ht = t_ht
        self.t_load = 1110 #kg
        self.w_l = w_l
        self.c_pull = c_pull
        self.fl = fl #m
        self.fh = fh #m 
        
    def vertical_load(self):
        Towerload = self.t_load * 9.81 /1000          #KN 
        foundation = 25 * self.fl **2 * self.fh     #KN if C25 = 25 nKn/m3 foundation deat wt
        return (Towerload + foundation)
    
    def horizontal_load(self):
        wind = 0.6 * self.w_l **2/1000      #Kn/m2 IS code 875-3 Section 5.4
        later_load = wind * 10          # KN wind exposed area of 5 m2 for lattice girder
        moment = (later_load + self.c_pull) * self.t_ht*0.9
        return moment
    
    def bearing_check(self):
        z = (self.fl*self.fl**2)/6
        A = self.fl**2
        bearing = self.vertical_load() / A + self.horizontal_load() / z
        return bearing
    
    def overturning(self):
        M_resist = self.vertical_load() * self.fl/2
        
        FOS = M_resist/ self.horizontal_load()
       
        return FOS
    
    def Ast(self):
        bearing = self.bearing_check() 
        eff_depth = self.fh - 0.5           # m
        Mu = bearing * (self.fl / 2) ** 2 * 0.5  # KNm
        Ast_reqd = (Mu * 10**6) / (0.87 * 500 * eff_depth*1000)
        
        bars = [10, 12, 16]  # Rebar diameters
        spacing = [100, 150, 200]  # Spacing in mm
        data = []
        
        for s in spacing:
            for d in bars:
                A_bar = np.pi * (d**2) * 0.25  # Cross-sectional area of the bar in mm^2
                bar_area = A_bar * (1000 / s)  # Area of rebar for the given spacing
                
                if  bar_area >= Ast_reqd:
                    data.append((s, d, bar_area))
        
        # Create a DataFrame from the collected data
        df_rebar = pd.DataFrame(data, columns=['spacing', 'diameter', 'Area'])
        df_rebar['Ast_rqd'] = Ast_reqd
        return df_rebar                      

if __name__ == "__main__":
    t_ht = 14           #m
    c_pull = 40*0.5      #3 KN phase tension wire tension sharing from both ends
    w_l = 47            #m/s   as per NEA  
    # w_l = 5 # wind force = 207 Kg/m2 which is equivalent 2.5 m/s
    T2 = Tower_foundation(t_ht, c_pull, 3, 1.5, w_l)
    
    print(f"Total Bearing capacity for the structure is {T2.bearing_check():.3f} Kn/m")   
    print(f" Total Factor safety is {T2.overturning()}")
    
    print(T2.Ast())





    