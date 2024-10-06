# kriging.py

## Tabla de Contenidos
- [kriging.py](#krigingpy)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Descripción](#descripción)
  - [Funciones](#funciones)
   
## Descripción

Este modulo continene las funciones relacionadas con el uso de la estrategia de interpolación por Kriging para determinar el impacto que tienen las zonas industriales, las areas verdes recreativas y los hospitales. Para determinar dicho impacto puntual sobre las localizaciones obtenidas por web screpping se emplearon varias tecnicas de estandarización de variables. Para despues usar un Regresor de Procesos Gaussianos con un kernel Cuadratico Racional.

Dichas estrategias se realizaron en el siguiente orden:
- Log-normalización con el desfase positivo de 1.
- Se aplico un ruido gaussiano de longitud del 15% de la media.
- Finalmente una estandarizacion z-normal.

## Funciones

```krigingInterpolation(gdf, filter, showplot=False, n = 300)```

**gdf**: dataframe de pandas con coordenadas geograficas y cantidad de coincidencias en un radio de 1km.

**filter**: nombre de la infraestructura a filtrar.

**show_plot**: Si se debe imprimir el mapa o no. Falso por defecto.

**n**: la cantidad de discretizacion de la malla de puntos

**```Return```**

**gp**: El regresor ya ajustado con los datos.

**gid_proints**: La malla de valores discrtizados.

**X**: las coordenadas de los puntos extraidos del dataframe.
