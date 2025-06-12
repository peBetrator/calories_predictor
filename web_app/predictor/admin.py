import time

from django.contrib import admin, messages
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.urls import path, reverse_lazy
from django.utils.translation import gettext_lazy as _
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ImportForm, ExportForm
from unfold.contrib.filters.admin import (
    ChoicesCheckboxFilter,
    RangeNumericFilter,
)
from unfold.components import BaseComponent, register_component
from unfold.decorators import action
from unfold.enums import ActionVariant

from .enums import MlModel
from .models import CaloriesData, ExerciseData, TrainedModel, Forms
from .utils import ModelTrainer, get_cohort_dataset_data
from .views import PredictCaloriesView


class CaloriesDataResource(resources.ModelResource):
    user_id = fields.Field(attribute='user_id', column_name='User_ID')
    calories = fields.Field(attribute='calories', column_name='Calories')

    class Meta:
        model = CaloriesData
        skip_unchanged = True
        report_skipped = False
        fields = (
            'user_id',
            'calories',
        )
        import_id_fields = ('user_id',)


class ExerciseDataResource(resources.ModelResource):
    user_id = fields.Field(attribute='user_id', column_name='User_ID')
    gender = fields.Field(attribute='gender', column_name='Gender')
    age = fields.Field(attribute='age', column_name='Age')
    height = fields.Field(attribute='height', column_name='Height')
    weight = fields.Field(attribute='weight', column_name='Weight')
    duration = fields.Field(attribute='duration', column_name='Duration')
    heart_rate = fields.Field(attribute='heart_rate', column_name='Heart_Rate')
    body_temp = fields.Field(attribute='body_temp', column_name='Body_Temp')

    class Meta:
        model = ExerciseData
        skip_unchanged = True
        report_skipped = False
        fields = (
            'user_id',
            'gender',
            'age',
            'height',
            'weight',
            'duration',
            'heart_rate',
            'body_temp',
        )
        import_id_fields = ('user_id',)


@admin.register(CaloriesData)
class CaloriesDataAdmin(ModelAdmin, ImportExportModelAdmin):
    list_filter_sheet = False
    list_fullwidth = False

    list_display = (
        'user_id',
        'calories',
    )
    search_fields = ('user_id',)

    resource_classes = (CaloriesDataResource,)
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(ExerciseData)
class ExerciseDataAdmin(ModelAdmin, ImportExportModelAdmin):
    list_filter_sheet = False
    list_fullwidth = False

    list_display = (
        'user_id',
        'gender',
        'age',
        'height',
        'weight',
        'duration',
        'heart_rate',
        'body_temp',
    )
    list_filter = [
        ('gender', ChoicesCheckboxFilter),
        ('age', RangeNumericFilter),
        ('height', RangeNumericFilter),
        ('weight', RangeNumericFilter),
    ]
    list_filter_submit = True
    search_fields = ('user_id',)

    resource_classes = (ExerciseDataResource,)
    import_form_class = ImportForm
    export_form_class = ExportForm


@admin.register(TrainedModel)
class TrainedModelAdmin(ModelAdmin):
    list_filter_sheet = False
    list_fullwidth = False

    list_display = (
        'name',
        'mse',
        'r2',
        'updated_at',
    )

    actions_list = [
        {
            'title': _('Train Model'),
            'variant': ActionVariant.PRIMARY,
            'items': [
                'ml_model_1',
                'ml_model_2',
                'ml_model_3',
            ],
        },
    ]

    @action(description=MlModel.LINEAR_REGRESSION.label, icon='linear_scale')
    def ml_model_1(self, request):
        start = time.time()
        ModelTrainer(MlModel.LINEAR_REGRESSION.value).run()
        train_time = time.time() - start
        messages.success(request, _(f'The training of {MlModel.LINEAR_REGRESSION.label} model has been completed in {train_time:.2f} seconds'))
        return redirect(reverse_lazy('admin:predictor_trainedmodel_changelist'))

    @action(description=MlModel.RANDOM_FOREST.label, icon='forest')
    def ml_model_2(self, request):
        start = time.time()
        ModelTrainer(MlModel.RANDOM_FOREST.value).run()
        train_time = time.time() - start
        messages.success(request, _(f'The training of {MlModel.RANDOM_FOREST.label} model has been completed in {train_time:.2f} seconds'))
        return redirect(reverse_lazy('admin:predictor_trainedmodel_changelist'))

    @action(description=MlModel.XGBOOST.label, icon='speed')
    def ml_model_3(self, request):
        start = time.time()
        ModelTrainer(MlModel.XGBOOST.value).run()
        train_time = time.time() - start
        messages.success(request, _(f'The training of {MlModel.XGBOOST.label} model has been completed in {train_time:.2f} seconds'))
        return redirect(reverse_lazy('admin:predictor_trainedmodel_changelist'))

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@register_component
class CohortDatasetComponent(BaseComponent):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = get_cohort_dataset_data()
        return context


@admin.register(Forms)
class FormsAdmin(ModelAdmin):
    def get_urls(self):
        return super().get_urls() + [
            path(
                'predict-calories',
                self.admin_site.admin_view(PredictCaloriesView.as_view(model_admin=self)),
                name='predict_calories',
            ),
        ]
