from django.db import models

from .enums import Gender, MlModel


class CaloriesData(models.Model):
    user_id = models.BigIntegerField()
    calories = models.FloatField()

    def __str__(self):
        return f'User {self.user_id}: {self.calories} kcal'

    class Meta:
        verbose_name = 'Calories Data'
        verbose_name_plural = 'Calories Data'


class ExerciseData(models.Model):
    user_id = models.BigIntegerField()
    gender = models.CharField(choices=Gender.choices, max_length=10)
    age = models.PositiveIntegerField()
    height = models.FloatField(help_text='Height in cm')
    weight = models.FloatField(help_text='Weight in kg')
    duration = models.FloatField(help_text='Duration in minutes')
    heart_rate = models.FloatField()
    body_temp = models.FloatField(help_text='Body temperature in °C')

    def __str__(self):
        return f'User {self.user_id}: {self.gender}, {self.age} yrs'

    class Meta:
        verbose_name = 'Exercise Data'
        verbose_name_plural = 'Exercise Data'


class TrainedModel(models.Model):
    name = models.CharField(choices=MlModel.choices, max_length=20, unique=True)
    file = models.FileField(upload_to='models/')
    mse = models.FloatField(null=True, blank=True)
    r2 = models.FloatField(null=True, blank=True)
    feature_importances = models.JSONField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Forms(models.Model):
    pass
