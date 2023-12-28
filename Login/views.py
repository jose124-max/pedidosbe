from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.db import transaction
import json
from .models import Cuenta, Clientes
from django.contrib.auth.hashers import make_password, check_password
from Administrador.models import Administrador

@method_decorator(csrf_exempt, name='dispatch')
class CrearUsuarioView(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            nombre_usuario = data.get('nombreusuario')
            contrasenia = data.get('contrasenia')
            ctelefono = data.get('ctelefono')
            razons= data.get('crazon_social')
            telefono=data.get('ctelefono')
            tipocliente= data.get('tipocliente')
            snombre=data.get('snombre')
            capellido=data.get('capellido')
            ruc_cedula= data.get('ruc_cedula')
            correorecuperacion=data.get('correorecuperacion')
            ubicacion=data.get('ubicacion')

            user = User.objects.create_user(username=nombre_usuario, password=contrasenia)


            cuenta_nueva  = Cuenta.objects.create(
                nombreusuario=nombre_usuario,
                contrasenia= make_password(contrasenia),
                estadocuenta ='1',
                rol = 'C',
                correorecuperacion =correorecuperacion
            )

            # Crear un nuevo cliente asociado al usuario y la cuenta
            cliente_nuevo  = Clientes.objects.create(
                ctelefono=ctelefono,
                id_cuenta=cuenta_nueva,
                crazon_social = razons,
                tipocliente = tipocliente,
                snombre = snombre,
                capellido = capellido,
                ruc_cedula = ruc_cedula,
                ccorreo_electronico = correorecuperacion,
                ubicacion = ubicacion
            )
        

            return JsonResponse({'mensaje': 'Usuario creado con éxito'})
        
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class IniciarSesionView(View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            nombre_usuario = data.get('nombreusuario')
            contrasenia = data.get('contrasenia')
            


            # Autenticar al usuario
            user = authenticate(username=nombre_usuario, password=contrasenia)

            if user is not None:
                # Iniciar sesión y guardar información en la sesión del usuario
                login(request, user)

                # Verificar si la contraseña es correcta
                if user.check_password(contrasenia):
                    # Obtener la cuenta asociada al usuario
                    cuenta = Cuenta.objects.filter(nombreusuario=user.username).first()

                    if cuenta:
                        # Definir el diccionario de funciones según el rol
                        rol_actions = {
                            'C': self.handle_cliente,
                            'A': self.handle_administrador,
                            'X': self.handle_jefecocina,
                            'M': self.handle_mesero,
                            'D': self.handle_motorizado,
                            'S': self.handle_administrador,
                        }

                        # Obtener la función correspondiente al rol
                        action_func = rol_actions.get(cuenta.rol, self.handle_default)

                        # Ejecutar la función correspondiente
                        return action_func(cuenta)

                    else:
                        return JsonResponse({'mensaje': 'La cuenta asociada al usuario no tiene información'}, status=404)

                else:
                    return JsonResponse({'mensaje': 'Contraseña incorrecta'}, status=401)
            else:
                return JsonResponse({'mensaje': 'Credenciales incorrectas'}, status=401)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    def handle_cliente(self, cuenta):
        cliente = Clientes.objects.filter(id_cuenta=cuenta.id_cuenta).first()

        cliente_info = {
            'id_cliente' : cliente.id_cliente,
            'username':cliente.id_cuenta.nombreusuario,
            'razon_social': cliente.crazon_social,
            'telefono': cliente.ctelefono,
            'tipo_cliente': cliente.tipocliente,
            'nombre': cliente.snombre,
            'apellido': cliente.capellido,
            'puntos': cliente.cpuntos,
            'correo_electronico': cliente.ccorreo_electronico,
            'ubicacion': cliente.ubicacion,
            'fecha_registro':cliente.cregistro,
            'ruc_cedula':cliente.ruc_cedula,
            'id_cuenta':cliente.id_cuenta.id_cuenta,
            'ubicacion1': cliente.id_ubicacion1 if hasattr(cliente, 'id_ubicacion1') else None,
            'ubicacion2': cliente.id_ubicacion2 if hasattr(cliente, 'id_ubicacion2') else None,
            'ubicacion3': cliente.id_ubicacion3 if hasattr(cliente, 'id_ubicacion3') else None,
        }

        return JsonResponse({'mensaje': 'Inicio de sesión exitoso', 'cliente_info': cliente_info})
    def handle_administrador(self, cuenta):
        administrador = Administrador.objects.filter(id_cuenta=cuenta.id_cuenta).first()
        administrador_info = {
            'id_administrador':administrador.id_administrador,
            'telefono':administrador.telefono,
            'apellido':administrador.apellido,
            'nombre':administrador.nombre,
            'id_cuenta':administrador.id_cuenta.id_cuenta,
            'id_sucursal':administrador.id_sucursal if hasattr(administrador, 'id_sucursal') else None
        }
        return JsonResponse({'mensaje': 'Inicio de sesión exitoso como Administrador','administrador_info':administrador_info})
    def handle_jefecocina(self, cuenta):
        # Realiza acciones específicas para el rol de Administrador
        return JsonResponse({'mensaje': 'Inicio de sesión exitoso como Administrador'})
    def handle_mesero(self, cuenta):
        # Realiza acciones específicas para el rol de Administrador
        return JsonResponse({'mensaje': 'Inicio de sesión exitoso como Administrador'})
    def handle_motorizado(self, cuenta):
        # Realiza acciones específicas para el rol de Administrador
        return JsonResponse({'mensaje': 'Inicio de sesión exitoso como Administrador'})
    def handle_default(self, cuenta):
        return JsonResponse({'mensaje': 'Rol no reconocido'}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class CerrarSesionView(View):
    def post(self, request, *args, **kwargs):
        try:
            logout(request)
            return JsonResponse({'mensaje': 'Sesión cerrada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class EditarCliente(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            cuenta = Cuenta.objects.filter(nombreusuario=request.user.username).first()
            # Obtener datos del cliente a actualizar
            cliente_id = Clientes.objects.filter(id_cuenta=cuenta.id_cuenta).first().id_cliente  # Asegúrate de tener la URL configurada para recibir el ID del cliente

            # Obtener cliente existente
            cliente = Clientes.objects.get(id_cliente=cliente_id)

            # Actualizar solo los campos permitidos
            cliente.crazon_social = request.POST.get('crazon_social', cliente.crazon_social)
            cliente.ctelefono = request.POST.get('ctelefono', cliente.ctelefono)
            cliente.tipocliente = request.POST.get('tipocliente', cliente.tipocliente)
            cliente.snombre = request.POST.get('snombre', cliente.snombre)
            cliente.capellido = request.POST.get('capellido', cliente.capellido)
            cliente.ruc_cedula = request.POST.get('ruc_cedula', cliente.ruc_cedula)
            cliente.ccorreo_electronico = request.POST.get('ccorreo_electronico', cliente.ccorreo_electronico)
            cliente.ubicacion = request.POST.get('ubicacion', cliente.ubicacion)

            # Guardar el cliente actualizado
            cliente.save()

            return JsonResponse({'mensaje': 'Cliente editado con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
