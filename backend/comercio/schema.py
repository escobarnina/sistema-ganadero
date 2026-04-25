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


class CrearCliente(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        nombre = graphene.String(required=True)
        apellidos = graphene.String()
        telefono = graphene.String()
        direccion = graphene.String()
        ci = graphene.String()
        email = graphene.String()

    cliente = graphene.Field(ClienteType)

    def mutate(
        self,
        info,
        finca_id,
        nombre,
        apellidos=None,
        telefono=None,
        direccion=None,
        ci=None,
        email=None
    ):
        from fincas.models import Finca

        finca = Finca.objects.get(id=finca_id)

        cliente = Cliente.objects.create(
            finca=finca,
            nombre=nombre,
            apellidos=apellidos,
            telefono=telefono,
            direccion=direccion,
            ci=ci,
            email=email
        )

        return CrearCliente(cliente=cliente)


class CrearNotaVenta(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        cliente_id = graphene.ID()
        fecha_venta = graphene.Date(required=True)
        guia_salida = graphene.String()
        observaciones = graphene.String()

    nota_venta = graphene.Field(NotaVentaType)

    def mutate(
        self,
        info,
        finca_id,
        fecha_venta,
        cliente_id=None,
        guia_salida=None,
        observaciones=None
    ):
        from fincas.models import Finca

        finca = Finca.objects.get(id=finca_id)
        cliente = Cliente.objects.filter(id=cliente_id).first() if cliente_id else None

        nota_venta = NotaVenta.objects.create(
            finca=finca,
            cliente=cliente,
            fecha_venta=fecha_venta,
            guia_salida=guia_salida,
            observaciones=observaciones
        )

        return CrearNotaVenta(nota_venta=nota_venta)


class CrearDetalleVenta(graphene.Mutation):
    class Arguments:
        nota_venta_id = graphene.ID(required=True)
        animal_id = graphene.ID(required=True)
        precio_unitario = graphene.Decimal(required=True)
        peso_venta_kg = graphene.Decimal(required=True)

    detalle_venta = graphene.Field(DetalleVentaType)

    def mutate(
        self,
        info,
        nota_venta_id,
        animal_id,
        precio_unitario,
        peso_venta_kg
    ):
        from animales.models import Animal

        nota_venta = NotaVenta.objects.get(id=nota_venta_id)
        animal = Animal.objects.get(id=animal_id)

        detalle = DetalleVenta.objects.create(
            nota_venta=nota_venta,
            animal=animal,
            precio_unitario=precio_unitario,
            peso_venta_kg=peso_venta_kg
        )

        return CrearDetalleVenta(detalle_venta=detalle)


class CrearMuerteBaja(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        animal_id = graphene.ID(required=True)
        fecha_baja = graphene.Date(required=True)
        causa = graphene.String(required=True)
        tipo = graphene.String(required=True)
        descripcion = graphene.String()
        peso_estimado_kg = graphene.Decimal()

    muerte_baja = graphene.Field(MuerteBajaType)

    def mutate(
        self,
        info,
        finca_id,
        animal_id,
        fecha_baja,
        causa,
        tipo,
        descripcion=None,
        peso_estimado_kg=0
    ):
        from fincas.models import Finca
        from animales.models import Animal

        finca = Finca.objects.get(id=finca_id)
        animal = Animal.objects.get(id=animal_id)

        muerte_baja = MuerteBaja.objects.create(
            finca=finca,
            animal=animal,
            fecha_baja=fecha_baja,
            causa=causa,
            tipo=tipo,
            descripcion=descripcion,
            peso_estimado_kg=peso_estimado_kg
        )

        return CrearMuerteBaja(muerte_baja=muerte_baja)


class Mutation(graphene.ObjectType):
    crear_cliente = CrearCliente.Field()
    crear_nota_venta = CrearNotaVenta.Field()
    crear_detalle_venta = CrearDetalleVenta.Field()
    crear_muerte_baja = CrearMuerteBaja.Field()