import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RationalQuadratic

def plotKriging(gp, X, grid_points):
  y_pred, _ = gp.predict(grid_points, return_std=True)

  plt.figure(figsize=(8, 6))
  plt.tricontourf(grid_points[:, 0], grid_points[:, 1], y_pred, levels=100, cmap='viridis', alpha=0.5)
  plt.scatter(X[:, 0], X[:, 1], c='red', marker='.', label='Sitios Importantes')

  plt.colorbar(label='Valores Interpolados')
  plt.title('Interpolación de Kriging')
  plt.xlabel('X')
  plt.ylabel('Y')
  plt.legend()
  plt.show()

def krigingInterpolation(gdf, filter, showplot=False, n = 300):
  filtered_df = gdf[gdf["Tipo"] == filter]

  features = ['lon', 'lat', f'num_{filter}_en_1km']
  coordinates = np.array(filtered_df[features].values.tolist())

  coordinates[:,2] = np.log(coordinates[:,2] + 1)

  beta = np.mean(coordinates[:,2])
  noise = np.random.normal(loc=0, scale=0.15, size=len(coordinates))
  coordinates[:,2] = coordinates[:,2] + beta*noise

  mean = np.mean(coordinates[:,2])
  std = np.std(coordinates[:,2])
  coordinates[:,2] = (coordinates[:,2] - mean) / std

  X = coordinates[:, :2]
  y = coordinates[:, 2]

  x_min, x_max = X[:, 0].min(), X[:, 0].max()
  y_min, y_max = X[:, 1].min(), X[:, 1].max()

  grid_x = np.linspace(x_min, x_max, n)
  grid_y = np.linspace(y_min, y_max, n)
  grid_points = np.array(np.meshgrid(grid_x, grid_y)).T.reshape(-1, 2)
  kernel = RationalQuadratic(length_scale=0.0001, alpha=0.5, length_scale_bounds=(1e-10, 1e2))
  gp = GaussianProcessRegressor(kernel=kernel)
  gp.fit(X, y)

  if showplot:
    plotKriging(gp, X, grid_points)

  return gp, grid_points