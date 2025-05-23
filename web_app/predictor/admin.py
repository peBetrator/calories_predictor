from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ImportForm, ExportForm
from unfold.contrib.filters.admin import (
    AllValuesCheckboxFilter,
    AutocompleteSelectMultipleFilter,
    BooleanRadioFilter,
    CheckboxFilter,
    ChoicesCheckboxFilter,
    RangeDateFilter,
    RangeDateTimeFilter,
    RangeNumericFilter,
    RelatedCheckboxFilter,
    RelatedDropdownFilter,
    SingleNumericFilter,
    TextFilter,
)

from .models import CaloriesData, ExerciseData


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
    list_fullwidth = True

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
    list_fullwidth = True

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
