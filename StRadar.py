# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 22:58:24 2019

@author: shulya403
"""

import numpy as np
from pprint import pprint
import math

class stradar(object):
    
    def coincidence_matrix(self):
        #Матрица совпадений concide_m
        
        concide_m = np.zeros((self.data_len, self.search_len))
        
        for i in range(self.data_len):
            for j in range(self.search_len):
                if (self.data[i] != " ") and (self.search[j] != " "):
                    if self.data[i].lower() == self.search[j].lower():
                        concide_m[i, j] = 1
        
        return concide_m
    
    def groups(self):
        #Поиск групп в concide_m.
        concide_m_clear = self.coincidence_matrix().copy()
        
        self.groups_list = list()
        
        for i in range(self.data_len):
            for j in range(self.search_len):
                if concide_m_clear[i, j] == 1:
                    dia = 0
                    gp_len = 0
                    while (i+dia < self.data_len) and (j+dia < self.search_len) and (concide_m_clear[i+dia, j+dia] == 1):
                        gp_len += 1
                        dia += 1
                    horiz_lines = [y for y in range(i, i + gp_len)]
                    vert_lines = [x for x in range(j, j + gp_len)]
                    self.groups_list.append((horiz_lines, vert_lines, gp_len))
                    #чистка
                    for cl in range(0, gp_len):
                        concide_m_clear[i + cl, j + cl] = 0
        
        return self.groups_list
  
  
    def groups_clear(self):
            #поиск пересекающихся по горизонтали и вертикали более мелких групп и их отсев
        groups_sort = sorted(self.groups(), key=lambda group: group[2], reverse=True)

        for i, big_group in enumerate(groups_sort):
            horiz_big_set = set(big_group[0])
            vert_big_set = set(big_group[1])

            if i != len(groups_sort):
    
                for bottom_group in groups_sort[i+1:]:
                    horiz_bottom_set = set(bottom_group[0])
                    vert_bottom_set = set(bottom_group[1])

                    if (len(horiz_big_set & horiz_bottom_set) != 0) \
                            or (len(vert_big_set & vert_bottom_set) != 0):
                        groups_sort.remove(bottom_group)


        return groups_sort
    
    def result(self):
        #выходная формула (Сумма квадратов длин оставшихся групп делить на сумму длин искомых слов)
        
        groups_cl = self.groups_clear()
        search_words = self.search.split()

        #В зачет идут группы размерностью более 1
        #длина группы в степени (log длины по основанию 3) длина в 3 символа = 3, в 2 = 1,55, в 4 = 5,75
        # поделенный на log положения группы в строке data по основанию (5 плюс длина слова search)

        try:
            concide_exit = [x[2] ** (math.log(x[2], 3) / math.log(x[0][0] + 1, 5 + self.search_len))
                            for x in groups_cl if x[2] > 1]
        except ZeroDivisionError:
            concide_exit = [x[2] ** (math.log(x[2], 3) / math.log(x[0][0] + 2, 5 + self.search_len))
                            for x in groups_cl if x[2] > 1]

        search_ln = [len(y) for y in search_words]
        
        concide_coeff = sum(concide_exit) / sum(search_ln)


  
        return concide_coeff
    
    def __init__(self, data, search):
        self.data = str(data)
        self.data_len = len(self.data)
        
        self.search = str(search)
        self.search_len = len(self.search)
        
        self.total_len = self.data_len + self.search_len + 1
         

        