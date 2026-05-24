import pickle
import pandas as pd # type: ignore
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler

def my474_predict(X, model):
      scaler = StandardScaler()
      X_scaled = scaler.fit_transform(X)
      return model.predict(X_scaled)