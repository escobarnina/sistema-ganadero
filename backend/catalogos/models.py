from django.db import models
from fincas.models import Finca


class Raza(models.Model):
    TIPO_PRODUCCION_CHOICES = [
        ("CARNE", "Carne"),
        ("LECHE", "Leche"),
        ("DOBLE_PROPOSITO", "Doble propósito"),
    ]

    nombre = models.CharField(max_length=100)
    orientacion = models.CharField(
        max_length=30,
        choices=TIPO_PRODUCCION_CHOICES,
        default="DOBLE_PROPOSITO"
    )
    origen = models.CharField(max_length=100, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class CategoriaAnimal(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class TipoMedicamento(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

 

class Medicamento(models.Model):
    finca = models.ForeignKey(
        Finca,
        on_delete=models.CASCADE,
        related_name="medicamentos"
    )
    tipo = models.ForeignKey(
        TipoMedicamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    laboratorio = models.CharField(max_length=150, blank=True, null=True)
    unidad_medida = models.CharField(max_length=50, blank=True, null=True)
    stock_cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contenido_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    intervalo_dias = models.IntegerField(default=0)
    imagen = models.ImageField(upload_to="medicamentos/", blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Veterinario(models.Model):
    finca = models.ForeignKey(
        Finca,
        on_delete=models.CASCADE,
        related_name="veterinarios"
    )
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    ci = models.CharField(max_length=30, blank=True, null=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos or ''}"


class Alimento(models.Model):
    finca = models.ForeignKey(
        Finca,
        on_delete=models.CASCADE,
        related_name="alimentos"
    )
    nombre = models.CharField(max_length=150)
    contenido_neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unidad_medida = models.CharField(max_length=50, blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    stock_cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio_referencia = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class Reproductor(models.Model):
    TIPO_ORIGEN_CHOICES = [
        ("INTERNO", "Interno"),
        ("EXTERNO", "Externo"),
        ("SEMEN", "Semen"),
    ]

    finca = models.ForeignKey(
        Finca,
        on_delete=models.CASCADE,
        related_name="reproductores"
    )
    raza = models.ForeignKey(
        Raza,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reproductores"
    )

    codigo = models.CharField(max_length=100)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    tipo_origen = models.CharField(max_length=30, choices=TIPO_ORIGEN_CHOICES)
    codigo_pajuela = models.CharField(max_length=100, blank=True, null=True)
    laboratorio = models.CharField(max_length=150, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre or self.codigo

