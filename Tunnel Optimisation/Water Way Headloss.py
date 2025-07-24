
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.optimize import curve_fit

class Headloass:
    
    def __init__(self):
        
        self.g = 9.81
        
    def friction_loss(self, f, l, D, Q):   
        """ Darcy Weisbach equation"""
    
        A = math.pi * D**2 / 4 
        v = Q/ A
        hf = (f * l * v**2)/(D* 2* self.g)
        return hf,v
    
    def minor_loss(self, v, k, nos):
        """Bend loss, niche loss in tunnel and shafts"""
        hl = ( k * v **2)/(2* self.g)
        return hl*nos
    
    def transition_loss(self, Q, D1,D2):       
        A1 = math.pi * D1
        A2 = math.pi * D2
        v1 = Q/ A1
        v2 = Q / A2
        
        hl = (1-A1/A2)**2 * (v1**2/(2*self.g))
            
        return hl
    
    def contraction_loss(self, cl):
        v, g = self.v, self.g
        hl = cl * v**2/(2*g)
        return hl

    
if __name__ == "__main__":
    test = Headloass()
    #%% Input parameters
    data = []
    """
    Update the values in the following section as per the project specification
    """
    for q in np.linspace(20,125, 100):
        tunnel_params = {
            "f": 0.018,     # Darcy friction factor (concrete)
            "l": 5700,      # Length in meters as (update as per project)
            "D": 6.50,       # Diameter in meters
            "Q": q       # Discharge in m³/s
        }
        penstock_params = {
            "f": 0.015,     # Darcy friction factor (concrete)
            "l": 200,      # Length in meters
            "D": 5,       # Diameter in meters
            "Q": q       # Discharge in m³/s
        }
        
        HRT_bends = {
            "k":0.03,
            "nos": 5}
        
        p_bends = {
            "k":0.02,
            "nos": 4}
        
        tran_param = {
            "Q": q ,
            "D1":6.5,
            "D2":5}
        
        niche_param = {
            "k": 0.1,
            "nos": tunnel_params['l']/600}
    #%%Results
    #Tunnel losses
        hft, vt = test.friction_loss(**tunnel_params)
        
        #Penstock losses
        hfp, vp = test.friction_loss(**penstock_params)
        #bend losses
        hb_t = test.minor_loss(vt, **HRT_bends)
        hb_p = test.minor_loss(vp, **p_bends)
        
        #transition losses
        h_trans = test.transition_loss(**tran_param)
        #niche losses
        h_nic = test.minor_loss(vt, **niche_param)
    
        total_t = hft + hb_t+ h_trans+ h_nic
        total_p = hfp + hb_t 
        total = total_p + total_t
        data.append({"Discharge": q,
                      "tunnel_hl": total_t,
                      "Penstock_hl": total_p, 
                      "total_hl": total})   
    
    df = pd.DataFrame(data)   
    print (df)

"""
We will generate an equation for different flow conditions, which will be instrumental in net head calculation for energy/ power generation equation for daily discharge
"""
#%% curve fit for future discharge value
def power_law(Q, a, b):
    return a*Q**b

popt_tunnel, _ = curve_fit(power_law, df.Discharge, df.total_hl)
a_tunnel, b_tunnel = popt_tunnel
print(f"The curve fitting equation is {round(a_tunnel,3)}Q**{round(b_tunnel,3)}")

q_vals = np.linspace(min(df["Discharge"]), max(df["Discharge"]), 100)
plt.figure(figsize= (10,6))
plt.scatter(df.Discharge, df.total_hl,color = 'blue')
plt.plot(q_vals,power_law(q_vals, *popt_tunnel), label=f"Tunnel HL fit: h = {a_tunnel:.4f} * Q^{b_tunnel:.2f}", color='blue', linestyle='--')
plt.xlabel("Discharge (m³/s)")
plt.ylabel("Headloss (m)")
plt.title("Best-fit Curves for Tunnel and Penstock Headloss")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
 


