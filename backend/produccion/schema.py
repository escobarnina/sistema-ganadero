import graphene
from graphene_django import DjangoObjectType

from .models import (
    RegistroPeso,
    Lactancia,
    ProduccionLeche,
    AlimentoAnimal,
)


class RegistroPesoType(DjangoObjectType):
    class Meta:
        model = RegistroPeso
        fields = "__all__"


class LactanciaType(DjangoObjectType):
    class Meta:
        model = Lactancia
        fields = "__all__"


class ProduccionLecheType(DjangoObjectType):
    class Meta:
        model = ProduccionLeche
        fields = "__all__"


class AlimentoAnimalType(DjangoObjectType):
    class Meta:
        model = AlimentoAnimal
        fields = "__all__"


class Query(graphene.ObjectType):
    registros_peso = graphene.List(RegistroPesoType)
    lactancias = graphene.List(LactanciaType)
    producciones_leche = graphene.List(ProduccionLecheType)
    alimentaciones_animales = graphene.List(AlimentoAnimalType)

    produccion_leche_por_animal = graphene.List(
        ProduccionLecheType,
        animal_id=graphene.ID(required=True)
    )

    produccion_leche_por_anio = graphene.List(
        ProduccionLecheType,
        anio=graphene.Int(required=True)
    )

    def resolve_registros_peso(self, info):
        return RegistroPeso.objects.all()

    def resolve_lactancias(self, info):
        return Lactancia.objects.all()

    def resolve_producciones_leche(self, info):
        return ProduccionLeche.objects.all()

    def resolve_alimentaciones_animales(self, info):
        return AlimentoAnimal.objects.all()

    def resolve_produccion_leche_por_animal(self, info, animal_id):
        return ProduccionLeche.objects.filter(vaca_id=animal_id)

    def resolve_produccion_leche_por_anio(self, info, anio):
        return ProduccionLeche.objects.filter(fecha__year=anio)