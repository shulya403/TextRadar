# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 22:58:24 2019

@author: shulya403
"""

import numpy as np

class stradar(object):
    
    def coincidence_matrix(self):
        #Матрица совпадений concide_m
        
        concide_m = np.zeros((self.data_len, self.search_len))
        
        for i in range(self.data_len):
            for j in range(self.search_len):
                if (self.data[i] != " ") and (self.search[j] != " "):
                    if self.data[i].lower() == self.search[j].lower():
                        concide_m[i,j] = 1
        
        return concide_m
    
    def groups(self):
        #Поиск групп в concide_m.
        concide_m_clear = self.coincidence_matrix().copy()
        
        self.groups_list = list()
        
        for i in range(self.data_len):
            for j in range(self.search_len):
                if concide_m_clear[i,j] == 1:
                    dia = 0
                    gp_len = 0
                    while (i+dia < self.data_len) and (j+dia < self.search_len) and (concide_m_clear[i+dia, j+dia] == 1):
                        gp_len += 1
                        dia += 1
                    horiz_lines = [y for y in range(i, i + gp_len)]
                    vert_lines = [x for x in range(j, j + gp_len)]
                    self.groups_list.append((horiz_lines, vert_lines,gp_len))
                    #чистка
                    for cl in range (0, gp_len):
                        concide_m_clear[i + cl,j + cl] = 0
        
        return self.groups_list
  
  
    def groups_clear(self):
            #поиск пересекающихся по горизонтали и вертикали более мелких групп и их отсев
        groups_sort = sorted(self.groups(), key = lambda group: group[2], reverse = True)
        for i, big_group in enumerate(groups_sort):
            horiz_big_set = set(big_group[0])
            vert_big_set = set(big_group[1])
    
            for bottom_group in groups_sort[i+1:]:
                horiz_bottom_set = set(bottom_group[0])
                vert_bottom_set = set (bottom_group[1])
                
                try:
                    if len(horiz_big_set & horiz_bottom_set) != 0:
                        groups_sort.remove(bottom_group)
                    if len(vert_big_set & vert_bottom_set) != 0:
                        groups_sort.remove(bottom_group)
                except ValueError as Err:
                    pass
        
        return groups_sort
    
    def result(self):
        
        groups_cl = self.groups_clear()
        search_words = self.search.split()
        
        concide_square = [x[2]**2 for x in groups_cl]
        search_square = [len(y)**2 for y in search_words]
        
        concide_coeff = (sum(concide_square) / sum(search_square)) ** 0.5
  
        return concide_coeff
    
    def __init__(self, data, search):
        self.data = str(data)
        self.data_len = len(self.data)
        
        self.search = str(search)
        self.search_len = len(self.search)
        
        self.total_len = self.data_len + self.search_len + 1
         

        