

import numpy as np
import math
import seaborn as sns
import pandas  as pd
import matplotlib.pyplot as plt
# from boq.py import boq_cost


class Optimisation:
    
    def __init__(self, Q):
        """
        Cost of cement, rebar might vary as per site location and time of analysis
        """
        self.Q =Q
        self.v = 1.5            #limiting velocity 
        self.length = 2380      #waterway length
        
        self.e_c = 5000           #excavation cost
        self.m_c = 550              #mucking cost
        self.s_c = 65000            #shotcrete cost
        self.c_c = 26000            #concrete lining cost
        self.b_c = 3000             #bolt cost
        self.r_c = 160              #rebar cost
        
        self.sfr = 0.15             #shotcrete thickness
        self.cl = 0              #concrete lining thickness
        #coefficient for darcy equation
        
        
    def tunnel_base(self):
        A = self.Q / self.v
        d = round((4*A/math.pi)**0.5,3)
        d_ex = round(d + (self.sfr + self.cl) * 2, 3)
        
        return d, d_ex
    
    def tunnel(self, D):
        A = math.pi * D ** 2 /4
        v = self.Q / A
        D_ex = round(D + 2 *(self.sfr+self.cl) ,3)
        return  v, D_ex
    
    def tunnel_cost(self, D ):
        v, D_ex = self.tunnel(D)
        area = math.pi * D_ex**2 /4
        peri = math.pi * D_ex
        exc_cost = area * self.e_c
        muc_cost = 1.1 * area * self.m_c
        sfr_cost = peri * self.sfr * self.s_c
        c_c = peri * self.cl * self.c_c
        r_c = peri * self.cl * 7850 * 1.5/100 * self.r_c
        b_c = peri/1.5 * self.b_c
        total_cost = exc_cost + muc_cost + sfr_cost + c_c + r_c + b_c
        total = 1.4 * total_cost * self.length
        return round(total,2)               #millon 
    
    def boq_cost(self, d):
        return (11778.027208 * d**2 + 54973.159049 * d + 36440.589826)*self.length
    
    def head_loss(self, D):
        """Darcy weisbach equation"""
        v, D_ex = self.tunnel(D)
        factor = 0.01507
        hf = factor * (self.length/ D) * (v**2 /(2*9.81))
        return  hf, v               #in m
      
    def energy(self, D):
        """ As per current NEA rate, 
        dry energy = 8.4 NRS/Kwh
        wet energy = 4.8 NRs/Kwh
        average = 0.7*4.8+0.3*8.4
        """
        rate = 5.88                     #NRS/unit
        pf = 0.66                       #Plant factor
        p = self.head_loss(D)[0] * 0.90* 9.81* self.Q
        loss = p * 24 *365 *pf * rate   
        return p, loss
        
    def NPV(self, cost, n, R):
        
        annuity = cost* ((1-(1+R)**(-n))/R)
        return annuity 
        
    
if __name__ == "__main__":
    test = Optimisation(21)
    d, d_ex = test.tunnel_base()
    # print (test.NPV(1, 30, 0.1))
   
    data = []
    for i in np.arange(d-2, d+2, 0.01):
        hf, v = test.head_loss(i)
        tunnel_cost = test.tunnel_cost(i) 
        total_boq = test.boq_cost(i) 
        power, cost = test.energy(i)   
        energy_loss = test.NPV(cost, 30, 11/100)
        total_1 = round(energy_loss + tunnel_cost, 2)
        total_2 = round(energy_loss + total_boq, 2)
        data.append({"dia": i,
                     "v": v,
                     "headloss": hf,
                     
                     "tun_cost": tunnel_cost/1e6,
                     "Energy_loss": energy_loss/1e6,
                     "total_cost_1": total_1/1e6,
                     "total_cost_2": total_2/1e6})
    df = pd.DataFrame(data)
    
    dia_1 = df['dia'][df['total_cost_1'].idxmin()]
    dia_2 = df['dia'][df['total_cost_2'].idxmin()]

    # dia_v = [df['v']3]]
    
    print(f"The optimised diameter of tunnel is {dia_1, dia_2}  m" )
    
    
    def plot(data):
        
        sns.lineplot(data, x = "dia", y = "tun_cost", label= "Tunnel cost")
        sns.lineplot(data, x = "dia", y = "Energy_loss", label = "Energy loss")
        sns.lineplot(data, x = "dia", y = "total_cost_1", label = "Total cost")
        # plt.axvline(dia, color = 'y', linestyle = '--', linewidth = 1, label = f"optimum dia = {dia:.2f} m")
        plt.legend()
        
  
    print(plot(df))
    
    
        