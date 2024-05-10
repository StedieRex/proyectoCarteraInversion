import pandas as pd
import random
import os
import math
# Obtener el directorio actual del script, para que el directorio este en el mismo lugar que el script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Cambiar el directorio de trabajo actual al directorio del script
os.chdir(script_dir)

    
# aqui se aplica la mutacion
def valanceandoInversion(cartera,df): #funcion de aptitud
    
    numFilas = len(df)

    #print(numFilas)
    arrayActivoa = df[cartera[0]].values
    arrayActivob = df[cartera[1]].values

    #print(arrayBBVA)
    #print(arrayTEF)
    #print(sum(arrayBBVA))
    #print(sum(arrayTEF))

    REa = sum(arrayActivoa)/numFilas #reindimiento individual de la empresa a
    REb = sum(arrayActivob)/numFilas #reindimiento individual de la empresa b
    #print(REa)
    #print(REb)

    #rendimiento del portafolio por monto
    #retorna (banco a,banco b,porsentaje1,porcentaje2,rendimiento)
    rendimiento = (0.5*REa)+(0.5*REb)
    if rendimiento < 0.4*REa+0.6*REb:
        rendimiento = 0.4*REa+0.6*REb
        rf = rendimiento/calculandoRiesgo(cartera[0],cartera[1],REa,REb,df,0.4,0.6)
        return [cartera[0],cartera[1],0.4,0.6,rf] #activo a, activo b, porcentajeInversion a, porcentajeInversion b, rendimiento final
    if rendimiento < 0.6*REa+0.4*REb:
        rendimiento = 0.6*REa+0.4*REb
        rf = rendimiento/calculandoRiesgo(cartera[0],cartera[1],REa,REb,df,0.6,0.4)
        return [cartera[0],cartera[1],0.6,0.4,rf]
    
    rf= rendimiento/calculandoRiesgo(cartera[0],cartera[1],REa,REb,df,0.5,0.5)
    return [cartera[0],cartera[1],0.5,0.5,rf]

def calculandoRiesgo(c1,c2,RI1,RI2,df,p1,p2):
    varA=0
    varB=0
    numFilas = len(df)
    arrayBBVA = df[c1].values
    arrayTEF = df[c2].values
    for i in range(numFilas):
        varA += ((arrayBBVA[i]-RI1)**2)/(numFilas-1)
        varB += ((arrayTEF[i]-RI2)**2)/(numFilas-1)

    covAB = 0
    for i in range(numFilas):
        covAB += ((arrayBBVA[i]-RI1)+(arrayTEF[i]-RI2))/(numFilas-1)

    riesgo = (p1**2)*varA + (p2**2)*varB + 2*p1*p2*covAB
    return math.sqrt(riesgo)

def comparandoCarteras(cartera,carteras):

    if len(carteras)==0:
        return True
    
    for cartera2 in carteras:
        if cartera2[0]==cartera[0] or cartera2[0]==cartera[1]:
            if cartera2[1]==cartera[0] or cartera2[1]==cartera[1]:
                return False
        if cartera2[1]==cartera[0] or cartera2[1]==cartera[1]:
            if cartera2[0]==cartera[0] or cartera2[0]==cartera[1]:
                return False
    return True


def crarCarteras(df):#cada cartera es un individuo
    numeroCarteras=10
    
    carteras=[]
    while numeroCarteras>0:
        cartera = []
        #se eligen 2 empresas al azar, para añadirlas a la cartera
        empresas = list(df.columns)
        empresas.remove('Date')

        for _ in range(2):
            eleccion1=random.choice(empresas)
            cartera.append(eleccion1)
            empresas.remove(eleccion1)

        if comparandoCarteras(cartera,carteras):
            carteras.append(cartera)
            numeroCarteras-=1
        

    return carteras

def ruleta(mejoresPortafolios):
    CreandoRuleta = []
    for portafolio in mejoresPortafolios:
        for _ in range(int(portafolio[4])): #se añade el portafolio a la ruleta tantas veces como su rendimiento
            CreandoRuleta.append(portafolio)

    numGiros = 5
    elegidos = []
    for _ in range(numGiros):
        elegidos.append(random.choice(CreandoRuleta))

    return elegidos

def main():
    df = pd.read_csv('data/preciosCierreEmpresas.csv')
    #print(df)
    misCarteras=crarCarteras(df)

    mejoresCarteras = []
    for cartera in misCarteras:
        mejoresCarteras.append(valanceandoInversion(cartera,df))

    seleccion = ruleta(mejoresCarteras)
    print(seleccion)
    #print(mejoresPortafolios)


main()