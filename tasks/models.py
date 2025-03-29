from django.db import models

class User(models.Model):
    nombre = models.CharField(max_length=150)
    correo = models.EmailField(unique=True)  
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

    def __str__(self):
        return self.title
