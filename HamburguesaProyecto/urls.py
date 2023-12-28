from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Login/', include('Login.urls')),
    path('cliente/', include('Cliente.urls')),
    path('empresa/', include('Empresa.urls')),
    path('sucursal/', include('Sucursal.urls')),
    path('bodega/', include('Bodega.urls')),
    path('producto/', include('Producto.urls')),
    path('combos/', include('Combos.urls')),
    path('avisos/', include('avisos.urls')),
    path('empleado/', include('Empleados.urls')),
]

