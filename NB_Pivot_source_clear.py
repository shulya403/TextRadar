# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 01:00:49 2019

@author: shulya403
"""
import pandas as pd
from pprint import pprint
import StRadar

class nb_excel_clear(object):
    def __init__(self, filename, fileresult = ""):
        
        self.df = pd.read_excel(filename)
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
        
        pprint(cons_estim_dict)
        #max_estim = max(list(cons_estim_list[:][1]))
        print(df_line)
        
        return df_line_corrected
    
    def fill_na(self):
       self.df[self.df['TM'].isnull()] = self.df[
               self.df['TM'].isnull()].apply(lambda f: self.searcher(f), axis = 1)

nb_excel_clear('NB_Pivot_November_19_py.xlsx').fill_na() 
        







