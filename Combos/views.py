from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import transaction
from Login.models import Cuenta
from Producto.views import obtener_siguiente_codprincipal
import json

@method_decorator(csrf_exempt, name='dispatch')
class CrearCategoriaCombo(View):
    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
            if cuenta.rol != 'S':
                return JsonResponse({'error': 'No tienes permisos para crear una categoría de combo'}, status=403)
            
            data = json.loads(request.body)
            cat_nombre = data.get('cat_nombre')
            descripcion = data.get('descripcion')
            imagencategoria = data.get('imagencategoria')

            categoria_combo = CategoriasCombos.objects.create(catnombre=cat_nombre, descripcion=descripcion,imagencategoria=imagencategoria)
            categoria_combo.save()

            return JsonResponse({'mensaje': 'Categoría de combo creada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class CrearCombo(View):
    @method_decorator(login_required)
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
            if cuenta.rol != 'S':
                return JsonResponse({'error': 'No tienes permisos para crear un combo'}, status=403)

            data = json.loads(request.body)
            id_cat_combo = data.get('id_cat_combo')
            imagenc = data.get('imagen_c')
            puntos_cb = data.get('puntos_cb')
            nombre_cb = data.get('nombre_cb')
            descripcioncombo = data.get('descripcion_combo')
            preciounitario = data.get('precio_unitario')
            iva = data.get('iva')
            ice = data.get('ice')
            irbpnr = data.get('irbpnr')

            categoria_combo = CategoriasCombos.objects.get(id_catcombo=id_cat_combo)
            combo = Combo.objects.create(
                id_catcombo=categoria_combo,
                imagenc=imagenc,
                puntoscb=puntos_cb,
                codprincipal=obtener_siguiente_codprincipal(),
                nombrecb=nombre_cb,
                descripcioncombo=descripcioncombo,
                preciounitario=preciounitario,
                iva=iva,
                ice=ice,
                irbpnr=irbpnr
            )
            combo.save()

            return JsonResponse({'mensaje': 'Combo creado con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class EditarCombo(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            cuenta = Cuenta.objects.get(nombreusuario=request.user.username)
            if cuenta.rol != 'S':
                return JsonResponse({'error': 'No tienes permisos para editar un combo'}, status=403)

            combo_id = kwargs.get('combo_id')  # Asegúrate de tener la URL configurada para recibir el ID del combo
            combo = Combo.objects.get(id_combo=combo_id)
            combo.id_catcombo = CategoriasCombos.objects.get(id_catcombo=request.POST.get('id_catcombo', combo.id_catcombo.id_catcombo))
            combo.imagenc = request.POST.get('imagenc', combo.imagenc)
            combo.puntoscb = request.POST.get('puntoscb', combo.puntoscb)
            combo.nombrecb = request.POST.get('nombrecb', combo.nombrecb)
            combo.descripcioncombo = request.POST.get('descripcioncombo', combo.descripcioncombo)
            combo.preciounitario = request.POST.get('preciounitario', combo.preciounitario)
            combo.iva = request.POST.get('iva', combo.iva)
            combo.ice = request.POST.get('ice', combo.ice)
            combo.irbpnr = request.POST.get('irbpnr', combo.irbpnr)

            combo.save()

            return JsonResponse({'mensaje': 'Combo editado con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)