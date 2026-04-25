import graphene
from graphene_django import DjangoObjectType

from .models import (
    Proveedor,
    NotaCompra,
    DetalleCompra,
    DetalleCompraAlimento,
)


class ProveedorType(DjangoObjectType):
    class Meta:
        model = Proveedor
        fields = "__all__"


class NotaCompraType(DjangoObjectType):
    class Meta:
        model = NotaCompra
        fields = "__all__"


class DetalleCompraType(DjangoObjectType):
    class Meta:
        model = DetalleCompra
        fields = "__all__"


class DetalleCompraAlimentoType(DjangoObjectType):
    class Meta:
        model = DetalleCompraAlimento
        fields = "__all__"


class Query(graphene.ObjectType):
    proveedores = graphene.List(ProveedorType)
    notas_compra = graphene.List(NotaCompraType)
    detalles_compra = graphene.List(DetalleCompraType)
    detalles_compra_alimento = graphene.List(DetalleCompraAlimentoType)

    compras_por_anio = graphene.List(
        NotaCompraType,
        anio=graphene.Int(required=True)
    )

    def resolve_proveedores(self, info):
        return Proveedor.objects.all()

    def resolve_notas_compra(self, info):
        return NotaCompra.objects.all()

    def resolve_detalles_compra(self, info):
        return DetalleCompra.objects.all()

    def resolve_detalles_compra_alimento(self, info):
        return DetalleCompraAlimento.objects.all()

    def resolve_compras_por_anio(self, info, anio):
        return NotaCompra.objects.filter(fecha_compra__year=anio)