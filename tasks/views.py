from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib import messages
from .models import persona, Task


def register_view(request):
    # Registro de usuarios nuevos
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Guardar un nuevo usuario en la base de datos
        persona.objects.create(
            nombre=nombre,
            correo=correo,
            password=confirm_password
        )
        messages.success(request, '¡Te has registrado exitosamente!')
        return redirect('seccion')  # Redirige al inicio de sesión
    return render(request, 'registroV.html')


def iniciar_sesion(request):
    # Inicio de sesión
    if request.method == 'POST':
        correo = request.POST.get('correo', '')
        password = request.POST.get('password', '')

        # Buscar el usuario en la base de datos
        persona_obj = persona.objects.filter(correo=correo, password=password).first()

        if persona_obj:
            # Redirige a la lista de tareas si las credenciales son válidas
            return redirect('lista_tareas', persona_id=persona_obj.id)
        else:
            # Si las credenciales son incorrectas, muestra un mensaje de error
            return render(request, 'registro.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'registro.html')


def lista_tareas(request, persona_id):
    # Muestra las tareas de un usuario específico
    persona_obj = get_object_or_404(persona, id=persona_id)
     # Verificar si el usuario decide cerrar sesión
    if 'cerrar_sesion' in request.GET:
        logout(request)
        return redirect('seccion')  # Redirige al inicio de sesión
    tareas = Task.objects.filter(nombre=persona_obj)  # Tareas asociadas al usuario
    return render(request, 'lista_tareas.html', {'persona': persona_obj, 'tareas': tareas})


def crear_tarea(request, persona_id):
    # Crear una nueva tarea para un usuario
    persona_obj = get_object_or_404(persona, id=persona_id)

    # Verificar si el usuario decide cerrar sesión
    if 'cerrar_sesion' in request.GET:
        logout(request)
        return redirect('seccion')  # Redirige al inicio de sesión

    if request.method == 'POST':
        title = request.POST.get('title', '')
        description = request.POST.get('description', '')
        completed = request.POST.get('completed', 'off') == 'on'

        # Guardar la nueva tarea en la base de datos
        Task.objects.create(
            title=title,
            description=description,
            completed=completed,
            nombre=persona_obj
        )
        return redirect('lista_tareas', persona_id=persona_id)

    return render(request, 'crear_tarea.html', {'persona': persona_obj})


def editar_tarea(request, tarea_id):
    # Editar una tarea existente
    tarea = get_object_or_404(Task, id=tarea_id)

    if request.method == 'POST':
        # Actualizar los datos de la tarea
        tarea.title = request.POST.get('title', tarea.title)
        tarea.description = request.POST.get('description', tarea.description)
        tarea.completed = request.POST.get('completed', 'off') == 'on'
        tarea.save()
        return redirect('lista_tareas', persona_id=tarea.nombre.id)

    return render(request, 'editar_tarea.html', {'tarea': tarea})


def eliminar_tarea(request, tarea_id):
    # Eliminar una tarea específica
    tarea = get_object_or_404(Task, id=tarea_id)
    persona_id = tarea.nombre.id  # ID del usuario asociado a la tarea
    tarea.delete()  # Eliminar la tarea de la base de datos
    return redirect('lista_tareas', persona_id=persona_id)