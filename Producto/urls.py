from django.urls import path
from .views import *

urlpatterns = [
    path('creartipop/', CrearTipoProducto.as_view(), name='creartipop'),
    path('crearcategoria/', CrearCategoria.as_view(), name='crearcategoria'),
    path('listatiposycategorias/', ListaTiposYCategorias.as_view(), name='lista_tipos_y_categorias'),
    path('editar_tipo_producto/<int:tipo_producto_id>/', EditarTipoProducto.as_view(), name='editar_tipo_producto'),
    path('editar_categoria/<int:categoria_id>/', EditarCategoria.as_view(), name='editar_categoria'),
    path('crearum/', CrearUnidadMedida.as_view(), name='crearum'),
    path('crearproducto/', CrearProducto.as_view(), name='crearproducto'),
    path('editarum/<int:unidad_id>/', EditarUnidadMedida.as_view(), name='editarum'),
    path('editarproducto/<int:producto_id>/', EditarProducto.as_view(), name='EditarProducto'),
    path('listar/', ListarProductos.as_view(), name='listar_productos'),
]
