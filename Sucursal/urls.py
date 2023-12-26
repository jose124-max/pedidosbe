from django.urls import path
from .views import SucursalesListView, Crearsucursal

urlpatterns = [
    path('sucusarleslist/', SucursalesListView.as_view(), name='SucursalesListView'),
    path('crear/', Crearsucursal.as_view(), name='Crearsucursal')
]