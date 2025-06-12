from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Fieldset, Row, Column, BaseInput
from django import forms
from django.utils.translation import gettext_lazy as _
from unfold.layout import Submit, ButtonClassesMixin
from unfold.widgets import (
    UnfoldAdminIntegerFieldWidget,
    UnfoldAdminRadioSelectWidget,
    UnfoldAdminSelectWidget,
)

from .enums import Gender, MlModel


class Reset(ButtonClassesMixin, BaseInput):
    input_type = 'reset'


class CaloriesForm(forms.Form):
    model = forms.ChoiceField(
        label='ML Model',
        choices=MlModel.choices,
        widget=UnfoldAdminSelectWidget(),
        required=True,
    )
    gender = forms.ChoiceField(
        choices=Gender.choices,
        initial='male',
        widget=UnfoldAdminRadioSelectWidget(),
        required=True,
    )
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        widget=UnfoldAdminIntegerFieldWidget(),
        required=True,
    )
    height = forms.FloatField(
        label='Height (cm)',
        min_value=30,
        widget=UnfoldAdminIntegerFieldWidget(),
        required=True,
    )
    weight = forms.FloatField(
        label='Weight (kg)',
        min_value=10,
        widget=UnfoldAdminIntegerFieldWidget(),
        required=True,
    )
    duration = forms.IntegerField(
        label='Duration (min)',
        min_value=1,
        widget=UnfoldAdminIntegerFieldWidget(),
        required=True,
    )
    heart_rate = forms.IntegerField(
        label='Heart Rate (bpm)',
        min_value=10,
        widget=UnfoldAdminIntegerFieldWidget(),
        required=True,
    )
    body_temp = forms.FloatField(
        label='Body Temp (°C)',
        min_value=30,
        max_value=45,
        initial=37.0,
        widget=UnfoldAdminIntegerFieldWidget(),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h2 class="text-2xl font-semibold mb-6">Calculate predicted calories</h2>'),
            Row(
                Column(
                    Fieldset(None, 'model'),
                    css_class='lg:w-1/2',
                ),
                Column(
                    css_class='lg:w-1/2',
                ),
                css_class='mb-8',
            ),
            Row(
                Column(
                    Fieldset('Your Data',
                        'age',
                        'height',
                        'weight',
                        'gender',
                    ),
                    css_class='lg:w-1/2',
                ),
                Column(
                    Fieldset('Exercise',
                        'duration',
                        'heart_rate',
                        'body_temp',
                    ),
                    css_class='lg:w-1/2',
                ),
                css_class='mb-8',
            ),
        )
        self.helper.add_input(Reset('reset', _('Clear')))
        self.helper.add_input(Submit('submit', _('Predict')))
