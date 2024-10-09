from geopy.distance import geodesic
import matplotlib.pyplot as plt
import numpy as np
import os.path
import pandas as pd
import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RationalQuadratic
from sklearn.preprocessing import MinMaxScaler
import json

def getMapsAPIkey():
    with open('APIS.json', 'r') as file:
        data = json.load(file)
    return data.get('GoogleMaps')

def getGenLanModAPIkey():
    with open('APIS.json', 'r') as file:
        data = json.load(file)
    return data.get('GoogleGenLanMod')

def calcular_distancia_mas_cercana(lat, lon):
    df = pd.read_csv('datasets/Coords_Estaciones_de_Monitoreo_AGUA_gto.csv')
    
    punto_seleccionado = (lat, lon)
    
    distancias = df.apply(lambda row: geodesic(punto_seleccionado, (row['LATITUD'], row['LONGITUD'])).km, axis=1)
    sitio_mas_cercano = df.loc[distancias.idxmin()]
    
    return distancias.min(), sitio_mas_cercano['SITIO'], (sitio_mas_cercano['LATITUD'], sitio_mas_cercano['LONGITUD'])

def plotKriging(gp, X, grid_points):
  y_pred, sigma = gp.predict(grid_points, return_std=True)

  plt.figure(figsize=(8, 6))
  plt.tricontourf(grid_points[:, 0], grid_points[:, 1], y_pred, levels=100, cmap='viridis', alpha=0.5)
  plt.scatter(X[:, 0], X[:, 1], c='red', marker='.', label='Sitios Importantes')

  plt.colorbar(label='Valores Interpolados')
  plt.title('Interpolación de Kriging usando scikit-learn')
  plt.xlabel('X')
  plt.ylabel('Y')
  plt.legend()
  plt.show()

def krigingInterpolacion(gdf, filter, showplot=False):
    
    filtered_df = gdf[gdf["Tipo"] == filter]

    features = ['lon', 'lat', f'num_{filter}_en_1km']
    coordinates = np.array(filtered_df[features].values.tolist())

    noise = np.random.normal(loc=0, scale=0.15, size=len(coordinates))

    # Estandarizar el vector
    coordinates[:,2] = np.log(coordinates[:,2] + 1)
    mean = np.mean(coordinates[:,2])
    coordinates[:,2] = coordinates[:,2] + mean*noise
    mean = np.mean(coordinates[:,2])
    std = np.std(coordinates[:,2])
    coordinates[:,2] = (coordinates[:,2] - mean) / std

    X = coordinates[:, :2]  # lon, lat
    y = coordinates[:, 2]   # valor de la variable dependiente

    n = 300
    x_min, x_max = X[:, 0].min(), X[:, 0].max()
    y_min, y_max = X[:, 1].min(), X[:, 1].max()

    grid_x = np.linspace(x_min, x_max, n)
    grid_y = np.linspace(y_min, y_max, n)
    grid_points = np.array(np.meshgrid(grid_x, grid_y)).T.reshape(-1, 2)

    scale = 0.0001
    kernel = RationalQuadratic(length_scale=scale, alpha=0.5, length_scale_bounds=(1e-10, 1e2))
    gp = GaussianProcessRegressor(kernel=kernel)
    gp.fit(X, y)

    if showplot:
        plotKriging(gp, X, grid_points)

    return gp, grid_points, X, y, x_min, x_max, y_min, y_max  # Retornar también x_min, x_max, y_min, y_max

def krigginBase(gp, grid_points, X, y, x_min, x_max, y_min, y_max, name1, name2):
    # Usar el renderizador para abrir el gráfico en el navegador
    pio.renderers.default = 'browser'

    # Normalizar los valores de y para que estén en el rango [1, 10]
    scaler = MinMaxScaler(feature_range=(1, 10))  # Ajusta los valores para evitar el log(0)
    y_scaled = scaler.fit_transform(y.reshape(-1, 1)).ravel()

    # Entrenar el modelo con los valores escalados
    gp.fit(X, y_scaled)

    # Predecir los valores escalados
    y_pred_scaled, sigma = gp.predict(grid_points, return_std=True)

    # Invertir la escala para obtener los valores originales
    y_pred = scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).ravel()

    # Limitar los valores predichos a un rango de 0 a 1
    y_pred = np.clip(y_pred, 0, 1)

    # Crear el subplot con mapa
    fig = make_subplots(rows=1, cols=1, specs=[[{'type': 'scattermapbox'}]])

    # Convertir las coordenadas de la malla a lon y lat para el mapa
    grid_lon = grid_points[:, 0]
    grid_lat = grid_points[:, 1]

    # Añadir la densidad basada en la interpolación (valores predichos limitados a [0, 1])
    fig.add_trace(go.Densitymapbox(lat=grid_lat, lon=grid_lon, z=y_pred,
                                colorscale='Jet', showscale=True, radius=10,
                                zmin=0, zmax=1,  # Establecer el rango de colores
                                hovertemplate='%{z:.2f} unidades interpoladas',
                                name=name1), row=1, col=1)

    # Añadir los puntos originales de los datos
    fig.add_trace(go.Scattermapbox(lat=X[:, 1], lon=X[:, 0], mode='markers',
                                marker=dict(color='violet', size=8),
                                text=y, hovertemplate='%{text:.2f} unidades',
                                name=name2), row=1, col=1)

    # Configurar el mapa
    fig.update_layout(mapbox=dict(style='open-street-map', zoom=10,
                                center=dict(lat=np.mean([y_min, y_max]),
                                            lon=np.mean([x_min, x_max]))),
                    title='Interpolación de Kriging en Mapa',
                    margin=dict(l=20, r=20, t=80, b=20))

    return fig

def kriggingHospitales():
    filepath = 'static/kriggingHospitales.html'
    if not os.path.isfile(filepath):
        path = 'datasets/infraestructuras_con_conteo.csv'
        gdf = pd.read_csv(path)
        gp, grid_points, X, y, x_min, x_max, y_min, y_max = krigingInterpolacion(gdf, 'hospitales', showplot=False)
        fig = krigginBase(gp, grid_points, X, y, x_min, x_max, y_min, y_max, name1='Densidad Hospitalaria', name2='Puntos Hospitales')
        pio.write_html(fig, file=filepath, auto_open=False)
    
def kriggingIndustrial():
    filepath = 'static/kriggingIndustrial.html'
    if not os.path.isfile(filepath):
        path = 'datasets/infraestructuras_con_conteo.csv'
        gdf = pd.read_csv(path)
        gp, grid_points, X, y, x_min, x_max, y_min, y_max = krigingInterpolacion(gdf, 'Industrial', showplot=False)
        fig = krigginBase(gp, grid_points, X, y, x_min, x_max, y_min, y_max, name1='Densidad Industrial', name2='Puntos Industriales')
        pio.write_html(fig, file=filepath, auto_open=False)


def kriggingParques():
    filepath = 'static/kriggingParques.html'
    if not os.path.isfile(filepath):
        path = 'datasets/infraestructuras_con_conteo.csv'
        gdf = pd.read_csv(path)
        gp, grid_points, X, y, x_min, x_max, y_min, y_max = krigingInterpolacion(gdf, 'parks', showplot=False)
        fig = krigginBase(gp, grid_points, X, y, x_min, x_max, y_min, y_max, name1='Densidad de Parques', name2='Puntos de Parques')
        pio.write_html(fig, file=filepath, auto_open=False)
