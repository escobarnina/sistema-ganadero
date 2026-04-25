import graphene
from graphene_django import DjangoObjectType

from .models import (
    Cliente,
    NotaVenta,
    DetalleVenta,
    MuerteBaja,
)


class ClienteType(DjangoObjectType):
    class Meta:
        model = Cliente
        fields = "__all__"


class NotaVentaType(DjangoObjectType):
    class Meta:
        model = NotaVenta
        fields = "__all__"


class DetalleVentaType(DjangoObjectType):
    class Meta:
        model = DetalleVenta
        fields = "__all__"


class MuerteBajaType(DjangoObjectType):
    class Meta:
        model = MuerteBaja
        fields = "__all__"


class Query(graphene.ObjectType):
    clientes = graphene.List(ClienteType)
    notas_venta = graphene.List(NotaVentaType)
    detalles_venta = graphene.List(DetalleVentaType)
    muertes_bajas = graphene.List(MuerteBajaType)

    ventas_por_anio = graphene.List(
        NotaVentaType,
        anio=graphene.Int(required=True)
    )

    def resolve_clientes(self, info):
        return Cliente.objects.all()

    def resolve_notas_venta(self, info):
        return NotaVenta.objects.all()

    def resolve_detalles_venta(self, info):
        return DetalleVenta.objects.all()

    def resolve_muertes_bajas(self, info):
        return MuerteBaja.objects.all()

    def resolve_ventas_por_anio(self, info, anio):
        return NotaVenta.objects.filter(fecha_venta__year=anio)