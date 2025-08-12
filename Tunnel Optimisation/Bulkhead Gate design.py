

import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class BH:
    
    def __init__(self, D, hw, fric, co ):
        self.D = D 
        self.hw = hw
        
        self.fc = 25*1000  #Kpa
        self.spw = 10       #KN/m3
        self.spr = 27       #KN/m3
        self.sig_n =0.15 *1000   #Kpa
        
        self.fric= math.radians(fric)
        self.co = co
        
        self.Jr = 1.5
        self.Ja = 4
        self.JCS = 20*1000    #KPa
        self.JRC = 20 * (self.Jr/self.Ja) 
        

    def w_head(self):
        p_w = self.spw * self.hw
        
        return p_w
    
    def hoop(self):
        area = math.pi * self.D**2 *0.25
        h_stress = area * self.w_head()
        return h_stress
    
    def c_shear(self):
        fric, sig_n, JRC, JCS = self.fric, self.sig_n, self.JRC, self.JCS
        tau = self.co + sig_n * math.tan(fric)
        tau_1 = sig_n * math.tan(math.radians((math.degrees(fric) + JRC * math.log10(JCS/sig_n))))
        return tau, tau_1
    
    def l_plug(self):
        L = (2*self.hoop())/(self.c_shear()[0]* math.pi * self.D)
        return round (L, 2)
        # print ("The required length of plug is " + str(round(L,2)) + " m") 
    def c_strenght(self):
        hoop = self.hoop()
        t = math.sqrt(hoop * 4 / (math.pi * self.fc ))
        return round (t, 2)
    
if __name__ == "__main__":
    
    D = 5          #Daimter of tunnel/plug, m
    hw = 35        #Max head at plug/ gate area, m
    fric = 30       #frictional resistance of host rock
    co = 30         #cohesion, Kpa
    
    
    test = BH(D, hw,    fric, co)
    print(test.hoop(), test.c_shear())
    print(test.l_plug(), test.c_strenght())
    