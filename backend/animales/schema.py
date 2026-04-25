import graphene
from graphene_django import DjangoObjectType

from .models import Animal, Parcela, AnimalParcela


class AnimalType(DjangoObjectType):
    class Meta:
        model = Animal
        fields = "__all__"


class ParcelaType(DjangoObjectType):
    class Meta:
        model = Parcela
        fields = "__all__"


class AnimalParcelaType(DjangoObjectType):
    class Meta:
        model = AnimalParcela
        fields = "__all__"


class Query(graphene.ObjectType):
    animales = graphene.List(AnimalType)
    animales_activos = graphene.List(AnimalType)
    animal_por_arete = graphene.Field(
        AnimalType,
        nro_arete=graphene.String(required=True)
    )
    animales_por_anio_nacimiento = graphene.List(
        AnimalType,
        anio=graphene.Int(required=True)
    )
    animales_por_estado = graphene.List(
        AnimalType,
        estado=graphene.String(required=True)
    )
    parcelas = graphene.List(ParcelaType)
    historial_parcelas = graphene.List(AnimalParcelaType)

    def resolve_animales(self, info):
        return Animal.objects.all()

    def resolve_animales_activos(self, info):
        return Animal.objects.filter(estado="ACTIVO")

    def resolve_animal_por_arete(self, info, nro_arete):
        return Animal.objects.filter(nro_arete=nro_arete).first()

    def resolve_animales_por_anio_nacimiento(self, info, anio):
        return Animal.objects.filter(fecha_nacimiento__year=anio)

    def resolve_animales_por_estado(self, info, estado):
        return Animal.objects.filter(estado=estado)

    def resolve_parcelas(self, info):
        return Parcela.objects.all()

    def resolve_historial_parcelas(self, info):
        return AnimalParcela.objects.all()