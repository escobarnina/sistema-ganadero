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