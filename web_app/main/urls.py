from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from predictor import urls as predictor_urls


urlpatterns = [
    path('', admin.site.urls),

    # path('', include(predictor_urls.urlpatterns)),
]
