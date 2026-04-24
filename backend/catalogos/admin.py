from django.contrib import admin
from .models import (
    Raza,
    CategoriaAnimal,
    TipoMedicamento,
    Medicamento,
    Veterinario,
    Alimento,
)

admin.site.register(Raza)
admin.site.register(CategoriaAnimal)
admin.site.register(TipoMedicamento)
admin.site.register(Medicamento)
admin.site.register(Veterinario)
admin.site.register(Alimento)

# Register your models here.
