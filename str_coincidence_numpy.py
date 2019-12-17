# -*- coding: utf-8 -*-
"""
Created on Sun Dec 15 04:17:12 2019

@author: shulya403
"""

import numpy as np

data = "HP UMC EB 830G3 8135U 2GB 512SSD GMA800"
#search1 = "Elitebook 830 G3"
#data = "acc knta"
search1 = "Elitebook 830 G3"
search2 = "Elitebook 830 G6"

data_len = len(data)
search_len = len(search1)

total_len = data_len+search_len-1

#Матрица совпадений concide_m
concide_m = np.zeros((data_len, search_len))

for i in range(data_len):
    for j in range(search_len):
        if (data[i] != " ") and (search1[j] != " "):
            if data[i].lower() == search1[j].lower():
                concide_m[i,j] = 1

          
#Поиск групп сразу в concide_m.
concide_m_clear = concide_m.copy()

groups = list()

for i in range(data_len):
    for j in range(search_len):
        if concide_m_clear[i,j] == 1:
            dia = 0
            gp_len = 0
            while (i+dia < data_len) and (j+dia < search_len) and (concide_m_clear[i+dia, j+dia] == 1):
                gp_len += 1
                dia += 1
            horiz_lines = [y for y in range(i, i + gp_len)]
            vert_lines = [x for x in range(j, j + gp_len)]
            groups.append((horiz_lines, vert_lines,gp_len))
            for cl in range (0, gp_len):
                concide_m_clear[i + cl,j + cl] = 0
        
#Сортировка групп по длине

groups_sort = sorted(groups, key = lambda group: group[2], reverse = True)

#поиск пересекающихся по горизонтали и вертикали более мелких групп и их отсев
for i, big_group in enumerate(groups_sort):
    horiz_big_set = set(big_group[0])
    vert_big_set = set (big_group[1])
    
    for bottom_group in groups_sort[i+1:]:
            horiz_bottom_set = set(bottom_group[0])
            vert_bottom_set = set (bottom_group[1])
            
            if len(horiz_big_set & horiz_bottom_set) != 0:
                groups_sort.remove(bottom_group)
            if len(vert_big_set & vert_bottom_set) != 0:
                groups_sort.remove(bottom_group)

    
 

    


#Рассчет итога
            
            



