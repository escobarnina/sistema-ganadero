import graphene
from graphene_django import DjangoObjectType

from .models import Finca


class FincaType(DjangoObjectType):
    class Meta:
        model = Finca
        fields = "__all__"


class Query(graphene.ObjectType):
    fincas = graphene.List(FincaType)
    finca = graphene.Field(FincaType, id=graphene.ID(required=True))

    def resolve_fincas(self, info):
        return Finca.objects.all()

    def resolve_finca(self, info, id):
        return Finca.objects.filter(id=id).first()
    
class CrearFinca(graphene.Mutation):
    class Arguments:
        nombre = graphene.String(required=True)
        propietario = graphene.String()
        departamento = graphene.String()
        municipio = graphene.String()
        ubicacion = graphene.String()
        telefono = graphene.String()

    finca = graphene.Field(FincaType)

    def mutate(self, info, nombre, propietario=None, departamento=None, municipio=None, ubicacion=None, telefono=None):
        finca = Finca.objects.create(
            nombre=nombre,
            propietario=propietario,
            departamento=departamento,
            municipio=municipio,
            ubicacion=ubicacion,
            telefono=telefono
        )
        return CrearFinca(finca=finca)


class Mutation(graphene.ObjectType):
    crear_finca = CrearFinca.Field()
    
    
    