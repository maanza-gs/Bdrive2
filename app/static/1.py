# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""


import math

A1 = [1.5,2,1.6,1.2,1.5]
A2 = [1.7,1.9,1.8,1.5,1.0]

x=1.4
y=1.6

manhatan=[]
equl=[]
supremum=[]

def manhattan_distance(a1,a2,x,y):
    for i in range(0,len(a1)):
        print((abs(x-a1[i])+abs(y-a2[i])))
        
    
print("Manhatan")
manhattan_distance(A1,A2,x,y)

 
def euclidean_distance(a1,a2,x,y):
    for i in range(0,len(a1)):
        print(math.sqrt(((abs(a1[i]-x))**2)+(abs(a2[i]-y)**2)))
    
    
 
print ("Equlidian ")
euclidean_distance(A1,A2,x,y)


def cosine(a1,a2,x,y):
    for i in range(0,len(a1)):
        print( (a1[i]*x+a2[i]*y)/  (math.sqrt( a1[i]**2 + x**2) *  math.sqrt( a2[i]**2+y**2)  ))
print ("Cosine ")
euclidean_distance(A1,A2,x,y)