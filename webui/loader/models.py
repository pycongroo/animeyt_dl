from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Resultado:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
