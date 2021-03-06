from numpy import arange, sin, cos, sqrt, pi

x = 3
a = arange(7)
b = arange(64)
b.shape = (8,8)
c = arange(10.)/10
u = 0.5
x = 3
y = 2
z = 7.4
alist = [[1.,2.,3.,4.],[6.,7.,8.,9.],['a','b','c','d']]
adict ={'a':1.0, 'b':2.0, 'c':3.0}
yes = True
no  = False
nottrue = False
orx =2
andy = 99

def f1(a, b, c=10):
    "function f1(a,b,c=10)"
    return (a + b)/ c
#enddef

def f2(c=100, **kws):
    """ Doc for f2: """
    return c/2.0
#enddef

def mul2(x, b):
    return x * b
#enddef

## begin

mul2(2.0,5)                
a[2] + 3                 
b[2][4]                  
a[3+1]                   

x == 2                   
x == 3                   
x != 3                   
x >= 1                   
x >= 3                   
x >= 4                   
x < 99                   
(x>u) or x*u>100         
yes and no or nottrue     
yes and (no or nottrue)   
(yes and no) or nottrue   
yes or no and nottrue     
yes or (no and nottrue)   
(yes or no) and nottrue   
yes or not no             
not (no or yes)           
not no or yes             
not yes                   
not no                    
# ! yes                     
# ! no                      
a[0]                      
a[1]                      
a[0] and a[1]             
not a[0]                  
not a[1]                  
not a[2]                  

f1(2,8.0)                 
f1(2,2*7.,c=11.0)         

f1(2,8.0,c=sin(0.3))      
f2()                      
f2(c=99)                  
f2(d=88)                  
max(a[3]*01,9,3)          
sqrt(33.2j / cos(88.0))  
adict['b']                

adict['c'] /adict['b']    
0.2                       
.2                        
0.223e+4                  
.32101e+3j                
 
print adict                     


[1,2,['a', 'b','c'], 4.0] 
alist[2]                  
{'a':1, 'b':2.0, 'c':[1,2,'three']} 
alist                     

-(a[3:5] + 2)             
-a[3:7] + 2.0             

a[2:]                    
'a simple string '        
alist[2][3]               
[0,1,2,4,8,16,32]         
alist[1]                  

j1 = mul2(2.5,b)[3]

mul2(2.5,b)[3,4]            
 
a_string = ' %s = %g '  % ('sqrt(22.3)', sqrt(22.3))

b[2:4,3]                   
b[2:4,3:5]                 
b[2:4]                     
sin(a*pi/20)               




