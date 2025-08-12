
import pandas as pd
import math


from Energy import export_energy
dry, wet = export_energy()



class Financial:
    
    def __init__(self, cost, year):
        self.cost = cost
        self.year = year
        self.capacity = 60.2    #MW
        
        self.dry_cost = 8.4     #kwh
        self.wet_cost = 4.8     #Kwh
    
    def upfront_cost(self):
        break_down = [0.2, 0.3, 0.5]
        year = list(range(self.year, self.year+30))
        df = pd.DataFrame({'year': year})
        df['Capital'] = 0
        for i, pct in enumerate(break_down):
            df.loc[i, 'Capital'] = int(self.cost * pct )
        
        df['O&M'] = 0
       
        for i, idx in enumerate(df.index[df['Capital']==0]):
            
            if idx >=3:
                df.at[idx, 'O&M'] = int( round((1.5/100)*self.cost * (1+0.01)**(idx-2), 2)) 
          
        df['Total_cost_mill'] = df['Capital'] + df['O&M']
        return df
    
    def Revenue(self):
        data = self.upfront_cost()
        data['dry_rate'] = 0
        data['wet_rate'] = 0
        data['dry_rate'] = data.index.to_series().apply(
            lambda i:  0 if i <3 else self.dry_cost * (1.03) ** min((i - 3),8))
        data['wet_rate'] = data.index.to_series().apply(
            lambda i:  0 if i <3 else self.wet_cost * (1.03) ** min((i - 3),8))
        data['Bulk_sale'] = dry * data.dry_rate + wet * data.wet_rate
        data['Royalties'] = data.index.to_series().apply( lambda i:  0 if i<3
                                               else self.capacity * 1000* 100/1e3 if i<=15 
                                               else self.capacity * 1000* 1000 /1e3
           )
        #apply 20 % for rows>=3  and <=15
        data['R'] = 0.0   #initialize
        for i in range(3, len(data)):
            royalties = data.iloc[i]['Bulk_sale']
            if royalties <=15:
                data.at[i, 'R'] = royalties * 0.02
            else:
                data.at[i, 'R'] = royalties *0.1
        data['T_royal'] = data['Royalties'] + data [ 'R']
        return data

    
if __name__ == "__main__":
    test = Financial(60.2*200, 2025)
    rev = test.Revenue()
    data = pd.DataFrame(rev)
    print(data)