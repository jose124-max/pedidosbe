from django.urls import path
from .views import CrearUsuarioView, IniciarSesionView,CerrarSesionView,EditarCliente

urlpatterns = [
    path('cerrar_sesion/', CerrarSesionView.as_view(), name='cerrar_sesion'),
    path('crear/', CrearUsuarioView.as_view(), name='crear_usuario'),
    path('iniciar_sesion/', IniciarSesionView.as_view(), name='iniciar_sesion'),
    path('editar_perfil/', EditarCliente.as_view(), name='editar_perfil'),
]