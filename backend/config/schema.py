import graphene

import accounts.schema
import fincas.schema
import catalogos.schema
import animales.schema
import reproduccion.schema
import sanidad.schema
import produccion.schema
import comercio.schema
import compras.schema
import alertas.schema


class Query(
    accounts.schema.Query,
    fincas.schema.Query,
    catalogos.schema.Query,
    animales.schema.Query,
    reproduccion.schema.Query,
    sanidad.schema.Query,
    produccion.schema.Query,
    comercio.schema.Query,
    compras.schema.Query,
    alertas.schema.Query,
    graphene.ObjectType
):
    pass


class Mutation(
    fincas.schema.Mutation,
    catalogos.schema.Mutation,
    animales.schema.Mutation,
    reproduccion.schema.Mutation,
    sanidad.schema.Mutation,
    produccion.schema.Mutation,
    comercio.schema.Mutation,
    compras.schema.Mutation,
    alertas.schema.Mutation,
    graphene.ObjectType
):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)