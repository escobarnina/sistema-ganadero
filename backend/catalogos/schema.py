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