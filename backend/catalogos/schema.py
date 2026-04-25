import graphene
from graphene_django import DjangoObjectType

from .models import (
    Raza,
    CategoriaAnimal,
    TipoMedicamento,
    Medicamento,
    Veterinario,
    Alimento,
    Reproductor,
)


class RazaType(DjangoObjectType):
    class Meta:
        model = Raza
        fields = "__all__"


class CategoriaAnimalType(DjangoObjectType):
    class Meta:
        model = CategoriaAnimal
        fields = "__all__"


class TipoMedicamentoType(DjangoObjectType):
    class Meta:
        model = TipoMedicamento
        fields = "__all__"


class MedicamentoType(DjangoObjectType):
    class Meta:
        model = Medicamento
        fields = "__all__"


class VeterinarioType(DjangoObjectType):
    class Meta:
        model = Veterinario
        fields = "__all__"


class AlimentoType(DjangoObjectType):
    class Meta:
        model = Alimento
        fields = "__all__"


class ReproductorType(DjangoObjectType):
    class Meta:
        model = Reproductor
        fields = "__all__"


class Query(graphene.ObjectType):
    razas = graphene.List(RazaType)
    categorias_animales = graphene.List(CategoriaAnimalType)
    tipos_medicamento = graphene.List(TipoMedicamentoType)
    medicamentos = graphene.List(MedicamentoType)
    veterinarios = graphene.List(VeterinarioType)
    alimentos = graphene.List(AlimentoType)
    reproductores = graphene.List(ReproductorType)

    def resolve_razas(self, info):
        return Raza.objects.all()

    def resolve_categorias_animales(self, info):
        return CategoriaAnimal.objects.all()

    def resolve_tipos_medicamento(self, info):
        return TipoMedicamento.objects.all()

    def resolve_medicamentos(self, info):
        return Medicamento.objects.all()

    def resolve_veterinarios(self, info):
        return Veterinario.objects.all()

    def resolve_alimentos(self, info):
        return Alimento.objects.all()

    def resolve_reproductores(self, info):
        return Reproductor.objects.all()
    
class CrearRaza(graphene.Mutation):
    class Arguments:
        nombre = graphene.String(required=True)
        orientacion = graphene.String()
        origen = graphene.String()
        descripcion = graphene.String()

    raza = graphene.Field(RazaType)

    def mutate(self, info, nombre, orientacion="DOBLE_PROPOSITO", origen=None, descripcion=None):
        raza = Raza.objects.create(
            nombre=nombre,
            orientacion=orientacion,
            origen=origen,
            descripcion=descripcion
        )
        return CrearRaza(raza=raza)


class CrearCategoriaAnimal(graphene.Mutation):
    class Arguments:
        nombre = graphene.String(required=True)
        descripcion = graphene.String()

    categoria = graphene.Field(CategoriaAnimalType)

    def mutate(self, info, nombre, descripcion=None):
        categoria = CategoriaAnimal.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )
        return CrearCategoriaAnimal(categoria=categoria)


class CrearReproductor(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        raza_id = graphene.ID()
        codigo = graphene.String(required=True)
        nombre = graphene.String()
        tipo_origen = graphene.String(required=True)
        codigo_pajuela = graphene.String()
        laboratorio = graphene.String()

    reproductor = graphene.Field(ReproductorType)

    def mutate(
        self,
        info,
        finca_id,
        codigo,
        tipo_origen,
        raza_id=None,
        nombre=None,
        codigo_pajuela=None,
        laboratorio=None
    ):
        from fincas.models import Finca

        finca = Finca.objects.get(id=finca_id)
        raza = Raza.objects.filter(id=raza_id).first() if raza_id else None

        reproductor = Reproductor.objects.create(
            finca=finca,
            raza=raza,
            codigo=codigo,
            nombre=nombre,
            tipo_origen=tipo_origen,
            codigo_pajuela=codigo_pajuela,
            laboratorio=laboratorio
        )

        return CrearReproductor(reproductor=reproductor)


class Mutation(graphene.ObjectType):
    crear_raza = CrearRaza.Field()
    crear_categoria_animal = CrearCategoriaAnimal.Field()
    crear_reproductor = CrearReproductor.Field()