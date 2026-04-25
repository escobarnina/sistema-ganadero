from datetime import date, timedelta

import graphene
from graphene_django import DjangoObjectType

from .models import (
    InseminacionArtificial,
    MontaNatural,
    DiagnosticoPrenez,
    Reproduccion,
)


class InseminacionArtificialType(DjangoObjectType):
    class Meta:
        model = InseminacionArtificial
        fields = "__all__"


class MontaNaturalType(DjangoObjectType):
    class Meta:
        model = MontaNatural
        fields = "__all__"


class DiagnosticoPrenezType(DjangoObjectType):
    class Meta:
        model = DiagnosticoPrenez
        fields = "__all__"


class ReproduccionType(DjangoObjectType):
    class Meta:
        model = Reproduccion
        fields = "__all__"


class Query(graphene.ObjectType):
    inseminaciones = graphene.List(InseminacionArtificialType)
    montas_naturales = graphene.List(MontaNaturalType)
    diagnosticos_prenez = graphene.List(DiagnosticoPrenezType)
    reproducciones = graphene.List(ReproduccionType)

    vacas_prenadas = graphene.List(ReproduccionType)
    proximos_partos = graphene.List(
        ReproduccionType,
        dias=graphene.Int(default_value=30)
    )

    def resolve_inseminaciones(self, info):
        return InseminacionArtificial.objects.all()

    def resolve_montas_naturales(self, info):
        return MontaNatural.objects.all()

    def resolve_diagnosticos_prenez(self, info):
        return DiagnosticoPrenez.objects.all()

    def resolve_reproducciones(self, info):
        return Reproduccion.objects.all()

    def resolve_vacas_prenadas(self, info):
        return Reproduccion.objects.filter(estado="PRENADA")

    def resolve_proximos_partos(self, info, dias=30):
        hoy = date.today()
        limite = hoy + timedelta(days=dias)

        return Reproduccion.objects.filter(
            fecha_parto_esperado__gte=hoy,
            fecha_parto_esperado__lte=limite,
        ).exclude(estado="PARIDA")
        
class CrearInseminacionArtificial(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        hembra_id = graphene.ID(required=True)
        reproductor_id = graphene.ID()
        fecha = graphene.Date(required=True)
        numero_servicio = graphene.Int()
        numero_pajuela = graphene.String()
        tecnico_inseminador = graphene.String()
        observaciones = graphene.String()

    inseminacion = graphene.Field(InseminacionArtificialType)

    def mutate(
        self,
        info,
        finca_id,
        hembra_id,
        fecha,
        reproductor_id=None,
        numero_servicio=1,
        numero_pajuela=None,
        tecnico_inseminador=None,
        observaciones=None
    ):
        from fincas.models import Finca
        from animales.models import Animal
        from catalogos.models import Reproductor

        finca = Finca.objects.get(id=finca_id)
        hembra = Animal.objects.get(id=hembra_id)
        reproductor = Reproductor.objects.filter(id=reproductor_id).first() if reproductor_id else None

        inseminacion = InseminacionArtificial.objects.create(
            finca=finca,
            hembra=hembra,
            reproductor=reproductor,
            fecha=fecha,
            numero_servicio=numero_servicio,
            numero_pajuela=numero_pajuela,
            tecnico_inseminador=tecnico_inseminador,
            observaciones=observaciones
        )

        return CrearInseminacionArtificial(inseminacion=inseminacion)


class CrearDiagnosticoPrenez(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        hembra_id = graphene.ID(required=True)
        fecha = graphene.Date(required=True)
        resultado_prenez = graphene.String(required=True)
        dias_gestacion = graphene.Int()
        metodo = graphene.String()

    diagnostico = graphene.Field(DiagnosticoPrenezType)

    def mutate(
        self,
        info,
        finca_id,
        hembra_id,
        fecha,
        resultado_prenez,
        dias_gestacion=0,
        metodo=None
    ):
        from fincas.models import Finca
        from animales.models import Animal

        finca = Finca.objects.get(id=finca_id)
        hembra = Animal.objects.get(id=hembra_id)

        diagnostico = DiagnosticoPrenez.objects.create(
            finca=finca,
            hembra=hembra,
            fecha=fecha,
            resultado_prenez=resultado_prenez,
            dias_gestacion=dias_gestacion,
            metodo=metodo
        )

        return CrearDiagnosticoPrenez(diagnostico=diagnostico)


class CrearReproduccion(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        madre_id = graphene.ID(required=True)
        fecha_servicio = graphene.Date()
        fecha_parto_real = graphene.Date()
        tipo_parto = graphene.String()
        num_crias = graphene.Int()
        estado = graphene.String()
        observaciones = graphene.String()

    reproduccion = graphene.Field(ReproduccionType)

    def mutate(
        self,
        info,
        finca_id,
        madre_id,
        fecha_servicio=None,
        fecha_parto_real=None,
        tipo_parto="NORMAL",
        num_crias=1,
        estado="SERVIDA",
        observaciones=None
    ):
        from fincas.models import Finca
        from animales.models import Animal

        finca = Finca.objects.get(id=finca_id)
        madre = Animal.objects.get(id=madre_id)

        reproduccion = Reproduccion.objects.create(
            finca=finca,
            madre=madre,
            fecha_servicio=fecha_servicio,
            fecha_parto_real=fecha_parto_real,
            tipo_parto=tipo_parto,
            num_crias=num_crias,
            estado=estado,
            observaciones=observaciones
        )

        return CrearReproduccion(reproduccion=reproduccion)


class Mutation(graphene.ObjectType):
    crear_inseminacion_artificial = CrearInseminacionArtificial.Field()
    crear_diagnostico_prenez = CrearDiagnosticoPrenez.Field()
    crear_reproduccion = CrearReproduccion.Field()
    
class Mutation(graphene.ObjectType):
    pass