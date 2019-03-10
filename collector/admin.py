from django.contrib import admin
from .models import (ConditionsRun, DeparturesRun, LocationsRun,
                     ConditionsRawHTML, DeparturesRawHTML, LocationsRawHTML)

class RunAdmin(admin.ModelAdmin):
    list_display = (
        'timestamp',
        'successful',
        'status',
        'html'
    )

admin.site.register(ConditionsRun, RunAdmin)
admin.site.register(DeparturesRun, RunAdmin)
admin.site.register(LocationsRun, RunAdmin)
admin.site.register(ConditionsRawHTML)
admin.site.register(DeparturesRawHTML)
admin.site.register(LocationsRawHTML)

# Register your models here.
