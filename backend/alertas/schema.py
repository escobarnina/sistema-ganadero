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
    
class CrearGasto(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        animal_id = graphene.ID()
        fecha = graphene.Date(required=True)
        tipo_gasto = graphene.String(required=True)
        descripcion = graphene.String(required=True)
        cantidad = graphene.Decimal()
        precio_unitario = graphene.Decimal()

    gasto = graphene.Field(GastoType)

    def mutate(
        self,
        info,
        finca_id,
        fecha,
        tipo_gasto,
        descripcion,
        animal_id=None,
        cantidad=1,
        precio_unitario=0
    ):
        from fincas.models import Finca
        from animales.models import Animal

        finca = Finca.objects.get(id=finca_id)
        animal = Animal.objects.filter(id=animal_id).first() if animal_id else None

        gasto = Gasto.objects.create(
            finca=finca,
            animal=animal,
            fecha=fecha,
            tipo_gasto=tipo_gasto,
            descripcion=descripcion,
            cantidad=cantidad,
            precio_unitario=precio_unitario
        )

        return CrearGasto(gasto=gasto)


class Mutation(graphene.ObjectType):
    crear_gasto = CrearGasto.Field()