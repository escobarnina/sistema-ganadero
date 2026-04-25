from datetime import date, timedelta

import graphene
from graphene_django import DjangoObjectType

from .models import (
    InseminacionArtificial,
    MontaNatural,
    DiagnosticoPrenez,
    Reproduccion,
)


class InseminacionArtificialType(DjangoObjectType):
    class Meta:
        model = InseminacionArtificial
        fields = "__all__"


class MontaNaturalType(DjangoObjectType):
    class Meta:
        model = MontaNatural
        fields = "__all__"


class DiagnosticoPrenezType(DjangoObjectType):
    class Meta:
        model = DiagnosticoPrenez
        fields = "__all__"


class ReproduccionType(DjangoObjectType):
    class Meta:
        model = Reproduccion
        fields = "__all__"


class Query(graphene.ObjectType):
    inseminaciones = graphene.List(InseminacionArtificialType)
    montas_naturales = graphene.List(MontaNaturalType)
    diagnosticos_prenez = graphene.List(DiagnosticoPrenezType)
    reproducciones = graphene.List(ReproduccionType)

    vacas_prenadas = graphene.List(ReproduccionType)
    proximos_partos = graphene.List(
        ReproduccionType,
        dias=graphene.Int(default_value=30)
    )

    def resolve_inseminaciones(self, info):
        return InseminacionArtificial.objects.all()

    def resolve_montas_naturales(self, info):
        return MontaNatural.objects.all()

    def resolve_diagnosticos_prenez(self, info):
        return DiagnosticoPrenez.objects.all()

    def resolve_reproducciones(self, info):
        return Reproduccion.objects.all()

    def resolve_vacas_prenadas(self, info):
        return Reproduccion.objects.filter(estado="PRENADA")

    def resolve_proximos_partos(self, info, dias=30):
        hoy = date.today()
        limite = hoy + timedelta(days=dias)

        return Reproduccion.objects.filter(
            fecha_parto_esperado__gte=hoy,
            fecha_parto_esperado__lte=limite,
        ).exclude(estado="PARIDA")