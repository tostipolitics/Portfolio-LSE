import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import (
    RobustScaler,
    OneHotEncoder,
    OrdinalEncoder,
    TargetEncoder
    )
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegressionCV
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer
from sklearn.ensemble import RandomForestRegressor

def my474_predict(X, fitted_object):
    """This function takes X independent variables to predict the probabilities of a binary outcome"""
    
    # Create a copy of the dataset
    X_transformed = X.copy()

    # Define variable types
    X_numeric = X_transformed.select_dtypes(include = "number").columns.tolist()
    X_categorical = X_transformed.select_dtypes(exclude = "number").columns.tolist()
    X_ordinal  = [
        'ideo5',
        'pew_religimp',
        'pew_churatd',
        'pew_prayer',
        'newsint'
        ]
    
    X_nominal = [col for col in X_categorical if col not in X_ordinal and col != 'inputstate']
    
    ordinal_categories = [
        ['Not sure', 'Very conservative', 'Conservative', 'Moderate', 'Liberal', 'Very liberal'],
        ['Very important', 'Somewhat important', 'Not at all important', 'Not too important'],
        ["Don't know", 'Never', 'Seldom', 'A few times a year', 'Once or twice a month', 'Once a week', 'More than once a week'],
        ["Don't know", 'Never', 'Seldom', 'A few times a month', 'Once a week', 'A few times a week', 'Once a day', 'Several times a day'],
        ["Don't know", 'Hardly at all', 'Only now and then', 'Some of the time', 'Most of the time']
        ]
    
    # Feature engineering part I
    ## Transform skweded columns
    log_cols = ['child18num']
    for col in log_cols:
        X_transformed[col] = np.log1p(X_transformed[col])
    
    ## add NA indicators
    for col in X_transformed.columns:
        if X_transformed[col].isna().any():
            X_transformed[col + '_is_na'] = X_transformed[col].isna().astype(int)
    
    ## recode NaN to "missing" for categorical columns
    for col in X_categorical:
        X_transformed[col] = X_transformed[col].fillna('missing')
    
    return fitted_object.predict_proba(X_transformed)[:, 1]