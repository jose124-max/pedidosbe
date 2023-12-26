from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.db import transaction
from PIL import Image
import base64
from io import BytesIO
import json

from .models import Empresa

@method_decorator(csrf_exempt, name='dispatch')
class EmpresaDatosView(View):
    def post(self, request, *args, **kwargs):
        try:

            empresa = Empresa.objects.first()

            if empresa:
                if empresa.elogo:
                    img = Image.open(BytesIO(base64.b64decode(empresa.elogo)))
                    img = img.resize((500, 500))
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    elogo_base64_resized = base64.b64encode(buffered.getvalue()).decode('utf-8')
                else:
                    elogo_base64_resized = None
                empresa_info = {
                    'id_empresa': empresa.id_empresa,
                    'enombre': empresa.enombre,
                    'direccion': empresa.direccion,
                    'etelefono': empresa.etelefono,
                    'correoelectronico': empresa.correoelectronico,
                    'fechafundacion': empresa.fechafundacion,
                    'sitioweb': empresa.sitioweb,
                    'eslogan': empresa.eslogan,
                    'elogo':elogo_base64_resized,
                    'edescripcion':empresa.edescripcion,
                    'docmenu':empresa.docmenu

                }

                # Devuelve la información como respuesta JSON
                return JsonResponse({'mensaje': 'Datos de la empresa', 'empresa_info': empresa_info})
            else:
                return JsonResponse({'mensaje': 'No hay registros en la tabla Empresa'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)