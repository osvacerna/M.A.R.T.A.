import pandas as pd
import numpy as np

import matplotlib.pyplot as plt

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

from keras.models import Sequential # type: ignore
from keras.layers import LSTM, Dense, Input # type: ignore

from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential # type: ignore
from keras.layers import LSTM, Dense, Input # type: ignore

import unicodedata

def rmvAccent(texto):
    norm = unicodedata.normalize('NFKD', texto.lower())
    return ''.join(char for char in norm if unicodedata.category(char) != 'Mn')

def splitSequenceInSteps(sequence, n_steps):
    X, y = list(), list()
    for i in range(len(sequence)):
        end_ix = i + n_steps
        if end_ix > len(sequence)-1:
            break
        seq_x, seq_y = sequence[i:end_ix], sequence[end_ix]
        X.append(seq_x)
        y.append(seq_y)
    return np.array(X), np.array(y)

def splitTrainingTest(sequence, n_steps, ratio=2):
    index = int(ratio*len(sequence)/(ratio+1))
    training_data = sequence[:index]
    test_data = sequence[index:]

    return splitSequenceInSteps(training_data, n_steps), splitSequenceInSteps(test_data, n_steps)

def parseSheet(excel_filename):
  excel_file = pd.ExcelFile(excel_filename)
  sheetnames = excel_file.sheet_names
  data = {}

  for name in sheetnames:
    df = pd.read_excel(excel_filename, sheet_name=name)

    df.set_index(df.columns[0], inplace=True)
    arr = np.array(df.iloc[:-4, :12].values.flatten())
    for i in range(len(arr)):
      if np.isnan(arr[i]):
        same_month = np.arange(i%12, i, 12)
        arr[i] = np.mean(arr[same_month])

    data[rmvAccent(name)] = arr

  return data

def createModel(input_size, output_size):
    model = Sequential()

    model.add(Input(shape=input_size))
    model.add(LSTM(32, activation = 'relu', return_sequences=False))
    model.add(Dense(16, activation = 'relu'))
    model.add(Dense(output_size))

    model.compile(optimizer='adam', loss='mae')
    model.summary()

    return model

def train(data, n_steps, batch_size=16, epochs=100, verbose=0):
    data, scalers, models = {}, {}, {}
    X_training, y_training = {}, {}
    X_test, y_test = {}, {}

    for name in data.keys():
        print(f"--{name.upper()}--")
        scaler = MinMaxScaler()
        data[name] = scaler.fit_transform(data[name].reshape(-1, 1)).reshape(-1,1)
        
        training, test = splitTrainingTest(data[name], n_steps)
        X_training[name], y_training[name] = training
        X_test[name], y_test[name] = test

        model = createModel(X_training.shape[1:], 1)
        model.fit(X_training, y_training, batch_size=batch_size, 
                  epochs=epochs, verbose=verbose)

        models[name] = model
        scalers[name] = scaler
        
        model.save(f'{name}.keras')
        model.save(f'{name}.h5')

    return scalers, models, (X_training, y_training), (X_test, y_test)

def predict(model, scaler, x):
    return scaler.inverse_transform(model.predict(x).reshape(-1, 1))

def plot(name, y_test, y_pred):
    print(f"--{name.upper()}--")

    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print("MSE:", mse)
    print("MAE:", mae)

    plt.figure(figsize=(14, 7))
    plt.plot(y_test, label='Valores Reales', linestyle='-', marker='.')
    plt.plot(y_pred, label='Valores Predichos', linestyle='-', marker='*')

    plt.xlabel('Índice')
    plt.ylabel('Clases')

    plt.title(f'{name.upper()}')
    plt.legend()

    plt.show()