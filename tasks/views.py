from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import User, Task
from django.contrib import messages



def register_view(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validar que las contraseñas coinciden
        if password != confirm_password:
            messages.error(request, 'Las contraseñas no coinciden.')
        else:
            # Comprobar si el correo ya está registrado
            if User.objects.filter(correo=correo).exists():
                messages.error(request, 'El correo ya está registrado.')
            else:
                # Crear y guardar el usuario sin encriptar la contraseña
                user = User(nombre=nombre, correo=correo, password=password)  # Guardar la contraseña tal cual
                user.save()

                # Autenticar y loguear al usuario
                user = authenticate(request, correo=correo, password=password)
                if user is not None:
                    login(request, user)

                messages.success(request, '¡Te has registrado exitosamente!')
                return redirect('seccion')  # Redirige a la página principal o donde lo necesites

    return render(request, 'registroV.html')


def inicio_seccion(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']
        
        # Validar las credenciales
        user = authenticate(request, correo=correo, password=password)
        if user is not None:
            login(request, user)
            return redirect('crear')  
        else:
            messages.error(request, "Correo o contraseña incorrectos.")
    
    return render(request, 'registro.html')






@login_required
def create_task(request):
    if request.method == 'POST':
        # Obtenemos los datos del formulario manualmente
        title = request.POST.get('title')
        description = request.POST.get('description')
        completed = 'completed' in request.POST  # Si el checkbox está marcado, se considera True

        # Verificamos que los datos necesarios existan
        if title and description:
            task = Task.objects.create(
                title=title,
                description=description,
                completed=completed,
                user=request.user  # Asociamos la tarea con el usuario autenticado
            )
            return redirect('task_list')  # Redirigimos a la lista de tareas

    return render(request, 'tarea.html')


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)  # Solo las tareas del usuario autenticado
    return render(request, 'lista.html', {'tasks': tasks})