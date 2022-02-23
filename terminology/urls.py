from django.urls import path, register_converter

from . import views, converters

register_converter(converters.MyDateConverter, 'my_date')

urlpatterns = [
    path('spravochniks/', views.SpravochnikList.as_view()),
    path('spravochniks-actual/<my_date:date>', views.SpravochnikListActual.as_view()),
    path('elements-by-version/', views.ElementsByVersion.as_view()),
    path('elements-validation/', views.ElementValidation.as_view()),
]
