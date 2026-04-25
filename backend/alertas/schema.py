import graphene
from graphene_django import DjangoObjectType

from .models import Gasto, Alerta


class GastoType(DjangoObjectType):
    class Meta:
        model = Gasto
        fields = "__all__"


class AlertaType(DjangoObjectType):
    class Meta:
        model = Alerta
        fields = "__all__"


class Query(graphene.ObjectType):
    gastos = graphene.List(GastoType)
    alertas = graphene.List(AlertaType)
    alertas_pendientes = graphene.List(AlertaType)

    gastos_por_anio = graphene.List(
        GastoType,
        anio=graphene.Int(required=True)
    )

    def resolve_gastos(self, info):
        return Gasto.objects.all()

    def resolve_alertas(self, info):
        return Alerta.objects.all()

    def resolve_alertas_pendientes(self, info):
        return Alerta.objects.filter(leida=False)

    def resolve_gastos_por_anio(self, info, anio):
        return Gasto.objects.filter(fecha__year=anio)