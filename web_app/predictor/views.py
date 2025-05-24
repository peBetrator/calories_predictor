import json
import random

from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Count, Avg, Max
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from .enums import MlModel
from .models import CaloriesData, ExerciseData, TrainedModel


def dashboard_callback(request, context):
    context.update(chart_data())
    return context


def get_model_data():
    models = TrainedModel.objects.all()
    model_data = []
    for model in models:
        label = dict(MlModel.choices).get(model.name, model.name)
        metric = mark_safe(f"R²: {model.r2:.3f}<br> MSE: {model.mse:.3f}")
        footer = mark_safe(
            f'Last update &nbsp;<strong class="text-green-700 font-semibold dark:text-green-400">{model.updated_at:%d.%m.%Y %H:%M}</strong>'
        )
        model_data.append({
            "title": f"{label} model",
            "metric": metric,
            "footer": footer,
        })

    return model_data


def get_models_feature_importance():
    model_importance = {}
    models = TrainedModel.objects.all()
    for model in models:
        feats = model.feature_importances
        if not feats:
            continue
        max_importance = max([f["importance"] for f in feats]) or 1
        feats_list = []

        for feat in feats:
            feats_list.append({
                "title": feat["feature"].replace("_", " ").capitalize(),
                "description": f"Importance: {feat['importance']:.2f}",
                "value": int(feat["importance"] / max_importance * 100),
            })

        feats_list.sort(key=lambda x: x['value'], reverse=True)
        model_importance[model.get_name_display()] = feats_list

    return model_importance


def chart_data():
    WEEKDAYS = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]
    average = [r[1] - random.randint(3, 5) for r in positive]
    performance_positive = [[1, random.randrange(8, 28)] for i in range(1, 28)]
    performance_negative = [[-1, -random.randrange(8, 28)] for i in range(1, 28)]

    return {
        "model_data":get_model_data(),
        "model_importance": get_models_feature_importance(),
        "performance": [
            {
                "title": _("Last week revenue"),
                "metric": "$1,234.56",
                "footer": mark_safe(
                    '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                ),
                "chart": json.dumps(
                    {
                        "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                        "datasets": [
                            {
                                "data": performance_positive,
                                "borderColor": "var(--color-primary-700)",
                            }
                        ],
                    }
                ),
            },
            {
                "title": _("Last week expenses"),
                "metric": "$1,234.56",
                "footer": mark_safe(
                    '<strong class="text-green-600 font-medium">+3.14%</strong>&nbsp;progress from last week'
                ),
                "chart": json.dumps(
                    {
                        "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                        "datasets": [
                            {
                                "data": performance_negative,
                                "borderColor": "var(--color-primary-300)",
                            }
                        ],
                    }
                ),
            },
        ],
    }
