from django.contrib import admin
from .models import (ConditionsRun, DeparturesRun, LocationsRun,
                     ConditionsRawHTML, DeparturesRawHTML, LocationsRawHTML)

admin.site.register(ConditionsRun)
admin.site.register(DeparturesRun)
admin.site.register(LocationsRun)
admin.site.register(ConditionsRawHTML)
admin.site.register(DeparturesRawHTML)
admin.site.register(LocationsRawHTML)

# Register your models here.
