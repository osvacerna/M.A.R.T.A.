# lstm.py

## Tabla de Contenidos
- [lstm.py](#lstmpy)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Descripción](#descripción)
  - [Funciones](#funciones)
   
## Descripción

Este modulo continene las funciones relacionadas con el uso de una red neuronal basada en Long Short Term Memory para predecir el comportamiento de las temperaturas y precipitaciones. De hecho esto puede aplicarse a diferentes mediciones relacionadas a las anteriores (ej. las temperaturas maximas promedio mensuales, temperaturas minimas extremas mensuales, etc.)

Esto a partir de los datos obtenidos por la CONAGUA y diferentes centros de medición meteorologica en el país, cabe mencionar que los datos que no pudieron ser obtenidos se rellenaron a partir del promedio de los años anteriores en el mismo mes.

## Funciones

```splitSequenceInSteps(sequence, n_steps)```

Dada una secuencia temporal genera las series de tiempos a ```n_steps```.

```splitTrainingTest(sequence, n_steps, ratio=2)```

Dada una secuencia global genera la partición entre conjunto de entrenamiento y de prueba con una razon $ratio:1$, para posteriormente de ambos grupos retornar sus series de tiempos a ```n_steps```.

```parseSheet(excel_filename)```

Dada una ruta lee el excel obteniendo de cada hoja las secuencias globales de cada medida.

```createModel(input_size, output_size)```

Crea el modelo de LSTM capaz de admitir los tamaño de entrada y salida.

```train(data, n_steps, batch_size=16, epochs=100, verbose=0)```

Dado del diccionario con las series de tiempo globales de cada medición, el numero de pasos, el tamaño de lote para entrenar, el numero de epocas y si debe imprimirse el resultado de cada epoca o no, realiza lo siguiente:
- Genera las series de tiempo de entrenemiento y prueba.
- Además define y ajusta los algoritmos de escalamiento para mejorar el desempeño de la red. 
- Crea y entrena todos los modelos (uno para cada medición) de forma automatica. 
- Almacena los modelos en el disco duro en su extension *.h5* y *.keras*.
- Retorna los algoritmos de escalamiento, modelos, conjuntos de entrenamientos y prueba.

```predict(model, scaler, x)```

Funcion de predicción dado el modelo, la serie de tiempo y el factor de escalamiento.

```plot(name, y_test, y_pred)```

Funcion de comparación entre los valores de prueba y los de predicción. Además de calcular el error cuadratico medio y el arror cuadratico absoluto.