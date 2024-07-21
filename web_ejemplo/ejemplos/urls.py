
from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="index"),
    path('curso/<int:ini>', views.cursos, name="curso"),
    path('quienes_somos/', views.quienes_somos, name="quienes_somos"),

]
