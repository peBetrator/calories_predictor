import os
import joblib

import numpy as np
from django.conf import settings
from django.views.generic import FormView
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .enums import MlModel
from .forms import CaloriesForm
from .models import TrainedModel


def dashboard_callback(request, context):
    context.update({
        'model_data':get_model_data(),
        'model_importance': get_models_feature_importance(),
    })
    return context


def get_model_data():
    models = TrainedModel.objects.all()
    model_data = []
    for model in models:
        label = dict(MlModel.choices).get(model.name, model.name)
        metric = mark_safe(f'R²: {model.r2:.3f}<br> MSE: {model.mse:.3f}')
        footer = mark_safe(
            f'Last update &nbsp;<strong class="text-green-700 font-semibold dark:text-green-400">{model.updated_at:%d.%m.%Y %H:%M}</strong>'
        )
        model_data.append({
            'title': f'{label} model',
            'metric': metric,
            'footer': footer,
        })

    return model_data


def get_models_feature_importance():
    model_importance = {}
    models = TrainedModel.objects.all()
    for model in models:
        feats = model.feature_importances
        if not feats:
            continue
        max_importance = max([f['importance'] for f in feats]) or 1
        feats_list = []

        for feat in feats:
            feats_list.append({
                'title': feat['feature'].replace('_', ' ').capitalize(),
                'description': f'Importance: {feat['importance']:.2f}',
                'value': int(feat['importance'] / max_importance * 100),
            })

        feats_list.sort(key=lambda x: x['value'], reverse=True)
        model_importance[model.get_name_display()] = feats_list

    return model_importance


def predict_xgboost(gender, age, height, weight, duration, heart_rate, body_temp):
    model_path = os.path.join(settings.MEDIA_ROOT, 'models/xgboost_model.pkl')
    model = joblib.load(model_path)

    X = np.array([[age, height, weight, duration, heart_rate, body_temp, gender]])
    y_pred = model.predict(X)
    return round(float(y_pred[0]), 1)


class PredictCaloriesView(FormView):
    template_name = 'predictor/predict_form.html'
    form_class = CaloriesForm
    success_url = reverse_lazy('predict_calories')

    def form_valid(self, form):
        data = form.cleaned_data
        gender_val = 1 if data['gender'] == 'male' else 0

        prediction = predict_xgboost(
            gender_val, data['age'], data['height'], data['weight'],
            data['duration'], data['heart_rate'], data['body_temp']
        )
        return self.render_to_response(
            self.get_context_data(form=form, prediction=prediction)
        )
