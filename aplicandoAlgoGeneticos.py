import pandas as pd
import random
import os
# Obtener el directorio actual del script, para que el directorio este en el mismo lugar que el script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Cambiar el directorio de trabajo actual al directorio del script
os.chdir(script_dir)

def c(carteras,df):
    prueba = carteras[0]
    numFilas = len(df)
    
    #print(numFilas)
    arrayBBVA = df[prueba[0]].values
    arrayTEF = df[prueba[1]].values
def crarCarteras(df):#cada cartera es un individuo
    numeroCarteras=10
    
    carteras=[]
    for i in range(numeroCarteras):
        cartera=[]
        #se eligen 2 empresas al azar, para añadirlas a la cartera
        empresas = list(df.columns)
        empresas.remove('Date')

        for j in range(2):
            eleccion1=random.choice(empresas)
            cartera.append(eleccion1)
            empresas.remove(eleccion1)

        carteras.append(cartera)
    return carteras
def main():
    df = pd.read_csv('data/preciosCierreEmpresas.csv')
    #print(df)
    misCarteras=crarCarteras(df)
    c(misCarteras,df)
    #print(misCarteras)


main()