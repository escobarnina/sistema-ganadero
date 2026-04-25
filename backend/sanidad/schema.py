from datetime import date, timedelta

import graphene
from graphene_django import DjangoObjectType

from .models import (
    Vacunacion,
    Tratamiento,
    Desparasitacion,
    TratamientoMedicamento,
    AnimalMedicamento,
    Diagnostico,
    Observacion,
)


class VacunacionType(DjangoObjectType):
    class Meta:
        model = Vacunacion
        fields = "__all__"


class TratamientoType(DjangoObjectType):
    class Meta:
        model = Tratamiento
        fields = "__all__"


class DesparasitacionType(DjangoObjectType):
    class Meta:
        model = Desparasitacion
        fields = "__all__"


class TratamientoMedicamentoType(DjangoObjectType):
    class Meta:
        model = TratamientoMedicamento
        fields = "__all__"


class AnimalMedicamentoType(DjangoObjectType):
    class Meta:
        model = AnimalMedicamento
        fields = "__all__"


class DiagnosticoType(DjangoObjectType):
    class Meta:
        model = Diagnostico
        fields = "__all__"


class ObservacionType(DjangoObjectType):
    class Meta:
        model = Observacion
        fields = "__all__"


class Query(graphene.ObjectType):
    vacunaciones = graphene.List(VacunacionType)
    tratamientos = graphene.List(TratamientoType)
    desparasitaciones = graphene.List(DesparasitacionType)
    tratamiento_medicamentos = graphene.List(TratamientoMedicamentoType)
    animal_medicamentos = graphene.List(AnimalMedicamentoType)
    diagnosticos = graphene.List(DiagnosticoType)
    observaciones_sanitarias = graphene.List(ObservacionType)

    vacunas_proximas = graphene.List(
        VacunacionType,
        dias=graphene.Int(default_value=30)
    )
    vacunas_vencidas = graphene.List(VacunacionType)

    def resolve_vacunaciones(self, info):
        return Vacunacion.objects.all()

    def resolve_tratamientos(self, info):
        return Tratamiento.objects.all()

    def resolve_desparasitaciones(self, info):
        return Desparasitacion.objects.all()

    def resolve_tratamiento_medicamentos(self, info):
        return TratamientoMedicamento.objects.all()

    def resolve_animal_medicamentos(self, info):
        return AnimalMedicamento.objects.all()

    def resolve_diagnosticos(self, info):
        return Diagnostico.objects.all()

    def resolve_observaciones_sanitarias(self, info):
        return Observacion.objects.all()

    def resolve_vacunas_proximas(self, info, dias=30):
        hoy = date.today()
        limite = hoy + timedelta(days=dias)

        return Vacunacion.objects.filter(
            proxima_fecha__gte=hoy,
            proxima_fecha__lte=limite,
        )

    def resolve_vacunas_vencidas(self, info):
        hoy = date.today()

        return Vacunacion.objects.filter(
            proxima_fecha__lt=hoy,
        )