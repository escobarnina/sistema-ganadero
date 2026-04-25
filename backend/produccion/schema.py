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
    
class CrearRegistroPeso(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        animal_id = graphene.ID(required=True)
        fecha_pesaje = graphene.Date(required=True)
        peso_kg = graphene.Decimal(required=True)
        condicion_corporal = graphene.Decimal()
        observacion = graphene.String()

    registro = graphene.Field(RegistroPesoType)

    def mutate(
        self,
        info,
        finca_id,
        animal_id,
        fecha_pesaje,
        peso_kg,
        condicion_corporal=0,
        observacion=None
    ):
        from fincas.models import Finca
        from animales.models import Animal

        finca = Finca.objects.get(id=finca_id)
        animal = Animal.objects.get(id=animal_id)

        registro = RegistroPeso.objects.create(
            finca=finca,
            animal=animal,
            fecha_pesaje=fecha_pesaje,
            peso_kg=peso_kg,
            condicion_corporal=condicion_corporal,
            observacion=observacion
        )

        return CrearRegistroPeso(registro=registro)


class CrearLactancia(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        vaca_id = graphene.ID(required=True)
        numero_lactancia = graphene.Int()
        fecha_inicio = graphene.Date(required=True)

    lactancia = graphene.Field(LactanciaType)

    def mutate(self, info, finca_id, vaca_id, fecha_inicio, numero_lactancia=1):
        from fincas.models import Finca
        from animales.models import Animal

        finca = Finca.objects.get(id=finca_id)
        vaca = Animal.objects.get(id=vaca_id)

        lactancia = Lactancia.objects.create(
            finca=finca,
            vaca=vaca,
            numero_lactancia=numero_lactancia,
            fecha_inicio=fecha_inicio
        )

        return CrearLactancia(lactancia=lactancia)


class CrearProduccionLeche(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        vaca_id = graphene.ID(required=True)
        lactancia_id = graphene.ID(required=True)
        fecha = graphene.Date(required=True)
        turno = graphene.String(required=True)
        litros = graphene.Decimal(required=True)

    produccion = graphene.Field(ProduccionLecheType)

    def mutate(self, info, finca_id, vaca_id, lactancia_id, fecha, turno, litros):
        from fincas.models import Finca
        from animales.models import Animal

        finca = Finca.objects.get(id=finca_id)
        vaca = Animal.objects.get(id=vaca_id)
        lactancia = Lactancia.objects.get(id=lactancia_id)

        produccion = ProduccionLeche.objects.create(
            finca=finca,
            vaca=vaca,
            lactancia=lactancia,
            fecha=fecha,
            turno=turno,
            litros=litros
        )

        return CrearProduccionLeche(produccion=produccion)


class Mutation(graphene.ObjectType):
    crear_registro_peso = CrearRegistroPeso.Field()
    crear_lactancia = CrearLactancia.Field()
    crear_produccion_leche = CrearProduccionLeche.Field()