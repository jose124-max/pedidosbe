import json 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Sucursales
import base64
from horariossemanales.models import Horariossemanales
from GeoSector.models import Geosectores
from Empresa.models import Empresa
from Ubicaciones.models import Ubicaciones
from django.utils.decorators import method_decorator 
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from Login.models import Cuenta
from io import BytesIO
from PIL import Image

class SucursalesListView(View):
    def get(self, request, *args, **kwargs):
        try:
            valor=0
            if request.user.is_authenticated:
                cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
                if cuenta.rol == 'S':
                    valor = 1
            sucursales = Sucursales.objects.all()
            sucursales_list = []
            for sucursal in sucursales:
                if sucursal.imagensucursal:
                    img = Image.open(BytesIO(base64.b64decode(sucursal.imagensucursal)))
                    img = img.resize((500, 500))
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    imagen_base64_resized = base64.b64encode(buffered.getvalue()).decode('utf-8')
                else:
                    imagen_base64_resized = None
                ubicacion_info = {
                    'id_ubicacion': sucursal.id_ubicacion.id_ubicacion if sucursal.id_ubicacion else None,
                    'latitud': sucursal.id_ubicacion.latitud if sucursal.id_ubicacion else None,
                    'longitud': sucursal.id_ubicacion.longitud if sucursal.id_ubicacion else None,
                    'udescripcion': sucursal.id_ubicacion.udescripcion if sucursal.id_ubicacion else None,
                }
                sucursal_info = {
                    'id_sucursal': sucursal.id_sucursal,
                    'srazon_social': sucursal.srazon_social,
                    'sruc': sucursal.sruc,
                    'sestado': sucursal.sestado,
                    'scapacidad': sucursal.scapacidad,
                    'scorreo': sucursal.scorreo,
                    'stelefono': sucursal.stelefono,
                    'sdireccion': sucursal.sdireccion,
                    'snombre': sucursal.snombre,
                    'fsapertura': sucursal.fsapertura.strftime('%Y-%m-%d') if sucursal.fsapertura else None,
                    'id_horarios': sucursal.id_horarios.id_horarios if hasattr(sucursal, 'id_horarios') else None,
                    'id_geosector': getattr(sucursal.id_geosector, 'id_geosector', None),
                    'firmaelectronica': sucursal.firmaelectronica,
                    'id_empresa': sucursal.id_empresa_id,
                    'id_ubicacion': ubicacion_info,
                    'id_cuenta':sucursal.id_cuenta.id_cuenta if valor==1 else None,
                    'imagensucursal': imagen_base64_resized,
                    
                }
                sucursales_list.append(sucursal_info)

            return JsonResponse({'sucursales': sucursales_list}, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class Crearsucursal(View):
    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
            if cuenta.rol != 'S':
                return JsonResponse({'error': 'No tienes permisos para crear una sucursal'}, status=403)
            data = json.loads(request.body)
            razon_social = data.get('razonsocial')
            ruc = data.get('sruc')
            capacidad=data.get('capacidad')
            correo= data.get('scorreo')
            telefono= data.get('ctelefono')
            direccion= data.get('sdireccion')
            nombre= data.get('snombre')
            id_horarios=  data.get('horario')
            idgeosector= data.get('geosectorid')
            firmaelectronica = data.get('firma')
            id_ubicacion = data.get('ubicacion')
            imagen= data.get('imagen')
            if imagen!= None:
                imagen_binaria = base64.b64decode(imagen)
            else:
                imagen_binaria=None

            sucursal_nueva  = Sucursales.objects.create(
                srazon_social=razon_social,
                sruc=ruc,
                sestado ='1',
                scapacidad = capacidad,
                scorreo =correo,
                stelefono=telefono,
                sdireccion=direccion,
                snombre=nombre,
                id_horarios=Horariossemanales.objects.create(**id_horarios) if id_horarios is not None else None,
                id_geosector=Geosectores.objects.create(**idgeosector) if idgeosector is not None else None,
                firmaelectronica=firmaelectronica,
                id_empresa=Empresa.objects.filter(id_empresa=1).first(),
                id_ubicacion=Ubicaciones.objects.create(**id_ubicacion) if id_ubicacion is not None else None,
                imagensucursal=imagen_binaria,
                id_cuenta=cuenta
            )
            return JsonResponse({'mensaje': 'Sucursal creada con éxito'});
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
