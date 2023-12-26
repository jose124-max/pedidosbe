from django.urls import path
from .views import EmpresaDatosView

urlpatterns = [
    path('infoEmpresa/', EmpresaDatosView.as_view(), name='Empresa_datos'),
]