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
    
class CrearAnimal(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        raza_id = graphene.ID()
        categoria_id = graphene.ID()
        padre_id = graphene.ID()
        madre_id = graphene.ID()

        nro_arete = graphene.String(required=True)
        nombre = graphene.String()
        sexo = graphene.String(required=True)
        fecha_nacimiento = graphene.Date()
        peso_nacimiento = graphene.Decimal()
        peso = graphene.Decimal()
        tipo_produccion = graphene.String()
        origen = graphene.String()
        color = graphene.String()
        observaciones = graphene.String()

    animal = graphene.Field(AnimalType)

    def mutate(
        self,
        info,
        finca_id,
        nro_arete,
        sexo,
        raza_id=None,
        categoria_id=None,
        padre_id=None,
        madre_id=None,
        nombre=None,
        fecha_nacimiento=None,
        peso_nacimiento=0,
        peso=0,
        tipo_produccion="DOBLE_PROPOSITO",
        origen="NACIDO_FINCA",
        color=None,
        observaciones=None
    ):
        from fincas.models import Finca
        from catalogos.models import Raza, CategoriaAnimal

        finca = Finca.objects.get(id=finca_id)
        raza = Raza.objects.filter(id=raza_id).first() if raza_id else None
        categoria = CategoriaAnimal.objects.filter(id=categoria_id).first() if categoria_id else None
        padre = Animal.objects.filter(id=padre_id).first() if padre_id else None
        madre = Animal.objects.filter(id=madre_id).first() if madre_id else None

        animal = Animal.objects.create(
            finca=finca,
            raza=raza,
            categoria=categoria,
            padre=padre,
            madre=madre,
            nro_arete=nro_arete,
            nombre=nombre,
            sexo=sexo,
            fecha_nacimiento=fecha_nacimiento,
            peso_nacimiento=peso_nacimiento,
            peso=peso,
            tipo_produccion=tipo_produccion,
            origen=origen,
            color=color,
            observaciones=observaciones
        )

        return CrearAnimal(animal=animal)


class Mutation(graphene.ObjectType):
    crear_animal = CrearAnimal.Field()