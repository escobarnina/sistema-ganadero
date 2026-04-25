from datetime import timedelta

from django.conf import settings
from django.db import models

from fincas.models import Finca
from animales.models import Animal
from catalogos.models import Medicamento, Veterinario


class EventoSanitario(models.Model):
    finca = models.ForeignKey(
        Finca,
        on_delete=models.CASCADE,
        related_name="%(class)s_eventos_sanitarios"
    )
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="%(class)s_eventos_sanitarios"
    )
    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_eventos_sanitarios"
    )
    veterinario = models.ForeignKey(
        Veterinario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_eventos_sanitarios"
    )
    fecha = models.DateField()
    dosis = models.CharField(max_length=100, blank=True, null=True)
    via_aplicacion = models.CharField(max_length=100, blank=True, null=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    proxima_fecha = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_eventos_sanitarios_registrados"
    )

    class Meta:
        abstract = True
    def calcular_proxima_fecha(self):
        if self.fecha and self.medicamento and self.medicamento.intervalo_dias:
            return self.fecha + timedelta(days=self.medicamento.intervalo_dias)
        return None

class Vacunacion(EventoSanitario):
    campana = models.CharField(max_length=150, blank=True, null=True)
    lote = models.CharField(max_length=100, blank=True, null=True)
    fecha_proxima = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.proxima_fecha:
            self.proxima_fecha = self.calcular_proxima_fecha()

        if not self.fecha_proxima:
            self.fecha_proxima = self.proxima_fecha

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Vacunación - {self.animal} - {self.fecha}"


class Tratamiento(EventoSanitario):
    diagnostico = models.CharField(max_length=200, blank=True, null=True)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    dias_retiro = models.IntegerField(default=0)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    costo_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    en_tratamiento = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.proxima_fecha:
            self.proxima_fecha = self.calcular_proxima_fecha()

        if self.fecha_fin:
            self.en_tratamiento = False

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Tratamiento - {self.animal} - {self.diagnostico or self.fecha}"


class Desparasitacion(EventoSanitario):
    tipo_parasiticida = models.CharField(max_length=150, blank=True, null=True)
    peso_aplicacion = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lote = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.proxima_fecha:
            self.proxima_fecha = self.calcular_proxima_fecha()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Desparasitación - {self.animal} - {self.fecha}"


class TratamientoMedicamento(models.Model):
    tratamiento = models.ForeignKey(
        Tratamiento,
        on_delete=models.CASCADE,
        related_name="medicamentos_aplicados"
    )
    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.CASCADE,
        related_name="tratamientos_asociados"
    )
    dosis = models.CharField(max_length=100, blank=True, null=True)
    via_aplicacion = models.CharField(max_length=100, blank=True, null=True)
    dias_retiro = models.IntegerField(default=0)
    fecha = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.tratamiento} - {self.medicamento}"


class AnimalMedicamento(models.Model):
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="medicamentos_directos"
    )
    medicamento = models.ForeignKey(
        Medicamento,
        on_delete=models.CASCADE,
        related_name="animales_medicados"
    )
    dosis = models.CharField(max_length=100, blank=True, null=True)
    fecha_administracion = models.DateField()
    fecha_siguiente = models.DateField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.fecha_siguiente and self.medicamento.intervalo_dias:
            self.fecha_siguiente = self.fecha_administracion + timedelta(
                days=self.medicamento.intervalo_dias
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.animal} - {self.medicamento}"


class Diagnostico(models.Model):
    finca = models.ForeignKey(
        Finca,
        on_delete=models.CASCADE,
        related_name="diagnosticos"
    )
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="diagnosticos"
    )
    veterinario = models.ForeignKey(
        Veterinario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="diagnosticos_clinicos"
    )
    descripcion = models.TextField()
    fecha = models.DateField()

    def __str__(self):
        return f"Diagnóstico - {self.animal} - {self.fecha}"


class Observacion(models.Model):
    finca = models.ForeignKey(
        Finca,
        on_delete=models.CASCADE,
        related_name="observaciones_sanitarias"
    )
    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        related_name="observaciones_sanitarias"
    )
    descripcion = models.TextField()
    fecha = models.DateField()
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="observaciones_sanitarias_registradas"
    )

    def __str__(self):
        return f"Observación - {self.animal} - {self.fecha}"