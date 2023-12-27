from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import AvisosPrincipales
from Login.models import Cuenta
from Empresa.models import Empresa
import io
from django.db import transaction
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from PIL import Image, UnidentifiedImageError
from django.core.files.base import ContentFile
import base64
import json
from io import BytesIO

@method_decorator(csrf_exempt, name='dispatch')
class AvisosPrincipalesListView(View):
    def get(self, request, *args, **kwargs):
        try:
            avisos_principales = AvisosPrincipales.objects.all()
            avisos_list = []
            for aviso in avisos_principales:
                if aviso.imagen:
                    try:
                        # Decodificar la imagen base64
                        byteImg = base64.b64decode(aviso.imagen)

                        # Convertir los bytes a una cadena base64
                        imagen_base64 = base64.b64encode(byteImg).decode('utf-8')

                        # Crear un diccionario con la información del aviso
                        aviso_info = {
                            'id_aviso': aviso.id_aviso,
                            'id_empresa': aviso.id_empresa.id_empresa if aviso.id_empresa else None,
                            'titulo': aviso.titulo,
                            'descripcion': aviso.descripcion,
                            'imagen': imagen_base64,
                        }
                        avisos_list.append(aviso_info)
                    except Exception as img_error:
                        # Puedes imprimir o loggear el error para investigar más
                        print(f"Error al procesar imagen: {str(img_error)}")
                else:
                    aviso_info = {
                        'id_aviso': aviso.id_aviso,
                        'id_empresa': aviso.id_empresa.id_empresa if aviso.id_empresa else None,
                        'titulo': aviso.titulo,
                        'descripcion': aviso.descripcion,
                        'imagen': None,
                    }
                    avisos_list.append(aviso_info)

            return JsonResponse({'avisos_principales': avisos_list}, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
@method_decorator(csrf_exempt, name='dispatch')
class CrearAviso(View):
    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
            if cuenta.rol != 'S':
                return JsonResponse({'error': 'No tienes permisos para crear un aviso'}, status=403)

            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')

            # Recibir la imagen como FormData
            imagen_archivo = request.FILES.get('imagen')

            # Verificar que se ha enviado una imagen
            if imagen_archivo:
                # Leer y procesar la imagen
                try:
                    image = Image.open(imagen_archivo)
                    # Puedes realizar cualquier procesamiento adicional aquí si es necesario

                    # Convertir la imagen a bytes
                    byte_io = BytesIO()
                    image.save(byte_io, format="PNG")
                    byte_img = byte_io.getvalue()

                    # Guardar la imagen en el modelo
                    aviso_nuevo = AvisosPrincipales.objects.create(
                        id_empresa=Empresa.objects.filter(id_empresa=1).first(),
                        titulo=titulo,
                        descripcion=descripcion,
                        imagen=byte_img
                    )

                    return JsonResponse({'mensaje': 'Aviso creado con éxito'})
                except UnidentifiedImageError as img_error:
                    return JsonResponse({'error': f"Error al procesar imagen: {str(img_error)}"}, status=400)
            else:
                return JsonResponse({'error': 'No se proporcionó ninguna imagen'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)