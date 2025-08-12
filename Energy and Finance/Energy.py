
import math
import numpy as np
import pandas as pd
import os
import seaborn as sns



from HL import compute_headloss_coefficients
"""
Headloss for different discharge will be different, which will vary the net head of the project at different months,
Thus a fitting equation is imported from the Headloss file
"""
a_tunnel, b_tunnel = compute_headloss_coefficients()
# print(a, b)

class Energy:
    
    def __init__(self, Q_d, GH):
        self.Q_d = Q_d
        self.GH = GH
        
        self.eff_tur = 0.94
        self.eff_g = 0.98
        self.eff_t = 0.99
        self.eff = self.eff_tur * self.eff_g * self.eff_t
    
    def HL(self, Q):
        """Headloss for all discharge"""
        return a_tunnel * Q ** b_tunnel  + 5         #depending on the HW losses change 2-5 m
    
    def net_head(self, Q):
        return self.GH-self.HL(Q)
    
    def power(self, Q):
        
        return self.eff * 9.81 * self.net_head(Q) * Q
        

    
    def general(self, path):
        
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")
        
        df = pd.read_csv(path)
        
        #Adjust Q_av
        # df['Q_av'] = df.Q - 0.1* min(df.Q) 
        df['Q_av'] = df.Q - 0.1* df.Q 
        
        # #for power factor
        # df['Q_all'] = df['Q_av'].apply(lambda q: q if q >= 0.1 *
        #                                 else 0)
        
        #adjust discharge selection rule
        df['Q_used'] = df['Q_av'].apply(lambda q: self.Q_d if q >= self.Q_d
                                        else q if q >= 0.1 *self.Q_d
                                        else 0)
        
        #net head 
        df['Head_loss'] = self.HL(df.Q_used)
        df['Net_head'] = self.GH-self.HL(df.Q_used)
        
        # Calculate power
        df['full_p'] = self.power(df['Q_av']) / 1e3  # optional: convert to kWh
        df['Power_kW'] = self.power(df['Q_used']) / 1e3  # optional: convert to kWh
        return df
   
    def capacity(self, path):
        
        df = self.general(path)
       
        
        #adjust discharge selection rule
        wet_months = ['Mangsir-D','Poush','Magh','Falgun','Chaitra','Baisakh', 'Jestha-D']
        dry_months = ['Jestha-W', 'Asadh', 'Shrawan', 'Bhadra', 'Ashwin', 'Kartik', 'Mangsir-W']
        
        df['P_wet']= df.apply(lambda row: row['Power_kW'] if row['Month'] in wet_months else 0, axis=1)
        
        df['P_dry'] = df.apply(lambda row: row['Power_kW'] if row['Month'] in dry_months else 0, axis=1)
        
        df['wet_energy'] = df.P_wet * df.Days * 24  / 1e3 #Gwh
        df['dry_energy'] = df.P_dry * df.Days * 24  / 1e3  #Gwh
        return df
        

# if __name__ == "__main__":
def export_energy():
    
    project = {
        "Q_d": 21,
        "GH": 2386-2053}
    
    """  The path of CSV from the directory location"""
    path =r"............\Dishcharge.csv"
    
    test = Energy(**project)
    df_result = test.capacity(path)
    total_wet = sum(df_result.wet_energy)
    total_dry = sum(df_result.dry_energy)
    total_energy = total_wet + total_dry
    power_factor = sum(df_result.Power_kW)/ sum(df_result.full_p) 
    print(f"Total dry energy = {total_wet:.3f} GWh \nTotal Wet energy = {total_dry:.3f} GWh")
    print(f"Ratio of dry/wet is {total_wet/total_energy *100 : .3f} %")
    print(f"The plant factor is {power_factor * 100 : .3f} %")
    return total_wet, total_dry

print(export_energy())
