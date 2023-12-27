from django.urls import path
from .views import AvisosPrincipalesListView,CrearAviso

urlpatterns = [
    path('avisos/', AvisosPrincipalesListView.as_view(), name='avisos'),
    path('crear/', CrearAviso.as_view(), name='crearaviso'),
]