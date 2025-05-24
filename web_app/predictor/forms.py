from django import forms

from .enums import Gender


class CaloriesForm(forms.Form):
    gender = forms.ChoiceField(choices=Gender.choices, widget=forms.RadioSelect, initial='male')
    age = forms.IntegerField(min_value=1, max_value=120)
    height = forms.FloatField(label='Height (cm)', min_value=30)
    weight = forms.FloatField(label='Weight (kg)', min_value=10)
    duration = forms.IntegerField(label='Duration (min)', min_value=1)
    heart_rate = forms.IntegerField(label='Heart Rate (bpm)', min_value=10)
    body_temp = forms.FloatField(label='Body Temp (°C)', min_value=30, max_value=45, initial=37.0)
