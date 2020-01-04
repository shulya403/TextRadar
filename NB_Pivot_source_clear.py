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

        self.brand_models_dict = dict() #словарь бренды : известные модели

        for br in self.brands:

            self.brand_models_dict[br] = self.df[(self.df['Brand'] == br) &
                                  (self.df['TM'].isnull() == False)]['Model'].unique()

        self.df['Cheked'] = 0

    def searcher(self, df_line):

        cons_estim_dict = dict() # словарь известные модели данного бренда : оценка stradar
        for i in self.brand_models_dict[df_line['Brand']]:
            cons_estim_dict[i] = StRadar.stradar(df_line['Source'], i).result()
            print(i, ' - ', df_line['Source'])
            pprint(cons_estim_dict)

        max_estim = max(cons_estim_dict.values()) #максимум оценки по известным названиям модлей
        # словарь меделей имеющих максимальное значение
        max_estim_dict = {k: v for k, v in cons_estim_dict.items() if v == max_estim}

        # Выбираем самое длинное название модели из тех которые дали макисмум совпадения
        if len(max_estim_dict) > 1:
            max_len = max([len(str(l)) for l in max_estim_dict.keys()])
            longest_names = [k for k in max_estim_dict.keys() if len(str(k)) == max_len]

        else:
            longest_names = list(max_estim_dict.keys())

        estim_model_name = str(longest_names[0])

        df_line['Model'] = estim_model_name
        df_line['Cheked'] = 1

        #прибиваем название торговой марки, беря ее из описания известных моделей из основного df
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
        # Пускает apply self.searcher для незапоплненных строчек
       self.df[self.df['TM'].isnull()] = self.df[
               self.df['TM'].isnull()].apply(lambda f: self.searcher(f), axis=1)


       self.nec_output()


nb_excel_clear('NB_Pivot_November_19_py.xlsx', 'NB_Pivot_stradar_lg3-d-lg5len.xlsx').fill_na()









