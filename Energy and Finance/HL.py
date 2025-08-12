
# headloss_model.py

import math
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.optimize import curve_fit

class Headloass:
    
    def __init__(self):
        self.g = 9.81
        
    def friction_loss(self, f, l, D, Q):   
        A = math.pi * D**2 / 4 
        v = Q/ A
        hf = (f * l * v**2)/(D* 2* self.g)
        return hf, v
    
    def minor_loss(self, v, k, nos):
        hl = ( k * v **2)/(2* self.g)
        return hl * nos
    
    def transition_loss(self, Q, D1, D2):       
        A1 = math.pi * D1
        A2 = math.pi * D2
        v1 = Q / A1
        v2 = Q / A2
        hl = (1 - A1 / A2) ** 2 * (v1 ** 2 / (2 * self.g))
        return hl

    def contraction_loss(self, cl):
        v, g = self.v, self.g
        hl = cl * v**2 / (2 * g)
        return hl


    

    #%%
def compute_headloss_coefficients():
    test = Headloass()
    
    data = []
    for q in np.linspace(15, 25, 100):
        tunnel_params = {"f": 0.018, "l": 2300, "D": 3.44, "Q": q}
        penstock_params = {"f": 0.015, "l": 600, "D": 2.5, "Q": q}
        HRT_bends = {"k": 0.03, "nos": 5}
        p_bends = {"k": 0.02, "nos": 4}
        tran_param = {"Q": q, "D1": 3.4, "D2": 4}
        niche_param = {"k": 0.1, "nos": tunnel_params['l'] / 600}

        hft, vt = test.friction_loss(**tunnel_params)
        hfp, vp = test.friction_loss(**penstock_params)
        hb_t = test.minor_loss(vt, **HRT_bends)
        hb_p = test.minor_loss(vp, **p_bends)
        h_trans = test.transition_loss(**tran_param)
        h_nic = test.minor_loss(vt, **niche_param)

        total_t = hft + hb_t + h_trans + h_nic
        total_p = hfp + hb_p
        total = total_p + total_t
        
        data.append({"Discharge": q,
                     "tunnel_hl": total_t,
                     "Penstock_hl": total_p, 
                     "total_hl": total})
    
    df_hl = pd.DataFrame(data) 
 
    
    def power_law(Q, a, b):
        return a * Q ** b
   
    popt_tunnel, _ = curve_fit(power_law, df_hl.Discharge, df_hl.total_hl)
    a_tunnel, b_tunnel = popt_tunnel
    return a_tunnel, b_tunnel
    # print(a_tunnel * 21 ** b_tunnel)
  
test = compute_headloss_coefficients()

