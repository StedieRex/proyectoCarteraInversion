import os # Importamos el módulo os para poder cambiar el directorio de trabajo
import pandas as pd # Importamos Pandas y para simplificar le asignamos el nombre pd

from pandas_datareader import data as pdr
import yfinance as yf
yf.pdr_override() # Importamos Pandas Datareader y lo parcheamos para que funcione con Yahoo

import numpy as np # Importamos Numpy y le asociamos el nombre np

import datetime # Importamos datetime pero en este caso no vamos a asignarle ningún nombre

# Para graficar correctamente en el notebook hacemos lo siguiente
# esto hace que los gráficos se visualicen en el notebook
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

# Obtener el directorio actual del script, para que el directorio este en el mismo lugar que el script
script_dir = os.path.dirname(os.path.abspath(__file__))
# Cambiar el directorio de trabajo actual al directorio del script
os.chdir(script_dir)

pylab.rcParams['figure.figsize'] = 20, 10 # Definimos el tamaño de los gráficos para que se ajusten bien al notebook

start = datetime.datetime(2017, 1, 1)
end=datetime.datetime(2017, 12, 31)
#tickers=['SAN.MC', 'BBVA.MC', 'TEF.MC', 'ITX.MC', 'REP.MC', 'ACS.MC', 'FER.MC', 'GRF.MC', 'IAG.MC', 'AMS.MC'] #datos de santander, bbva, telefonica, inditex, repsol, acs, ferrovial, grifols, iag, amadeus
dataSantander=pdr.get_data_yahoo('SAN.MC', start=start, end=end)
dataBBVA=pdr.get_data_yahoo('BBVA.MC', start=start, end=end)
dataTelefonica=pdr.get_data_yahoo('TEF.MC', start=start, end=end)
dataInditex=pdr.get_data_yahoo('ITX.MC', start=start, end=end)
dataRepsol=pdr.get_data_yahoo('REP.MC', start=start, end=end)


#print(dataSantander.head())
#imprimiendo los datos de cierre de las acciones de cada mes de santander, bbva, telefonica e inditex
# print(dataSantander['Close'].resample('M').last())
# print(dataBBVA['Close'].resample('M').last())
# print(dataTelefonica['Close'].resample('M').last())
# print(dataInditex['Close'].resample('M').last())

cierreSantander=dataSantander['Close'].resample('M').last()
cierreBBVA=dataBBVA['Close'].resample('M').last()
cierreTelefonica=dataTelefonica['Close'].resample('M').last()
cierreInditex=dataInditex['Close'].resample('M').last()
cierreRepsol=dataRepsol['Close'].resample('M').last()

dfEmpresas=pd.DataFrame(index=cierreSantander.index)
dfEmpresas['Santander']=cierreSantander.loc[:]
dfEmpresas['BBVA']=cierreBBVA.loc[:]
dfEmpresas['Telefonica']=cierreTelefonica.loc[:]
dfEmpresas['Inditex']=cierreInditex.loc[:]
dfEmpresas['Repsol']=cierreRepsol.loc[:]

print(dfEmpresas)

# guardar en un archivo csv
dfEmpresas.to_csv('preciosCierreEmpresas.csv')
