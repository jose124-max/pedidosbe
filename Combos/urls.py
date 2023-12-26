from django.urls import path
from .views import CrearCategoriaCombo,CrearCombo,EditarCombo

urlpatterns = [
    path('crearcat/', CrearCategoriaCombo.as_view(), name='crearcatcombo'),
    path('crearcombo/', CrearCombo.as_view(), name='crearcatcombo'),
    path('editarcombo/<int:combo_id>/', EditarCombo.as_view(), name='editarcombo'),
]
