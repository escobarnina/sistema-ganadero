import graphene
from graphene_django import DjangoObjectType

from .models import Usuario, Rol


class RolType(DjangoObjectType):
    class Meta:
        model = Rol
        fields = "__all__"


class UsuarioType(DjangoObjectType):
    class Meta:
        model = Usuario
        fields = "__all__"


class Query(graphene.ObjectType):
    roles = graphene.List(RolType)
    usuarios = graphene.List(UsuarioType)

    def resolve_roles(self, info):
        return Rol.objects.all()

    def resolve_usuarios(self, info):
        return Usuario.objects.all()