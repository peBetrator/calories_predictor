import os
import joblib
from typing import Optional, Union, List, Dict, Any

import numpy as np
import pandas as pd
from django.conf import settings
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

from .models import CaloriesData, ExerciseData, TrainedModel
from .enums import MlModel


class ModelTrainer:
    MODEL_MAP = {
        MlModel.LINEAR_REGRESSION.value: LinearRegression,
        MlModel.RANDOM_FOREST.value: RandomForestRegressor,
        MlModel.XGBOOST.value: XGBRegressor,
    }

    def __init__(self, model_name: MlModel):
        self.model_name: MlModel = model_name
        self.model: Optional[Union[RandomForestRegressor, LinearRegression, XGBRegressor]] = None
        self.X: Optional[pd.DataFrame] = None
        self.y: Optional[Union[pd.Series, np.ndarray]] = None
        self.X_train: Optional[Union[pd.DataFrame, np.ndarray]] = None
        self.X_test: Optional[Union[pd.DataFrame, np.ndarray]] = None
        self.y_train: Optional[Union[pd.Series, np.ndarray]] = None
        self.y_test: Optional[Union[pd.Series, np.ndarray]] = None
        self.trained_model: Optional[TrainedModel] = None
        self.mse: Optional[float] = None
        self.r2: Optional[float] = None
        self.feature_importances: Optional[List[Dict[str, Any]]] = None
        self.model_path: str = f'models/{self.model_name}_model.pkl'

    def fetch_data(self):
        ex_df = pd.DataFrame(list(ExerciseData.objects.all().values()))
        cal_df = pd.DataFrame(list(CaloriesData.objects.all().values()))
        df = pd.merge(ex_df, cal_df, left_on='user_id', right_on='user_id')
        df['Gender_male'] = (df['gender'] == 'male').astype(int)
        self.X = df[['age', 'height', 'weight', 'duration', 'heart_rate', 'body_temp', 'Gender_male']]
        self.y = df['calories']

    def split_data(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )

    def build_model(self):
        match self.model_name:
            case MlModel.LINEAR_REGRESSION.value:
                self.model = self.MODEL_MAP[self.model_name]()
            case MlModel.RANDOM_FOREST.value:
                self.model = self.MODEL_MAP[self.model_name](random_state=42)
            case MlModel.XGBOOST.value:
                self.model = self.MODEL_MAP[self.model_name](objective='reg:squarederror', random_state=42)
            case _:
                raise ValueError(f'Unsupported model type: {self.model_name}')

    def train(self):
        self.model.fit(self.X_train, self.y_train)

    def evaluate(self):
        preds = self.model.predict(self.X_test)
        self.mse = mean_squared_error(self.y_test, preds)
        self.r2 = r2_score(self.y_test, preds)
        if hasattr(self.model, 'feature_importances_'):
            self.feature_importances = [
                {'feature': name, 'importance': float(imp)}
                for name, imp in zip(self.X.columns, self.model.feature_importances_)
            ]
        elif hasattr(self.model, 'coef_'):
            # For the linear regression model
            self.feature_importances = [
                {'feature': name, 'importance': float(abs(imp))}
                for name, imp in zip(self.X.columns, self.model.coef_)
            ]
        else:
            self.feature_importances = None

    def save_model(self):
        abs_path = os.path.join(settings.MEDIA_ROOT, self.model_path)
        os.makedirs(os.path.dirname(abs_path), exist_ok=True)
        joblib.dump(self.model, abs_path)

    def save_to_db(self):
        self.trained_model, _ = TrainedModel.objects.update_or_create(
            name=self.model_name,
            defaults={
                'file': self.model_path,
                'mse': self.mse,
                'r2': self.r2,
                'feature_importances': self.feature_importances,
            }
        )

    def run(self):
        self.fetch_data()
        self.split_data()
        self.build_model()
        self.train()
        self.evaluate()
        self.save_model()
        self.save_to_db()
        return self.trained_model
