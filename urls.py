from django.urls import path
from . import views

urlpatterns = [
    path("index", views.index),
    path("paint", views.calculate_wall_paint),
    path("flooring", views.calc_flooring),
    path("plaster", views.calc_plaster),
]