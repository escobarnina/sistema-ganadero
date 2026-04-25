from datetime import date, timedelta

import graphene
from graphene_django import DjangoObjectType

from .models import (
    Vacunacion,
    Tratamiento,
    Desparasitacion,
    TratamientoMedicamento,
    AnimalMedicamento,
    Diagnostico,
    Observacion,
)


class VacunacionType(DjangoObjectType):
    class Meta:
        model = Vacunacion
        fields = "__all__"


class TratamientoType(DjangoObjectType):
    class Meta:
        model = Tratamiento
        fields = "__all__"


class DesparasitacionType(DjangoObjectType):
    class Meta:
        model = Desparasitacion
        fields = "__all__"


class TratamientoMedicamentoType(DjangoObjectType):
    class Meta:
        model = TratamientoMedicamento
        fields = "__all__"


class AnimalMedicamentoType(DjangoObjectType):
    class Meta:
        model = AnimalMedicamento
        fields = "__all__"


class DiagnosticoType(DjangoObjectType):
    class Meta:
        model = Diagnostico
        fields = "__all__"


class ObservacionType(DjangoObjectType):
    class Meta:
        model = Observacion
        fields = "__all__"


class Query(graphene.ObjectType):
    vacunaciones = graphene.List(VacunacionType)
    tratamientos = graphene.List(TratamientoType)
    desparasitaciones = graphene.List(DesparasitacionType)
    tratamiento_medicamentos = graphene.List(TratamientoMedicamentoType)
    animal_medicamentos = graphene.List(AnimalMedicamentoType)
    diagnosticos = graphene.List(DiagnosticoType)
    observaciones_sanitarias = graphene.List(ObservacionType)

    vacunas_proximas = graphene.List(
        VacunacionType,
        dias=graphene.Int(default_value=30)
    )
    vacunas_vencidas = graphene.List(VacunacionType)

    def resolve_vacunaciones(self, info):
        return Vacunacion.objects.all()

    def resolve_tratamientos(self, info):
        return Tratamiento.objects.all()

    def resolve_desparasitaciones(self, info):
        return Desparasitacion.objects.all()

    def resolve_tratamiento_medicamentos(self, info):
        return TratamientoMedicamento.objects.all()

    def resolve_animal_medicamentos(self, info):
        return AnimalMedicamento.objects.all()

    def resolve_diagnosticos(self, info):
        return Diagnostico.objects.all()

    def resolve_observaciones_sanitarias(self, info):
        return Observacion.objects.all()

    def resolve_vacunas_proximas(self, info, dias=30):
        hoy = date.today()
        limite = hoy + timedelta(days=dias)

        return Vacunacion.objects.filter(
            proxima_fecha__gte=hoy,
            proxima_fecha__lte=limite,
        )

    def resolve_vacunas_vencidas(self, info):
        hoy = date.today()

        return Vacunacion.objects.filter(
            proxima_fecha__lt=hoy,
        )
        
class CrearVacunacion(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        animal_id = graphene.ID(required=True)
        medicamento_id = graphene.ID()
        fecha = graphene.Date(required=True)
        dosis = graphene.String()
        via_aplicacion = graphene.String()
        costo = graphene.Decimal()
        campana = graphene.String()
        lote = graphene.String()
        observaciones = graphene.String()

    vacunacion = graphene.Field(VacunacionType)

    def mutate(
        self,
        info,
        finca_id,
        animal_id,
        fecha,
        medicamento_id=None,
        dosis=None,
        via_aplicacion=None,
        costo=0,
        campana=None,
        lote=None,
        observaciones=None
    ):
        from fincas.models import Finca
        from animales.models import Animal
        from catalogos.models import Medicamento

        finca = Finca.objects.get(id=finca_id)
        animal = Animal.objects.get(id=animal_id)
        medicamento = Medicamento.objects.filter(id=medicamento_id).first() if medicamento_id else None

        vacunacion = Vacunacion.objects.create(
            finca=finca,
            animal=animal,
            medicamento=medicamento,
            fecha=fecha,
            dosis=dosis,
            via_aplicacion=via_aplicacion,
            costo=costo,
            campana=campana,
            lote=lote,
            observaciones=observaciones
        )

        return CrearVacunacion(vacunacion=vacunacion)


class CrearTratamiento(graphene.Mutation):
    class Arguments:
        finca_id = graphene.ID(required=True)
        animal_id = graphene.ID(required=True)
        medicamento_id = graphene.ID()
        fecha = graphene.Date(required=True)
        diagnostico = graphene.String()
        tipo = graphene.String()
        dosis = graphene.String()
        costo_total = graphene.Decimal()

    tratamiento = graphene.Field(TratamientoType)

    def mutate(
        self,
        info,
        finca_id,
        animal_id,
        fecha,
        medicamento_id=None,
        diagnostico=None,
        tipo=None,
        dosis=None,
        costo_total=0
    ):
        from fincas.models import Finca
        from animales.models import Animal
        from catalogos.models import Medicamento

        finca = Finca.objects.get(id=finca_id)
        animal = Animal.objects.get(id=animal_id)
        medicamento = Medicamento.objects.filter(id=medicamento_id).first() if medicamento_id else None

        tratamiento = Tratamiento.objects.create(
            finca=finca,
            animal=animal,
            medicamento=medicamento,
            fecha=fecha,
            fecha_inicio=fecha,
            diagnostico=diagnostico,
            tipo=tipo,
            dosis=dosis,
            costo_total=costo_total
        )

        return CrearTratamiento(tratamiento=tratamiento)


class Mutation(graphene.ObjectType):
    crear_vacunacion = CrearVacunacion.Field()
    crear_tratamiento = CrearTratamiento.Field()
    
class Mutation(graphene.ObjectType):
    pass