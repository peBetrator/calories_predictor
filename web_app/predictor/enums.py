from django.db.models import TextChoices


class Gender(TextChoices):
    MALE = 'male', 'Male'
    FEMALE = 'female', 'Female'


class MlModel(TextChoices):
    LINEAR_REGRESSION = 'linear_regression', 'Linear Regression'
    RANDOM_FOREST = 'random_forest', 'Random Forest'
    XGBOOST = 'xgboost', 'XGBoost'
    LIGHTGBM = 'lightgbm', 'LightGBM'
