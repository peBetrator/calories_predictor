from django.db import models

from .enums import Gender


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
