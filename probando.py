import pandas as pd
import random
import os
import math
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
# Obtener el directorio actual del script, para que el directorio este en el mismo lugar que el script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Cambiar el directorio de trabajo actual al directorio del script
os.chdir(script_dir)

    
# aqui se aplica la mutacion
def valanceandoInversion(cartera,df,pia,pib): #funcion de aptitud
    
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
    if rendimiento < pia*REa+pib*REb:
        rendimiento = pia*REa+pib*REb
        rf = rendimiento/calculandoRiesgo(cartera[0],cartera[1],REa,REb,df,pia,pib)
        return [cartera[0],cartera[1],pia,pib,rf] #activo a, activo b, porcentajeInversion a, porcentajeInversion b, rendimiento final
    if rendimiento < pib*REa+pia*REb:
        rendimiento = pib*REa+pia*REb
        rf = rendimiento/calculandoRiesgo(cartera[0],cartera[1],REa,REb,df,pib,pia)
        return [cartera[0],cartera[1],pib,pia,rf]
    
    rf= rendimiento/calculandoRiesgo(cartera[0],cartera[1],REa,REb,df,0.5,0.5)
    return [cartera[0],cartera[1],0.5,0.5,rf]

def calculandoRiesgo(c1,c2,RI1,RI2,df,p1,p2): #cartera1,cartera2,rendimiento1,rendimiento2,df,p1,p2
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

def eliminarRepetidos(lista):
    listaNueva = []
    for i in lista:
        if i not in listaNueva:
            listaNueva.append(i)
    return listaNueva

def cruzando(c1,c2):
    # tomo las primeras 2 carteras y las cruzo con el resto hasta optener las otras 10 carteras
    nuevaGeneracion = []
    indicePorcentaje = 2
    indiceActivo = 0

    if c2[indicePorcentaje]>c2[indicePorcentaje+1]:
        mejorIndiceP = indicePorcentaje
        mejorIndiceA = 0
    else:
        mejorIndiceP = indicePorcentaje+1
        mejorIndiceA = 1

    if c2[indicePorcentaje]>c2[indicePorcentaje+1] and c1[indiceActivo]!=c2[mejorIndiceA]:
        #print(f"1.[c2{c2[mejorIndiceA]},c1{c1[indiceActivo]}]")
        return[c2[mejorIndiceA],c1[indiceActivo]]
    elif(c1[indiceActivo+1]!=c2[mejorIndiceA]):
        #print(f"2.[c2{c2[mejorIndiceA]},c1{c1[indiceActivo+1]}]")
        return[c2[mejorIndiceA],c1[indiceActivo+1]]
    else:
        return[c2[mejorIndiceA],c1[indiceActivo]]

def darFormato(carteras):
    carterasF = []
    for i in range(0,len(carteras),2):
        if comparandoCarteras([carteras[i],carteras[i+1]],carterasF):
            carterasF.append([carteras[i],carteras[i+1]])
    return carterasF    

def main():
    try:
        n=int(caja_noIteraciones.get())
    except:
        messagebox.showwarning("Numero de generaciones incorrecto", "Por favor ingrese un numero de generaciones valido.")
        return
    if caja_noIteraciones.get() == "" or caja_noIteraciones.get() == "0" or caja_noIteraciones.get() == " ":
        messagebox.showwarning("Sin numero de generación", "Por favor ingrese el numero de generaciones que desea realizar para la evolución de la población.")
        return
    if int(caja_noIteraciones.get()) < 1:
        messagebox.showwarning("Sin numero de generación", "Por favor ingrese un numero de generaciones mayor a 0.")
        return
    if int(caja_noIteraciones.get()) > 5:
        messagebox.showwarning("Numero de generaciones excedido", "Por favor ingrese un numero de generaciones menor o igual a 5.")
        return
    #-------porcentajes dinamicos para el valanceo de invercion------
    porcentajeInversionA = 0.4
    porcentajeInversionB = 0.6
    incrementoInversion = 0.02
    #-------Cargando los datos de los activos en un dataFrame------
    df = pd.read_csv('data/preciosCierreEmpresas.csv')
    #print(df)
    #-------Crando las carteras de forma aleatoria------
    misCarteras=crearCarteras(df)

    #-------Dando su medida a cada cartera con la funcion de aptitud------
    carterasValanceadas = []
    for cartera in misCarteras:
        carterasValanceadas.append(valanceandoInversion(cartera,df,porcentajeInversionA,porcentajeInversionB))

    porcentajeInversionA -= incrementoInversion
    porcentajeInversionB += incrementoInversion
    seleccion = ruleta(carterasValanceadas)
    #print(seleccion)
    #-------comienza la creacion de las nuevas generaciones------- 
    i=0
    noHijos = 8

    seleccion = sorted(seleccion, key=lambda x: x[4], reverse=True)

    cajaTablaAgrupada.config(state="normal")
    cajaTablaAgrupada.insert(tk.END, f"Primera poblacion:\n")
    cajaTablaAgrupada.insert(tk.END, f"{seleccion}\n")
    cajaTablaAgrupada.config(state="disabled")
    
    loMejorDeLaGeneracion = [] #es la seleccion de los primeros lugares de cada generacion

    for _ in range(n):

        loMejorDeLaGeneracion.append(seleccion[0])
        loMejorDeLaGeneracion.append(seleccion[1])
        e1 = seleccion[0]
        e2 = seleccion[1]
        seleccion.remove(e1) 
        seleccion.remove(e2)
        #print(loMejorDeLaGeneracion)
        #print(seleccion)
        noHijos = 7
        nuevaGeneracionSinValance = []
        nuevaGeneracionSinValance.append(cruzando(loMejorDeLaGeneracion[1],loMejorDeLaGeneracion[0]))
        #print("-----------------Creando nueva generacion-----------------")
        for mejorCartera in loMejorDeLaGeneracion:
            for cartera in seleccion:
                nuevo = cruzando(cartera,mejorCartera)
                if comparandoCarteras(nuevo,nuevaGeneracionSinValance) or nuevaGeneracionSinValance ==[]:
                    nuevaGeneracionSinValance.append(nuevo)
                noHijos-=1
                if noHijos==0:
                    break  
        # print("-----------------Nueva Generacion-----------------")
        # print(nuevaGeneracionSinValance)
        # print(" ")

        #print(CarterasNuevaGeneracion)
        #print(" ")
        nuevaGeneracionValanceada = []
        for cartera in nuevaGeneracionSinValance:
            nuevaGeneracionValanceada.append(valanceandoInversion(cartera,df,porcentajeInversionA,porcentajeInversionB))
        porcentajeInversionA -= incrementoInversion
        porcentajeInversionB += incrementoInversion

        nuevaGeneracionValanceada = sorted(nuevaGeneracionValanceada, key=lambda x: x[4], reverse=True)

        loMejorDeLaGeneracion.append(nuevaGeneracionValanceada[0])
        loMejorDeLaGeneracion.append(nuevaGeneracionValanceada[1])
        loMejorDeLaGeneracion = eliminarRepetidos(loMejorDeLaGeneracion)
        loMejorDeLaGeneracion = sorted(loMejorDeLaGeneracion, key=lambda x: x[4], reverse=True)

        nuevaGeneracionValanceada.append(loMejorDeLaGeneracion[0])
        nuevaGeneracionValanceada.append(loMejorDeLaGeneracion[1])

        seleccion.clear()
        seleccion = nuevaGeneracionValanceada
        i+=1

        seleccion = sorted(seleccion, key=lambda x: x[4], reverse=True)
        
        cajaTablaAgrupada.config(state="normal")
        cajaTablaAgrupada.insert(tk.END, f"Generacion No: {i}\n")
        cajaTablaAgrupada.insert(tk.END, f"{seleccion}\n")
        cajaTablaAgrupada.config(state="disabled")

        if len(seleccion)==1:
            break
    
    print(loMejorDeLaGeneracion)

    cajaTablaAgrupada.config(state="normal")
    cajaTablaAgrupada.insert(tk.END, f"Estos son los primeros lugares de cada generacion:\n")
    cajaTablaAgrupada.insert(tk.END, f"{loMejorDeLaGeneracion}\n")
    cajaTablaAgrupada.config(state="disabled")
    
    # grafica donde x es el porcentaje de inversion en el activo a, y es el porcentaje de inversion en el activo b, y z es el rendimiento
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = []
    y = []
    z = []
    for cartera in loMejorDeLaGeneracion:
        x.append(cartera[2])
        y.append(cartera[3])
        z.append(cartera[4])

    print("x")
    print(x)
    print("y")
    print(y)
    print("z")
    print(z)

    sc = ax.scatter(x, y, z, c=z, cmap='RdYlGn')

    # Agregar una barra de colores
    cb = plt.colorbar(sc, ax=ax, shrink=0.5, aspect=5)
    cb.set_label('Intensidad del color deacuerdo al rendimiento')

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

# caja_noIteraciones.config(state="normal")
# caja_noIteraciones.insert(0, "3")
# caja_noIteraciones.config(state="disabled")

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