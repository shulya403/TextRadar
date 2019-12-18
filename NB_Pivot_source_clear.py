# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 01:00:49 2019

@author: shulya403
"""
import pandas as pd
from pprint import pprint
import StRadar

class nb_excel_clear(object):
    
    def __init__(self, filename, fileresult):
        
        self.filename = str(filename)
        self.outfile = str(fileresult)
        self.df = pd.read_excel(self.filename)
        self.df.Brand = self.df.Brand.str.lower()
        self.brands = self.df.Brand.unique()
       
        #Списки известных моделей по брендам
        
        self.brand_models_dict = dict()

        for br in self.brands:
            
            self.brand_models_dict[br] = self.df[(self.df['Brand'] == br) & 
                                  (self.df['TM'].isnull() == False)]['Model'].unique()
            
        self.df['Cheked'] = 0
        
    def searcher(self, df_line):
        
        cons_estim_dict = dict()
        for i in self.brand_models_dict[df_line['Brand']]:
            cons_estim_dict[i] = StRadar.stradar(df_line['Source'], i).result()
        

        max_estim = max(cons_estim_dict.values())
        print('max', max_estim)
        
        max_estim_dict = {k:v for k,v in cons_estim_dict.items() if v == max_estim}
        pprint(max_estim_dict)
        
        
        if len(max_estim_dict) > 1:
            max_len = max([len(str(l)) for l in max_estim_dict.keys()])
            longest_names = [k for k in max_estim_dict.keys() if len(str(k)) == max_len]
            
        else:
            longest_names = list(max_estim_dict.keys())
        
        estim_model_name = str(longest_names[0])
        
        df_line['Model'] = estim_model_name
        df_line['Cheked'] = 1
        try:    
            TM = self.df[(self.df['Cheked'] == 0) & (self.df['Model'] == df_line['Model'])]['TM'].iloc[0]
        except IndexError:
            TM = ''

        df_line['TM'] = TM
        print(df_line)
        
        return df_line
    
    def nec_output(self):
        
        self.df.to_excel(self.outfile)
        
    def fill_na(self):
       self.df[self.df['TM'].isnull()] = self.df[
               self.df['TM'].isnull()].apply(lambda f: self.searcher(f), axis = 1)
       
       
       self.nec_output()
    

nb_excel_clear('NB_Pivot_November_19_py.xlsx', 'NB_Pivot_November_19_1.xlsx').fill_na() 

        







