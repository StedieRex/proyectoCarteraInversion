import pandas as pd
import random
import os
# Obtener el directorio actual del script, para que el directorio este en el mismo lugar que el script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Cambiar el directorio de trabajo actual al directorio del script
os.chdir(script_dir)

# aqui se aplica la mutacion
def valanceandoInversion(cartera,df):
    
    numFilas = len(df)

    #print(numFilas)
    arrayBBVA = df[cartera[0]].values
    arrayTEF = df[cartera[1]].values

    #print(arrayBBVA)
    #print(arrayTEF)
    #print(sum(arrayBBVA))
    #print(sum(arrayTEF))

    REa = sum(arrayBBVA)/numFilas #reindimiento individual de la empresa a
    REb = sum(arrayTEF)/numFilas #reindimiento individual de la empresa b
    #print(REa)
    #print(REb)

    #rendimiento del portafolio por monto
    #retorna (banco a,banco b,porsentaje1,porcentaje2,rendimiento)
    rendimiento = (0.5*REa)+(0.5*REb)
    if rendimiento < 0.4*REa+0.6*REb:
        rendimiento = 0.4*REa+0.6*REb
        return (cartera[0],cartera[1],0.4,0.6,rendimiento)
    if rendimiento < 0.6*REa+0.4*REb:
        rendimiento = 0.6*REa+0.4*REb
        return (cartera[0],cartera[1],0.6,0.4,rendimiento)
    
    return (cartera[0],cartera[1],0.5,0.5,rendimiento)

def buscandoIguales(cartera,carteras):
    if carteras == []:
        return True
    
    for cartera2 in carteras:
        if cartera[0] == cartera2[0] and cartera[1] == cartera2[1]:
            return True
    return False

'''falta que esta funcion no de carteras iguales'''
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

        carteras.append(cartera)
        numeroCarteras-=1
        # if buscandoIguales(cartera,carteras):
        #     carteras.append(cartera)
        #     numeroCarteras-=1
        # else:
        #     numeroCarteras+=1

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

    mejoresPortafolios = []
    for cartera in misCarteras:
        mejoresPortafolios.append(valanceandoInversion(cartera,df))

    seleccion = ruleta(mejoresPortafolios)
    print(seleccion)
    #print(mejoresPortafolios)


main()