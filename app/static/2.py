# -*- coding: utf-8 -*-
"""
Created on Tue Dec 28 09:40:54 2021

@author: 18pt08
"""

from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse
from scipy.spatial import distance
import pandas as pd
from numpy.linalg import norm


Arr=pd.DataFrame({'A': [5,0,3,0,2,0,0,2,0,0],
                   'B': [3,0,1,0,1,1,0,1,0,1],
                   'C': [3,0,1,0,1,1,0,1,0,1],
                   'D':[0,7,0,2,1,0,0,3,0,0],
                   'E':[0,1,0,0,1,2,2,0,3,0]
                  })

similarities = cosine_similarity(Arr)
print('output:\n {}\n'.format(similarities))


print("Manhatan")
print (distance.cityblock(Arr.A,Arr.B),"A B")
print (distance.cityblock(Arr.A,Arr.C),"A c")
print (distance.cityblock(Arr.A,Arr.D),"A D")
print (distance.cityblock(Arr.A,Arr.E),"A E")

print (distance.cityblock(Arr.B,Arr.D),"B D")
print (distance.cityblock(Arr.B,Arr.E),"B E")
print (distance.cityblock(Arr.C,Arr.D),"C D") 
print (distance.cityblock(Arr.E,Arr.D),"D E")            
print (distance.cityblock(Arr.C,Arr.E),"C e") 




print("Equilidian")
print (norm(Arr['A'] - Arr['B']),"A B")
print (norm(Arr['A'] - Arr['C']),"A c")
print (norm(Arr['A'] - Arr['D']),"A D")
print (norm(Arr['A'] - Arr['E']),"A E")

print (norm(Arr['D'] - Arr['B']),"B D")
print (norm(Arr['E'] - Arr['B']),"B E")
print (norm(Arr['C'] - Arr['D']),"C D") 
print (norm(Arr['E'] - Arr['D']),"D E")            
print (norm(Arr['E'] - Arr['C']),"C e") 


print("minkowski")
print (distance.minkowski(Arr.A,Arr.B),"A B")
print (distance.minkowski(Arr.A,Arr.C),"A c")
print (distance.minkowski(Arr.A,Arr.D),"A D")
print (distance.minkowski(Arr.A,Arr.E),"A E")

print (distance.minkowski(Arr.B,Arr.D),"B D")
print (distance.minkowski(Arr.B,Arr.E),"B E")
print (distance.minkowski(Arr.C,Arr.D),"C D") 
print (distance.minkowski(Arr.E,Arr.D),"D E")            
print (distance.minkowski(Arr.C,Arr.E),"C e") 

