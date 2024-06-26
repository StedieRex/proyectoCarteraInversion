import pandas as pd
import random
import os
import math
import tkinter as tk
from tkinter import scrolledtext
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


def crearCarteras(df):#cada cartera es un individuo
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

    numGiros = 7 # El default es 6
    maximo = 0
    elegidos = []
    while numGiros>0:
        integrar = random.choice(CreandoRuleta)
        if comparandoCarteras(integrar,elegidos):
            numGiros-=1
            elegidos.append(integrar)
        elif maximo>10:
            break
        else:
            maximo+=1

    return elegidos

#def  tomarMejoresActivos():


def cruzandoMejores(seleccion,primeros2,noHIjos):
    # tomo las primeras 2 carteras y las cruzo con el resto hasta optener las otras 10 carteras
    nuevaGeneracion = []
    hijo = []
    pivote = 2

    for cartera in primeros2:
        if cartera[pivote]>cartera[pivote+1]:
            if len(hijo)>0:
                if cartera[pivote-2]==hijo[0]:
                    hijo.append(cartera[pivote-1])
                else:
                    hijo.append(cartera[pivote-2])
            else:
                hijo.append(cartera[pivote-2])
        else:
            if len(hijo)>0:
                if cartera[pivote-1]==hijo[0]:
                    hijo.append(cartera[pivote-2])
                else:
                    hijo.append(cartera[pivote-1])
            else:
                hijo.append(cartera[pivote-1])

    nuevaGeneracion.extend(hijo)
    #print(nuevaGeneracion)
    hijo.clear()
    noHIjos-=1
    
    for mejor in primeros2:
        hijo = []
        #tomamos el mejor activo de una cartera de las primeras 2 mejores
        if mejor[pivote]>mejor[pivote+1]:
            hijo.append(mejor[pivote-2])
        else:
            hijo.append(mejor[pivote-1])

        for cartera in seleccion:
            #tomamos el mejor activo de la cartera sobrante
            if cartera[pivote]>cartera[pivote+1]:
                if cartera[pivote-2] == hijo[0]:
                    hijo.append(cartera[pivote-1])
                    e = cartera[pivote-1]
                else:    
                    hijo.append(cartera[pivote-2])
                    e = cartera[pivote-2]
            else:
                if cartera[-1] == hijo[0]:
                    hijo.append(cartera[pivote-2])
                    e = cartera[pivote-2]
                else:
                    hijo.append(cartera[pivote-1])
                    e = cartera[pivote-1]

            #print(hijo)
            nuevaGeneracion.extend(hijo)
            hijo.remove(e)
            #print(nuevaGeneracion)
            noHIjos-=1
            if noHIjos<0:
                #print(nuevaGeneracion)
                return nuevaGeneracion
        hijo.clear()

    return nuevaGeneracion
    

def darFormato(carteras):
    carterasF = []
    for i in range(0,len(carteras),2):
        if comparandoCarteras([carteras[i],carteras[i+1]],carterasF):
            carterasF.append([carteras[i],carteras[i+1]])
    return carterasF    

def main():
    #-------Cargando los datos de los activos en un dataFrame------
    df = pd.read_csv('data/preciosCierreEmpresas.csv')
    #print(df)
    #-------Crando las carteras de forma aleatoria------
    misCarteras=crearCarteras(df)

    #-------Dando su medida a cada cartera con la funcion de aptitud------
    carterasValanceadas = []
    for cartera in misCarteras:
        carterasValanceadas.append(valanceandoInversion(cartera,df))

    seleccion = ruleta(carterasValanceadas)
    #print(seleccion)
    #-------comienza la creacion de las nuevas generaciones------- 
    n= int(caja_noIteraciones.get())
    i=0
    guardarPrimerosLugares = []
    noHijos = 8
    for _ in range(n):
        primerosDos = []
        seleccion = sorted(seleccion, key=lambda x: x[4], reverse=True)
        if i==0:
            cajaTablaAgrupada.config(state="normal")
            cajaTablaAgrupada.insert(tk.END, f"Primera poblacion:\n")
            cajaTablaAgrupada.insert(tk.END, f"{seleccion}\n")
            cajaTablaAgrupada.config(state="disabled")
            guardarPrimerosLugares.append(seleccion[0])

        primerosDos.append(seleccion[0])
        primerosDos.append(seleccion[1])
        e1 = seleccion[0]
        e2 = seleccion[1]
        seleccion.remove(e1) 
        seleccion.remove(e2)
        #print(primerosDos)
        #print(seleccion)
        sinFormato=cruzandoMejores(seleccion,primerosDos,noHijos)
        noHijos-=2
        #print(CarterasNuevaGeneracion)

        #aqui se eliminan los elementos repetidos que podemos tener en la cruza
        CarterasNuevaGeneracion=darFormato(sinFormato)
        CarterasNuevaGeneracion.append(primerosDos[0])
        CarterasNuevaGeneracion.append(primerosDos[1])

        #print(CarterasNuevaGeneracion)
        #print(" ")
        nuevaGeneracionValanceada = []
        for cartera in CarterasNuevaGeneracion:
            nuevaGeneracionValanceada.append(valanceandoInversion(cartera,df))


        seleccion.clear()
        seleccion=ruleta(nuevaGeneracionValanceada)

        i+=1

        cajaTablaAgrupada.config(state="normal")
        cajaTablaAgrupada.insert(tk.END, f"Generacion No: {i}\n")
        cajaTablaAgrupada.insert(tk.END, f"{seleccion}\n")
        cajaTablaAgrupada.config(state="disabled")
        guardarPrimerosLugares.append(seleccion[0])

        if len(seleccion)==1:
            break

    cajaTablaAgrupada.config(state="normal")
    cajaTablaAgrupada.insert(tk.END, f"Estos son los primeros lugares de cada generacion:\n")
    cajaTablaAgrupada.insert(tk.END, f"{guardarPrimerosLugares}\n")
    cajaTablaAgrupada.config(state="disabled")
    
    # grafica donde x es el porcentaje de inversion en el activo a, y es el porcentaje de inversion en el activo b, y z es el rendimiento
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []
    for cartera in seleccion:
        x.append(cartera[2])
        y.append(cartera[3])
        z.append(cartera[4])

    # print("x")
    # print(x)
    # print("y")
    # print(y)
    # print("z")
    # print(z)

    ax.scatter(x, y, z, c='r', marker='o')
    ax.set_xlabel('Porcentaje de inversion en el activo a')
    ax.set_ylabel('Porcentaje de inversion en el activo b')
    ax.set_zlabel('Rendimiento')
    plt.show()

ventana = tk.Tk()
ventana.title("Algoritmo Genetico")
ventana.geometry("600x500")

#Etiqueta para la lista de nodos
etiqueta_lista = tk.Label(ventana, text="Mostrando ejecucion del algoritmo:")
etiqueta_lista.place(x=800,y=10)
#caja para mostrar como funciona el algortimo

#-----------------BOTON-----------------
# Crear un botón para ejecutar el algoritmo
boton = tk.Button(ventana, text="Ejecutar Algoritmo", command=main)
boton.place(x=10,y=60)

#-----------------Etiqueta-----------------
# Crear una etiqueta para mostrar el resultado
etiqueta = tk.Label(ventana, text="No. iteraciones:")
etiqueta.place(x=10,y=10)

#-----------------Caja de texto-----------------
# Crear una caja de texto para ingresar el número de iteraciones
caja_noIteraciones = tk.Entry(ventana, width=20)#caja para numero de grupos
caja_noIteraciones.place(x=10,y=30)

caja_noIteraciones.config(state="normal")
caja_noIteraciones.insert(0, "3")
caja_noIteraciones.config(state="disabled")

#-----------------Creando la caja de texto con barra de desplazamiento-----------------
# Crear un Frame que contendrá la caja de texto y la barra de desplazamiento
frame_contenedor = tk.Frame(ventana)
frame_contenedor.pack()
frame_contenedor.config(width=300, height=50)
frame_contenedor.place(x=190,y=10)

# Crear una caja de texto con barras de desplazamiento vertical
cajaTablaAgrupada = scrolledtext.ScrolledText(frame_contenedor, height=25, width=45, state="disabled", wrap=tk.NONE)
cajaTablaAgrupada.pack(side="left", fill="both", expand=True)

# Crear una barra de desplazamiento horizontal
scrollbar_horizontal = tk.Scrollbar(frame_contenedor, orient=tk.HORIZONTAL, command=cajaTablaAgrupada.xview)
scrollbar_horizontal.place(x=0, y=388, relwidth=.96, height=20)

# Configurar la caja de texto para desplazarse horizontalmente
cajaTablaAgrupada.config(xscrollcommand=scrollbar_horizontal.set)

ventana.mainloop()