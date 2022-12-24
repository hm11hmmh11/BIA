from django.shortcuts import render
from array import array
from asyncio.windows_events import NULL
from django.shortcuts import render
from django.http import HttpResponse
from collections import deque
from django.http.response import JsonResponse
from django.shortcuts import HttpResponse
from django.core import serializers
import json
from django.http import JsonResponse
import numpy as np



# Create your views here.
def hompage(request):
    return render(request,'hompage.html')

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

variable=[]
v=[0]
tur1=["","","","",""]
tur2=["","","","",""]
conditions=["","","","",""]
f=''
def condition(m,ty,tur1,conditions=[""]):
    loptur23= True
    loptur2 =True
    comma=ty.find(",")
    ct=0
    items_c =[]
    for c in ty:
        items_c += c
        
        if ct >=1:
            if  items_c[ct-1].isalpha() == True :
                if items_c[ct].isdigit() == True :
                    ty=ty.replace(items_c[ct-1]+items_c[ct],items_c[ct-1]+"*"+items_c[ct])
                    
            elif items_c[ct-1].isdigit() == True :
                if items_c[ct].isalpha() == True :
                    ty=ty.replace(items_c[ct-1]+items_c[ct],items_c[ct-1]+"*"+items_c[ct])
        ct=ct+1 
    
    for t in ty:
         if t.isalpha() == True:
             for b in range(0,len(variable)):
                 if t == variable[b]:
                     z=b+1
                     ty=ty.replace(t,f"v[{z}]",z)
    v=ty.find(">")
                    
    ty=ty.replace(",", ty[v:]+" and ")
    
    conditions[m] = ty
    tur=ty
    ct=0
    items_c=[]
    loptur = True
    for c in tur:
      items_c += c
      if ct >=1:
          if  items_c[ct-1] + items_c[ct] =="<=" :
                  tur=tur.replace(items_c[ct-1]+items_c[ct],"==") 
                  loptur=False
                  loptur2=False
          if items_c[ct-1] + items_c[ct] ==">=" :
                  tur=tur.replace(items_c[ct-1]+items_c[ct],">") 
                  loptur=False
                  loptur23= False
      ct=ct+1
      
    
    if loptur == True:
        items_c=[]
        
        ct=0
        for c in tur:
            items_c +=c
            if ct >=1:
                if  items_c[ct-1] =="<" and items_c[ct] != "=":
                    tur=tur.replace(items_c[ct],"==-1+") 
                    break
                if items_c[ct-1] !="<" and items_c[ct] =="=" :
                    tur=tur.replace(items_c[ct],"==")
                    break
                if items_c[ct-1] !=">" and items_c[ct] =="=" :
                    tur=tur.replace(items_c[ct],"==")
                    break
            ct=ct+1
    
    tur1[m]=tur
    tur2[m]=ty
    
    v=tur2[m].find("=")
    if comma == -1 and loptur23 == False:
        tur2[m]=tur2[m][v+1:]+"+"+tur2[m][v+1:]+"*0.1 >= "+tur2[m][:v]
        tur2[m]=tur2[m].lstrip(">")
        tur2[m]=tur2[m].lstrip("<")
        tur2[m]=tur2[m].lstrip("=")
        tur2[m]=tur2[m].rstrip(">")
        tur2[m]=tur2[m].rstrip("<")
        tur2[m]=tur2[m].rstrip("=")
        
    if comma == -1 and loptur2 == False:
        tur2[m]=tur2[m].lstrip(">")
        tur2[m]=tur2[m].lstrip("<")
        tur2[m]=tur2[m].lstrip("=")
        tur2[m]=tur2[m].rstrip(">")
        tur2[m]=tur2[m].rstrip("<")
        tur2[m]=tur2[m].rstrip("=")


def fx(f,variable,v=[0]):
    # variable=[]
    items_t=[]
    ft=0
    va=1
    for c in f:
        items_t += c
        
        if ft >=1:
            if items_t[ft-1].isdigit() == True :
                if items_t[ft].isalpha() == True :
                    f=f.replace(items_t[ft-1]+items_t[ft],items_t[ft-1]+"*"+items_t[ft])
                   
            if items_t[ft-1].isalpha() == True :
                if items_t[ft].isdigit() == True :
                    f=f.replace(items_t[ft-1]+items_t[ft],items_t[ft-1]+"*"+items_t[ft])
                           
        
        ft=ft+1

    va=1
    for c in f:

        if c.isalpha() == True:
            
            variable += c
            v += c
            f=f.replace(c,f"v[{va}]",va)
            va=va+1
    return f

def init_pop(pop_size,lenvarible):
    return np.random.randint(-200,200,size=(pop_size, lenvarible))


def calc_fitness(population):
    fitness_vals = []
    
    
    for x in population:
        penalty=0
        n=1
        for z in x:
            v[n]=z
            n=n+1
        for w in range(0,5):
            if conditions[w]=="":
                penalty =penalty+ 13
            elif eval(conditions[w]) == True:
                penalty = penalty+7
                if eval(tur1[w])==True:
                    penalty = penalty+4 
                if eval(tur2[w])==True:
                    penalty = penalty+2
                    
                
                    
        fitness_vals.append(penalty)
    return np.array(fitness_vals)


def selection(population, fitness_vals) :
    probs = fitness_vals.copy()
    probs += abs(probs.max()) 
    probs= probs/probs. sum()
    N = len(population)
    indices=np.arange(N)
    selected_indices= np.random.choice(indices, size=N, p=probs)
    selected_population=population[selected_indices]
    return selected_population

def crossover(parent1, parent2, pc):
    r = np.random.random()
    if r < pc:
        m = np.random.randint(1, len(variable)-1)
        child1= np.concatenate([parent1[ :m], parent2[m:]])
        child2= np.concatenate([parent2[ :m], parent1[m:]])
    else:
        child1 = parent1.copy()
        child2= parent2.copy()
    return child1, child2


def mutation(individual, pm):
    r = np.random.random()
    if r < pm:
        m = np.random.randint(len(variable))
        individual [m]= np.random.randint(len(variable))
    return individual


def crossover_mutation(selected_pop, pc, pm) :
    N = len(selected_pop)
    new_pop= np.empty((N, len(variable)), dtype=int)
    for i in range(0, len(variable), 2): 
        parentl= selected_pop[i]
        parent2= selected_pop[i+1]
        child1, child2 = crossover(parentl, parent2, pc)
        new_pop[i]= child1
        new_pop[i+1]= child2
    for i in range(N):
        mutation(new_pop[i], pm)
    return new_pop


def eight_queens(lenvarible,pop_size, max_generations, pc=0.7, pm=0.01):
   
    n=16
    k=50
    population= init_pop(pop_size,lenvarible)
    best_fitness_overall = None
    for i_gen in range(max_generations) :
        if i_gen == k :
            population= init_pop(pop_size,lenvarible)
            k=k+50
        fitness_vals= calc_fitness(population)
        best_i = fitness_vals.argmax()
        best_fitness = fitness_vals[best_i]
        if best_fitness_overall is None or best_fitness > best_fitness_overall:
            best_fitness_overall = best_fitness
            best_solution=population[best_i]
        print(f'\rgen={i_gen+1:06} -besst f={best_fitness_overall:03} best={population[best_i]} -besst f={best_fitness:03} best={best_solution}',end='')
        

        if best_fitness == 65:
            print( '\nFound optimal solution')
            print( best_solution )    
            break
        selected_pop=selection(population, fitness_vals)
        population= crossover_mutation(selected_pop,pc, pm)
    print()
    b=0
    n=1
    for c in  best_solution:
        
        v[n]=c
        print(f"{variable[b]}={c}")
        b=b+1
        n=n+1
        

    return best_solution,variable

def test(request):
    # variable=[]

    names=[]
    data=request.POST
        # y=x["fun"]
    for x in data:
        names.append(x)
    names.pop(0)
    names.pop(0)
    f=data["fun"]
    f=fx(f,variable,v)
    print(f)
    m=0
    for x in names: 
            ty = data[x]
            if ty=="":
                break
            condition(m,ty,tur1,conditions)
            m=m+1
    
    x,y=eight_queens(len(variable),pop_size=200, max_generations=200, pc=0.5, pm=0.05)
    resulte={
        'var':x,
        'res':y,
        'f':f"f={eval(f)}",
        'n':len(x)
    }
    resulte2=[y,x]
    resulte3={
        'arr':resulte2,
        'n':len(x)
    }
    # x=''
    print(x)
    print(y)
    print(resulte)
    # print(f"f={eval(f)}")   
    # print("==========================================")
    # print(x[2])
    # best={"x":8,y:,z:}
    # variable=[]
    return render(request,'test.html',resulte)

    # print (best)
    # return JsonResponse((names), safe=False)

