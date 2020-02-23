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
        self.df = pd.read_excel(self.filename) #df источника
        #self.df.Brand = self.df.Brand.str.lower()
        self.brands = self.df['Brand'].str.lower().unique()
        #self.df.TM = self.df.TM.str.lower()

        #Списки известных моделей по брендам

        self.brand_models_dict = dict() #словарь бренды : известные модели

        for br in self.brands:
            tm_list = self.df[(self.df['Brand'].str.lower() == br) &
                                  (self.df['TM'].isnull() == False)]['TM'].str.lower().unique()
            tm_dict = dict()
            for tm in tm_list:
                tm_dict[tm] = self.df[(self.df['Brand'].str.lower() == br) &
                                                         (self.df['TM'].str.lower() == tm)]['Model'].unique()
            self.brand_models_dict[br] = tm_dict

        pprint(self.brand_models_dict)
        self.df['Cheked'] = 0

    #Основная функция поиска совпадающей модели c использованием модуля STRadar
    def searcher(self, df_line):

        cons_estim_dict = dict() # словарь известные модели данного бренда : оценка stradar
        #множество TM.lower() за вычетом TM совпадающих с названием бренда

        this_brand_tms_set = set(self.brand_models_dict[df_line['Brand'].lower()].keys()) - {df_line['Brand'].lower()}
        print(set(self.brand_models_dict[df_line['Brand'].lower()].keys()))
        print(this_brand_tms_set)

        this_brandline = ''
        for tm in this_brand_tms_set:
            if tm in df_line['Source'].lower():
                if len(tm) > len(this_brandline):
                    this_brandline = tm
        print(df_line['Source'].lower(), this_brandline)

        if this_brandline != '':
            model_array = list(self.brand_models_dict[df_line['Brand'].lower()][this_brandline])
        else:
            model_array = list()
            for i in self.brand_models_dict[df_line['Brand'].lower()].keys():
                model_array += list(self.brand_models_dict[df_line['Brand'].lower()][i])
        print(model_array)

        for i in model_array:
            cons_estim_dict[i] = StRadar.stradar(df_line['Source'], i).result()
        #    print(i, ' - ', df_line['Source'])
        #    pprint(cons_estim_dict)

        max_estim = max(cons_estim_dict.values()) #максимум оценки по известным названиям моедлей
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
            TM_ = self.df[(self.df['Cheked'] == 0) & (self.df['Model'] == df_line['Model'])]['TM'].iloc[0]
        except IndexError:
            TM_ = ''

        df_line['TM'] = TM_
        print(df_line)

        return df_line

    def nec_output(self):

        self.df.to_excel(self.outfile)

        # Вызывная функция заполнения. Пускает apply self.searcher для незапоплненных строчек
    def fill_na(self):

       self.df[self.df['TM'].isnull()] = self.df[
               self.df['TM'].isnull()].apply(lambda f: self.searcher(f), axis=1)


       self.nec_output()


test = nb_excel_clear('NB_Pivot_November_19_py.xlsx', 'test.xlsx').fill_na()









